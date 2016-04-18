cmake_minimum_required(VERSION 2.8)

set(project_name framer)
project(${project_name})

file(GLOB SOURCES "*.cpp" "*.c" "*.h")

# OpenCV
find_package(OpenCV REQUIRED)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x -O3 -Wall")
add_executable(${project_name} ${SOURCES})

target_link_libraries(${project_name} ${OpenCV_LIBS})