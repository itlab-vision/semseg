cmake_minimum_required(VERSION 2.8)

set(project_name classify)
project(${project_name})

file(GLOB SOURCES "*.cpp" "*.c" "*.h")

# OpenCV
find_package(OpenCV REQUIRED)
find_package(Caffe REQUIRED)

# Caffe
include_directories(${Caffe_INCLUDE_DIRS})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x -O3 -Wall")
add_executable(${project_name} ${SOURCES})

target_link_libraries(${project_name} ${OpenCV_LIBS} ${Caffe_LIBRARIES})
