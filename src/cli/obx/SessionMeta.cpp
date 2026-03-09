// OpenBiometrics - opt-in research capture tool
// SessionMeta.cpp — write metadata.json with no personal identifiers

#include "SessionMeta.hpp"

#include <fstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <random>
#include <chrono>
#include <ctime>

namespace obx {

static std::string generate_session_id() {
    // Random 128-bit hex, no personal data
    std::mt19937_64 rng(
        static_cast<uint64_t>(
            std::chrono::steady_clock::now().time_since_epoch().count()));
    std::uniform_int_distribution<uint64_t> dist;
    std::ostringstream oss;
    oss << std::hex << std::setfill('0')
        << std::setw(16) << dist(rng)
        << std::setw(16) << dist(rng);
    return oss.str();
}

std::string make_session_id() { return generate_session_id(); }

// Escape a JSON string value (minimal — handles common chars)
static std::string json_str(const std::string& s) {
    std::string out;
    out.reserve(s.size() + 2);
    out += '"';
    for (char c : s) {
        switch (c) {
            case '"':  out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\n': out += "\\n";  break;
            case '\r': out += "\\r";  break;
            case '\t': out += "\\t";  break;
            default:   out += c;      break;
        }
    }
    out += '"';
    return out;
}

static std::string bool_str(bool b) { return b ? "true" : "false"; }

bool SessionMeta::write(const std::string& path) const {
    if (session_id.empty()) {
        std::cerr << "[obx] ERROR: session_id not set before writing metadata.\n";
        return false;
    }

    std::ofstream f(path);
    if (!f) {
        std::cerr << "[obx] ERROR: Cannot open " << path << " for writing.\n";
        return false;
    }

    f << "{\n"
      << "  \"session_id\": "       << json_str(session_id)      << ",\n"
      << "  \"start_timestamp\": "  << json_str(start_timestamp) << ",\n"
      << "  \"end_timestamp\": "    << json_str(end_timestamp)   << ",\n"
      << "  \"tool_version\": "     << json_str(tool_version)    << ",\n"
      << "  \"modalities\": {\n"
      << "    \"video_recorded\": " << bool_str(video_recorded)  << ",\n"
      << "    \"audio_recorded\": " << bool_str(audio_recorded)  << "\n"
      << "  },\n"
      << "  \"consent\": {\n"
      << "    \"video\": "          << bool_str(consent_video)   << ",\n"
      << "    \"audio\": "          << bool_str(consent_audio)   << "\n"
      << "  },\n"
      << "  \"device_video\": {\n"
      << "    \"camera_index\": "   << camera_index              << ",\n"
      << "    \"frame_width\": "    << frame_width               << ",\n"
      << "    \"frame_height\": "   << frame_height              << ",\n"
      << "    \"fps\": "            << fps                       << "\n"
      << "  },\n"
      << "  \"device_audio\": {\n"
      << "    \"sample_rate\": "    << sample_rate               << ",\n"
      << "    \"channels\": "       << audio_channels            << "\n"
      << "  }\n"
      << "}\n";

    return true;
}

} // namespace obx
