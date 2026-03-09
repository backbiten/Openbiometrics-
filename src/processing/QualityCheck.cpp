// OpenBiometrics - opt-in research capture tool
// QualityCheck.cpp — placeholder quality-check implementations

#include "QualityCheck.hpp"

#include <iostream>

#ifdef OBX_HAVE_OPENCV
#  include <opencv2/opencv.hpp>
#endif

namespace obx {

double measure_blur(const std::string& frame_path) {
#ifdef OBX_HAVE_OPENCV
    cv::Mat img = cv::imread(frame_path, cv::IMREAD_GRAYSCALE);
    if (img.empty()) {
        std::cerr << "[obx] measure_blur: cannot read " << frame_path << "\n";
        return 0.0;
    }
    cv::Mat laplacian;
    cv::Laplacian(img, laplacian, CV_64F);
    cv::Scalar mean, stddev;
    cv::meanStdDev(laplacian, mean, stddev);
    double variance = stddev.val[0] * stddev.val[0];
    // Normalize: 0 = very blurry, 1 = sharp (clamp at 500)
    return std::min(variance / 500.0, 1.0);
#else
    (void)frame_path;
    return 1.0; // stub: assume sharp
#endif
}

double measure_brightness(const std::string& frame_path) {
#ifdef OBX_HAVE_OPENCV
    cv::Mat img = cv::imread(frame_path, cv::IMREAD_COLOR);
    if (img.empty()) {
        std::cerr << "[obx] measure_brightness: cannot read " << frame_path << "\n";
        return 0.0;
    }
    cv::Scalar mean = cv::mean(img);
    return (mean[0] + mean[1] + mean[2]) / 3.0;
#else
    (void)frame_path;
    return 128.0; // stub: mid-range luminance
#endif
}

double measure_audio_level(const std::string& audio_path) {
    // TODO: use FFmpeg libavcodec to decode and compute RMS
    (void)audio_path;
    return -20.0; // stub: -20 dBFS
}

} // namespace obx
