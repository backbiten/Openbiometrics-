// OpenBiometrics - opt-in research capture tool
// AudioCapture.cpp — stub audio recorder (extend with PortAudio/FFmpeg)

#include "AudioCapture.hpp"

#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>

namespace obx {

AudioRecorder::AudioRecorder(const AudioCaptureConfig& cfg) : cfg_(cfg) {}
AudioRecorder::~AudioRecorder() { close(); }

bool AudioRecorder::open() {
    // TODO: initialise real audio backend (PortAudio / FFmpeg avdevice)
    std::cout << "[obx] NOTE: Audio recorder opened (stub — no real capture).\n";
    opened_ = true;
    return true;
}

void AudioRecorder::close() {
    if (opened_) {
        // TODO: tear down audio backend
        opened_ = false;
    }
}

AudioDeviceInfo AudioRecorder::device_info() const {
    return {cfg_.sample_rate, cfg_.channels};
}

bool AudioRecorder::record(int seconds) {
    if (!opened_) {
        std::cerr << "[obx] ERROR: AudioRecorder not opened.\n";
        return false;
    }

    std::cout << "[obx] (stub) Simulating audio capture for " << seconds << "s ...\n";
    // Write a minimal placeholder file so downstream code can detect it
    {
        std::ofstream f(cfg_.output_path, std::ios::binary);
        if (f) f << "OBX_STUB_AUDIO\n";
    }
    std::this_thread::sleep_for(std::chrono::seconds(seconds));
    return true;
}

} // namespace obx
