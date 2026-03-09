# Building obx on Linux

## Prerequisites

```bash
# Debian / Ubuntu
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    git \
    libopencv-dev       # optional — enables real video capture
```

```bash
# Fedora / RHEL
sudo dnf install -y \
    gcc-c++ \
    cmake \
    git \
    opencv-devel        # optional
```

### FFmpeg (future — audio encoding)

Not required for Milestone 1. Audio capture is a stub in this release.

For future use:
```bash
# Debian / Ubuntu
sudo apt-get install -y libavcodec-dev libavformat-dev libswresample-dev
```

---

## Configure & Build

```bash
# Clone the repository
git clone https://github.com/backbiten/Openbiometrics-.git
cd Openbiometrics-

# Configure (with OpenCV — auto-detected)
cmake -B build -DCMAKE_BUILD_TYPE=Release -DOBX_WITH_OPENCV=ON

# Configure (without OpenCV — stub mode)
cmake -B build -DCMAKE_BUILD_TYPE=Release -DOBX_WITH_OPENCV=OFF

# Build
cmake --build build --parallel

# The executable is at:
#   build/obx
```

---

## Run example

```bash
# Create output directory
mkdir -p out

# Record 5 seconds of video (consent required)
./build/obx record \
    --consent yes \
    --video \
    --out out \
    --duration 5

# Output:
#   out/session_YYYYMMDD_HHMMSS/video.mp4
#   out/session_YYYYMMDD_HHMMSS/metadata.json
```

### With audio (stub)

```bash
./build/obx record \
    --consent yes \
    --video \
    --audio \
    --out out \
    --duration 5
```

### Without consent (expected failure)

```bash
./build/obx record --video --out out
# [obx] ERROR: Explicit consent is required to record.
# exit status 1
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `Cannot open camera index 0` | No webcam / permissions | Check `/dev/video0`, try `--camera-index 1` |
| `video.mp4` is a stub file | Built without OpenCV | Install `libopencv-dev` and rebuild |
| Linker error `stdc++fs` | GCC < 9 | Upgrade to GCC ≥ 9 or Ubuntu 20.04+ |

---

## Ethics reminder

`obx` is for **opt-in research / usability studies only**.  
Never record anyone without their explicit, informed consent.  
See [ethics.md](ethics.md) for full policy.
