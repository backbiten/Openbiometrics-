// OpenBiometrics (obx) — opt-in research / usability capture tool
//
// ETHICS NOTICE
// =============
// This tool is for consented research and usability studies ONLY.
// Recording without explicit consent is prohibited.
// Outputs are de-identified; no personal identifiers are stored.
// Surveillance use-cases (e.g., RTSP security feeds) are NOT supported.
//
// Usage:
//   obx record --consent yes --video [--audio] --out <dir>
//              [--duration <s>] [--camera-index <n>]

#include "SessionMeta.hpp"
#include "../../collector/VideoCapture.hpp"
#include "../../collector/AudioCapture.hpp"
#include "../../processing/QualityCheck.hpp"

#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <filesystem>

namespace fs = std::filesystem;

// ─── Version ──────────────────────────────────────────────────────────────────
static constexpr const char* OBX_VERSION = "0.1.0";

// ─── Helpers ──────────────────────────────────────────────────────────────────
static std::string iso8601_now() {
    auto now  = std::chrono::system_clock::now();
    auto tt   = std::chrono::system_clock::to_time_t(now);
    std::tm  tm_utc{};
#ifdef _WIN32
    gmtime_s(&tm_utc, &tt);
#else
    gmtime_r(&tt, &tm_utc);
#endif
    std::ostringstream oss;
    oss << std::put_time(&tm_utc, "%Y-%m-%dT%H:%M:%SZ");
    return oss.str();
}

static std::string timestamp_dirname() {
    auto now  = std::chrono::system_clock::now();
    auto tt   = std::chrono::system_clock::to_time_t(now);
    std::tm  tm_utc{};
#ifdef _WIN32
    gmtime_s(&tm_utc, &tt);
#else
    gmtime_r(&tt, &tm_utc);
#endif
    std::ostringstream oss;
    oss << "session_" << std::put_time(&tm_utc, "%Y%m%d_%H%M%S");
    return oss.str();
}

static std::string make_session_id_hex() {
    return obx::make_session_id();
}

// ─── CLI arg parsing ──────────────────────────────────────────────────────────
struct RecordOptions {
    std::string out_dir;
    bool        video        = false;
    bool        audio        = false;
    bool        consent      = false;  // --consent yes required
    int         duration     = 30;
    int         camera_index = 0;
};

static void print_usage(const char* prog) {
    std::cout
        << "Usage:\n"
        << "  " << prog << " record"
        << " --consent yes"
        << " --out <dir>"
        << " [--video]"
        << " [--audio]"
        << " [--duration <seconds>]"
        << " [--camera-index <n>]\n\n"
        << "Flags:\n"
        << "  --consent yes     Required. Affirm that all participants have given\n"
        << "                    explicit, informed consent to be recorded.\n"
        << "  --out <dir>       Output root directory.\n"
        << "  --video           Capture video (requires OpenCV).\n"
        << "  --audio           Capture audio (stub; requires backend).\n"
        << "  --duration <s>    Recording duration in seconds (default: 30).\n"
        << "  --camera-index <n> Camera index (default: 0).\n\n"
        << "Ethics notice:\n"
        << "  obx is for opt-in research / usability studies only.\n"
        << "  Never use it to record anyone without their knowledge.\n";
}

static RecordOptions parse_record_args(int argc, char* argv[]) {
    RecordOptions opts;
    for (int i = 0; i < argc; ++i) {
        std::string a = argv[i];
        auto require_next = [&](const char* flag) -> std::string {
            if (i + 1 >= argc) {
                std::cerr << "[obx] ERROR: " << flag << " requires a value.\n";
                std::exit(2);
            }
            return argv[++i];
        };

        if (a == "--out") {
            opts.out_dir = require_next("--out");
        } else if (a == "--video") {
            opts.video = true;
        } else if (a == "--audio") {
            opts.audio = true;
        } else if (a == "--consent") {
            std::string val = require_next("--consent");
            if (val != "yes") {
                std::cerr << "[obx] ERROR: --consent must be 'yes'. "
                             "Provide explicit consent before recording.\n";
                std::exit(2);
            }
            opts.consent = true;
        } else if (a == "--duration") {
            try {
                opts.duration = std::stoi(require_next("--duration"));
            } catch (...) {
                std::cerr << "[obx] ERROR: --duration must be a positive integer.\n";
                std::exit(2);
            }
            if (opts.duration <= 0) {
                std::cerr << "[obx] ERROR: --duration must be positive.\n";
                std::exit(2);
            }
        } else if (a == "--camera-index") {
            try {
                opts.camera_index = std::stoi(require_next("--camera-index"));
            } catch (...) {
                std::cerr << "[obx] ERROR: --camera-index must be an integer.\n";
                std::exit(2);
            }
        } else {
            std::cerr << "[obx] WARNING: Unknown flag '" << a << "' — ignored.\n";
        }
    }
    return opts;
}

// ─── Subcommand: record ───────────────────────────────────────────────────────
static int cmd_record(int argc, char* argv[]) {
    RecordOptions opts = parse_record_args(argc, argv);

    // ── Consent gate ──────────────────────────────────────────────────────────
    if (!opts.consent) {
        std::cerr
            << "[obx] ERROR: Explicit consent is required to record.\n"
            << "  Run with --consent yes after confirming all participants\n"
            << "  have given informed, voluntary consent.\n";
        return 1;
    }

    if (!opts.video && !opts.audio) {
        std::cerr << "[obx] ERROR: Nothing to record. "
                     "Specify --video and/or --audio.\n";
        return 1;
    }

    if (opts.out_dir.empty()) {
        std::cerr << "[obx] ERROR: --out <dir> is required.\n";
        return 1;
    }

    // ── Create session directory ───────────────────────────────────────────────
    fs::path session_dir = fs::path(opts.out_dir) / timestamp_dirname();
    try {
        fs::create_directories(session_dir);
    } catch (const std::exception& e) {
        std::cerr << "[obx] ERROR: Cannot create session dir: " << e.what() << "\n";
        return 1;
    }

    std::string start_ts = iso8601_now();
    std::cout << "[obx] Session dir : " << session_dir.string() << "\n"
              << "[obx] Start time  : " << start_ts << "\n"
              << "[obx] Duration    : " << opts.duration << "s\n"
              << "[obx] Video       : " << (opts.video ? "yes" : "no") << "\n"
              << "[obx] Audio       : " << (opts.audio ? "yes" : "no") << "\n"
              << "[obx] Consent     : CONFIRMED\n";

    // ── Prepare metadata ──────────────────────────────────────────────────────
    obx::SessionMeta meta;
    meta.session_id      = make_session_id_hex();
    meta.start_timestamp = start_ts;
    meta.tool_version    = OBX_VERSION;
    meta.consent_video   = opts.video;
    meta.consent_audio   = opts.audio;
    meta.camera_index    = opts.camera_index;
    meta.sample_rate     = 44100;
    meta.audio_channels  = 1;

    // ── Video capture ─────────────────────────────────────────────────────────
    bool video_ok = true;
    if (opts.video) {
        obx::VideoCaptureConfig vcfg;
        vcfg.camera_index = opts.camera_index;
        vcfg.output_path  = (session_dir / "video.mp4").string();

        obx::VideoRecorder vr(vcfg);
        if (!vr.open()) {
            std::cerr << "[obx] ERROR: Failed to open video device.\n";
            video_ok = false;
        } else {
            auto di = vr.device_info();
            meta.frame_width  = di.frame_width;
            meta.frame_height = di.frame_height;
            meta.fps          = di.fps;

            std::cout << "[obx] Recording video → " << vcfg.output_path << "\n"
                      << "[obx] Camera          : " << di.frame_width << "x"
                      << di.frame_height << " @ " << di.fps << " fps\n";

            video_ok = vr.record(opts.duration);
            if (!video_ok)
                std::cerr << "[obx] WARNING: Video recording encountered an error.\n";
            else
                meta.video_recorded = true;
        }
    }

    // ── Audio capture ─────────────────────────────────────────────────────────
    bool audio_ok = true;
    if (opts.audio) {
        obx::AudioCaptureConfig acfg;
        acfg.sample_rate  = 44100;
        acfg.channels     = 1;
        acfg.output_path  = (session_dir / "audio.m4a").string();

        obx::AudioRecorder ar(acfg);
        if (!ar.open()) {
            std::cerr << "[obx] ERROR: Failed to open audio device.\n";
            audio_ok = false;
        } else {
            std::cout << "[obx] Recording audio → " << acfg.output_path << "\n";
            audio_ok = ar.record(opts.duration);
            if (!audio_ok)
                std::cerr << "[obx] WARNING: Audio recording encountered an error.\n";
            else
                meta.audio_recorded = true;
        }
    }

    // ── Finish metadata ───────────────────────────────────────────────────────
    meta.end_timestamp = iso8601_now();
    std::string meta_path = (session_dir / "metadata.json").string();
    if (!meta.write(meta_path)) {
        std::cerr << "[obx] ERROR: Failed to write metadata.json.\n";
        return 1;
    }
    std::cout << "[obx] Metadata    → " << meta_path << "\n";

    bool any_error = (opts.video && !video_ok) || (opts.audio && !audio_ok);
    if (any_error) {
        std::cerr << "[obx] Session completed with errors.\n";
        return 1;
    }
    std::cout << "[obx] Session complete.\n";
    return 0;
}

// ─── Entry point ──────────────────────────────────────────────────────────────
int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    std::string subcmd = argv[1];
    if (subcmd == "record") {
        return cmd_record(argc - 2, argv + 2);
    } else if (subcmd == "--help" || subcmd == "-h" || subcmd == "help") {
        print_usage(argv[0]);
        return 0;
    } else {
        std::cerr << "[obx] ERROR: Unknown subcommand '" << subcmd << "'.\n";
        print_usage(argv[0]);
        return 1;
    }
}
