#pragma once
// OpenBiometrics - opt-in research capture tool
// SessionMeta.hpp — metadata.json writer (no personal identifiers)

#include <string>

namespace obx {

struct SessionMeta {
    // Identifiers / timing
    std::string session_id;       // random UUID-like, no personal info
    std::string start_timestamp;  // ISO-8601
    std::string end_timestamp;    // ISO-8601

    // Modalities recorded
    bool video_recorded = false;
    bool audio_recorded = false;

    // Consent flags (explicit)
    bool consent_video = false;
    bool consent_audio = false;

    // Device info — video
    int    camera_index  = 0;
    int    frame_width   = 0;
    int    frame_height  = 0;
    double fps           = 0.0;

    // Device info — audio
    int    sample_rate   = 0;
    int    audio_channels = 0;

    // Tool version
    std::string tool_version;

    // Write to <path>/metadata.json; returns true on success.
    bool write(const std::string& path) const;
};

// Generate a random de-identified session ID (128-bit hex, no personal data)
std::string make_session_id();

} // namespace obx
