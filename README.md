# Openbiometrics-

[![CI](https://github.com/backbiten/Openbiometrics-/actions/workflows/ci.yml/badge.svg)](https://github.com/backbiten/Openbiometrics-/actions/workflows/ci.yml)

For open source development of field biometrics.

## Building

Requires CMake ≥ 3.15 and a C compiler.

```bash
cmake -S . -B build
cmake --build build
```

To enable the camera capture subsystem (requires OpenCV and FFmpeg):

```bash
cmake -S . -B build -DOBX_ENABLE_CAPTURE=ON
cmake --build build
```

## Continuous Integration

CI builds run automatically on every push to `main` and on every pull request.
The matrix covers **Ubuntu** and **Windows** using GitHub Actions.
Builds use `OBX_ENABLE_CAPTURE=OFF` (the default) so no heavy third-party
libraries are required in CI.
