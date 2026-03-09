# OpenBiometrics (`obx`)

[![CI](https://github.com/backbiten/Openbiometrics-/actions/workflows/ci.yml/badge.svg)](https://github.com/backbiten/Openbiometrics-/actions/workflows/ci.yml)

> **Opt-in research capture tool — for consented usability studies only.**

`obx` is an open-source C++ command-line tool for recording video and audio
sessions during research and usability studies. It is built with
[OpenCV](https://opencv.org/) and [FFmpeg](https://ffmpeg.org/) (audio TBD)
and targets Windows and Linux.

---

## ⚠️ Ethical Use — Read This First

**`obx` is for opt-in research / usability studies ONLY.**

- **Explicit consent is required.** The `--consent yes` flag must be passed on
  every recording invocation. Without it the tool exits immediately.
- **No hidden recording.** The preview window displays a prominent
  `RECORDING (CONSENTED)` overlay while a session is active.
- **De-identified outputs only.** `metadata.json` never contains names,
  transcripts, or personal identifiers.
- **Surveillance is not supported.** Network camera feeds (RTSP etc.) are
  intentionally out of scope.

See [docs/ethics.md](docs/ethics.md) for the full responsible-use policy.

---

## Quick Start

```bash
# Build (Linux example — see docs/ for full instructions)
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel

# Record 5 seconds of video with consent
./build/obx record --consent yes --video --out out --duration 5

# Session outputs:
#   out/session_YYYYMMDD_HHMMSS/video.mp4
#   out/session_YYYYMMDD_HHMMSS/metadata.json
```

---

## Features (Milestone 1)

| Feature | Status |
|---------|--------|
| `obx record` CLI with consent gate | ✅ |
| Video capture (OpenCV / H.264) | ✅ (stub if OpenCV absent) |
| Preview window with consent overlay | ✅ |
| Audio capture (AAC) | 🔧 stub — backend TBD |
| `metadata.json` (de-identified) | ✅ |
| Quality-check hooks (blur / brightness / audio level) | 🔧 stub |
| Windows & Linux builds | ✅ |
| GitHub Actions CI | ✅ |

---

## Documentation

- [docs/build-linux.md](docs/build-linux.md) — Linux build instructions
- [docs/build-windows.md](docs/build-windows.md) — Windows build instructions
- [docs/ethics.md](docs/ethics.md) — Ethics & responsible-use policy

---

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
