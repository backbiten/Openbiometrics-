#pragma once
// OpenBiometrics - opt-in research capture tool
// Video capture interface (OpenCV-based)

#include <string>

namespace obx {

struct VideoCaptureConfig {
    int    camera_index = 0;
    int    width        = 0;   // 0 = use camera default
    int    height       = 0;
    double fps          = 0.0;
    std::string output_path;   // path to video.mp4
};

struct VideoDeviceInfo {
    int    camera_index;
    int    frame_width;
    int    frame_height;
    double fps;
};

class VideoRecorder {
public:
    explicit VideoRecorder(const VideoCaptureConfig& cfg);
    ~VideoRecorder();

    // Returns actual device parameters after open()
    bool open();
    void close();

    VideoDeviceInfo device_info() const;

    // Record for 'seconds'. Shows preview window with consent overlay.
    bool record(int seconds);

private:
    struct Impl;
    Impl* impl_ = nullptr;
    VideoCaptureConfig cfg_;
};

} // namespace obx
