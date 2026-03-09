#pragma once
// OpenBiometrics - opt-in research capture tool
// Audio capture interface stub (FFmpeg/PortAudio-based, extensible)

#include <string>

namespace obx {

struct AudioCaptureConfig {
    int sample_rate = 44100;
    int channels    = 1;
    std::string output_path;  // path to audio.m4a
};

struct AudioDeviceInfo {
    int sample_rate;
    int channels;
};

class AudioRecorder {
public:
    explicit AudioRecorder(const AudioCaptureConfig& cfg);
    ~AudioRecorder();

    bool open();
    void close();

    AudioDeviceInfo device_info() const;

    // Record for 'seconds'. Blocks until done.
    bool record(int seconds);

private:
    AudioCaptureConfig cfg_;
    bool opened_ = false;
};

} // namespace obx
