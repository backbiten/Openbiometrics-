cmake_minimum_required(VERSION 3.15)
project(openbiometrics VERSION 0.1.0 LANGUAGES C)

# Optional capture subsystem (requires OpenCV/FFmpeg when ON).
# Disabled by default so CI builds remain lightweight.
option(OBX_ENABLE_CAPTURE "Enable camera capture subsystem (requires OpenCV/FFmpeg)" OFF)

add_executable(obx src/main.c)

target_compile_definitions(obx PRIVATE
    OBX_VERSION="${PROJECT_VERSION}"
)

if(OBX_ENABLE_CAPTURE)
    target_compile_definitions(obx PRIVATE OBX_ENABLE_CAPTURE)
    message(STATUS "Capture subsystem: ENABLED (OpenCV/FFmpeg required)")
else()
    message(STATUS "Capture subsystem: DISABLED (stub build)")
endif()

install(TARGETS obx RUNTIME DESTINATION bin)
