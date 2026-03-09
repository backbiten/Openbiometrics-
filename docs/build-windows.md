# Building obx on Windows

## Prerequisites

| Tool | Recommended source |
|------|--------------------|
| CMake ≥ 3.16 | https://cmake.org/download/ |
| Visual Studio 2019/2022 (with "Desktop development with C++") | https://visualstudio.microsoft.com/ |
| Git | https://git-scm.com/ |

### OpenCV (optional — enables real video capture)

1. Download the Windows installer from https://opencv.org/releases/
2. Extract to e.g. `C:\opencv`
3. Add `C:\opencv\build\x64\vc16\bin` to your `PATH`
4. Set `OpenCV_DIR` when configuring CMake (see below)

### FFmpeg (future — audio encoding)

Not required for Milestone 1. Audio capture is a stub in this release.

---

## Configure & Build

Open a **Developer Command Prompt** (or PowerShell with VS environment loaded):

```powershell
# Clone the repository
git clone https://github.com/backbiten/Openbiometrics-.git
cd Openbiometrics-

# Configure (with OpenCV)
cmake -B build -G "Visual Studio 17 2022" -A x64 `
      -DOpenCV_DIR="C:/opencv/build" `
      -DOBX_WITH_OPENCV=ON

# Configure (without OpenCV — stub mode)
cmake -B build -G "Visual Studio 17 2022" -A x64 `
      -DOBX_WITH_OPENCV=OFF

# Build
cmake --build build --config Release

# The executable is at:
#   build\Release\obx.exe
```

---

## Run example

```powershell
# Create output directory
mkdir out

# Record 5 seconds of video (consent required)
.\build\Release\obx.exe record `
    --consent yes `
    --video `
    --out out `
    --duration 5

# Output:
#   out\session_YYYYMMDD_HHMMSS\video.mp4
#   out\session_YYYYMMDD_HHMMSS\metadata.json
```

### Without consent (expected failure)

```powershell
.\build\Release\obx.exe record --video --out out
# [obx] ERROR: Explicit consent is required to record.
# Exit code: 1
```

---

## Ethics reminder

`obx` is for **opt-in research / usability studies only**.  
Never record anyone without their explicit, informed consent.  
See [ethics.md](ethics.md) for full policy.
