#pragma once
// OpenBiometrics - opt-in research capture tool
// QualityCheck.hpp — placeholder quality-check hooks

#include <string>

namespace obx {

// Returns a value in [0, 1]; lower = blurrier.
// Stub returns 1.0 (assumed sharp) when built without OpenCV.
double measure_blur(const std::string& frame_path);

// Returns average luminance in [0, 255].
// Stub returns 128.0 when built without OpenCV.
double measure_brightness(const std::string& frame_path);

// Returns RMS audio level in dBFS. Stub returns -20.0 dBFS.
double measure_audio_level(const std::string& audio_path);

} // namespace obx
