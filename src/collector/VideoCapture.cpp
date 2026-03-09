// OpenBiometrics - opt-in research capture tool
// VideoCapture.cpp — OpenCV-based video recorder with consent overlay

#include "VideoCapture.hpp"

#include <iostream>
#include <fstream>
#include <stdexcept>
#include <chrono>
#include <thread>

#ifdef OBX_HAVE_OPENCV
#  include <opencv2/opencv.hpp>
#endif

namespace obx {

struct VideoRecorder::Impl {
#ifdef OBX_HAVE_OPENCV
    cv::VideoCapture cap;
    cv::VideoWriter  writer;
#endif
    VideoDeviceInfo info{};
};

VideoRecorder::VideoRecorder(const VideoCaptureConfig& cfg)
    : impl_(new Impl), cfg_(cfg) {}

VideoRecorder::~VideoRecorder() {
    close();
    delete impl_;
}

bool VideoRecorder::open() {
#ifdef OBX_HAVE_OPENCV
    if (!impl_->cap.open(cfg_.camera_index)) {
        std::cerr << "[obx] ERROR: Cannot open camera index " << cfg_.camera_index << "\n";
        return false;
    }
    if (cfg_.width  > 0) impl_->cap.set(cv::CAP_PROP_FRAME_WIDTH,  cfg_.width);
    if (cfg_.height > 0) impl_->cap.set(cv::CAP_PROP_FRAME_HEIGHT, cfg_.height);
    if (cfg_.fps    > 0) impl_->cap.set(cv::CAP_PROP_FPS,          cfg_.fps);

    impl_->info.camera_index = cfg_.camera_index;
    impl_->info.frame_width  = static_cast<int>(impl_->cap.get(cv::CAP_PROP_FRAME_WIDTH));
    impl_->info.frame_height = static_cast<int>(impl_->cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    impl_->info.fps          = impl_->cap.get(cv::CAP_PROP_FPS);
    if (impl_->info.fps <= 0) impl_->info.fps = 25.0;
    return true;
#else
    // Stub: no OpenCV — fill in defaults and return true
    impl_->info.camera_index = cfg_.camera_index;
    impl_->info.frame_width  = (cfg_.width  > 0) ? cfg_.width  : 640;
    impl_->info.frame_height = (cfg_.height > 0) ? cfg_.height : 480;
    impl_->info.fps          = (cfg_.fps    > 0) ? cfg_.fps    : 25.0;
    std::cout << "[obx] NOTE: Built without OpenCV; video capture is simulated.\n";
    return true;
#endif
}

void VideoRecorder::close() {
#ifdef OBX_HAVE_OPENCV
    if (impl_->writer.isOpened()) impl_->writer.release();
    if (impl_->cap.isOpened())    impl_->cap.release();
#endif
}

VideoDeviceInfo VideoRecorder::device_info() const { return impl_->info; }

bool VideoRecorder::record(int seconds) {
#ifdef OBX_HAVE_OPENCV
    if (!impl_->cap.isOpened()) {
        std::cerr << "[obx] ERROR: Camera not opened.\n";
        return false;
    }

    int fourcc = cv::VideoWriter::fourcc('a','v','c','1');
    bool writer_ok = impl_->writer.open(
        cfg_.output_path, fourcc, impl_->info.fps,
        cv::Size(impl_->info.frame_width, impl_->info.frame_height));
    if (!writer_ok) {
        std::cerr << "[obx] ERROR: Cannot open video writer at " << cfg_.output_path << "\n";
        return false;
    }

    const std::string window_name = "OBX Preview";
    cv::namedWindow(window_name, cv::WINDOW_AUTOSIZE);

    const int total_frames = static_cast<int>(impl_->info.fps * seconds);
    const std::string overlay_text = "RECORDING (CONSENTED)";
    const cv::Scalar overlay_color(0, 0, 220); // red in BGR
    const int font_face  = cv::FONT_HERSHEY_SIMPLEX;
    const double font_scale = 0.9;
    const int thickness  = 2;

    cv::Mat frame;
    for (int f = 0; f < total_frames; ++f) {
        if (!impl_->cap.read(frame) || frame.empty()) break;

        impl_->writer.write(frame);

        // Draw consent overlay on the preview copy
        cv::Mat preview = frame.clone();
        cv::putText(preview, overlay_text,
                    cv::Point(10, 30), font_face, font_scale,
                    overlay_color, thickness);
        cv::imshow(window_name, preview);

        // Allow ESC to abort recording
        if (cv::waitKey(1) == 27) {
            std::cout << "[obx] Recording interrupted by user.\n";
            break;
        }
    }

    cv::destroyWindow(window_name);
    impl_->writer.release();
    return true;
#else
    // Stub behaviour: just wait the requested duration
    std::cout << "[obx] (stub) Simulating video capture for " << seconds << "s ...\n";
    // Write a minimal placeholder file so downstream code can detect it
    {
        std::ofstream f(cfg_.output_path, std::ios::binary);
        if (f) f << "OBX_STUB_VIDEO\n";
    }
    std::this_thread::sleep_for(std::chrono::seconds(seconds));
    return true;
#endif
}

} // namespace obx
