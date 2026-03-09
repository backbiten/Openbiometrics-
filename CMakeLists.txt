cmake_minimum_required(VERSION 3.16)
project(OpenBiometrics VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ──────────────────────────────────────────────────────────────────────────────
# Options
# ──────────────────────────────────────────────────────────────────────────────
option(OBX_WITH_OPENCV "Enable OpenCV video capture" ON)
option(OBX_WITH_FFMPEG "Enable FFmpeg for audio encoding (future)" OFF)

# ──────────────────────────────────────────────────────────────────────────────
# Dependencies
# ──────────────────────────────────────────────────────────────────────────────
if(OBX_WITH_OPENCV)
    find_package(OpenCV QUIET)
    if(OpenCV_FOUND)
        message(STATUS "[obx] OpenCV ${OpenCV_VERSION} found — video capture enabled")
        add_compile_definitions(OBX_HAVE_OPENCV)
    else()
        message(STATUS "[obx] OpenCV NOT found — building without video capture (stub mode)")
    endif()
endif()

# ──────────────────────────────────────────────────────────────────────────────
# Processing library
# ──────────────────────────────────────────────────────────────────────────────
add_library(obx_processing
    src/processing/QualityCheck.cpp
)
target_include_directories(obx_processing PUBLIC src/processing)
if(OpenCV_FOUND)
    target_link_libraries(obx_processing PUBLIC ${OpenCV_LIBS})
    target_include_directories(obx_processing PUBLIC ${OpenCV_INCLUDE_DIRS})
endif()

# ──────────────────────────────────────────────────────────────────────────────
# Collector library
# ──────────────────────────────────────────────────────────────────────────────
add_library(obx_collector
    src/collector/VideoCapture.cpp
    src/collector/AudioCapture.cpp
)
target_include_directories(obx_collector PUBLIC src/collector)
if(OpenCV_FOUND)
    target_link_libraries(obx_collector PUBLIC ${OpenCV_LIBS})
    target_include_directories(obx_collector PUBLIC ${OpenCV_INCLUDE_DIRS})
endif()

# ──────────────────────────────────────────────────────────────────────────────
# CLI executable: obx
# ──────────────────────────────────────────────────────────────────────────────
add_executable(obx
    src/cli/obx/main.cpp
    src/cli/obx/SessionMeta.cpp
)
target_include_directories(obx PRIVATE src/cli/obx src/collector src/processing)
target_link_libraries(obx PRIVATE obx_collector obx_processing)

# Filesystem support (GCC < 9 needs -lstdc++fs)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU" AND CMAKE_CXX_COMPILER_VERSION VERSION_LESS "9")
    target_link_libraries(obx PRIVATE stdc++fs)
endif()

# ──────────────────────────────────────────────────────────────────────────────
# Install
# ──────────────────────────────────────────────────────────────────────────────
install(TARGETS obx RUNTIME DESTINATION bin)
