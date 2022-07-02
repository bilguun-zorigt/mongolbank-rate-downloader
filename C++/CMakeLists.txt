cmake_minimum_required(VERSION 3.1.0)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_TOOLCHAIN_FILE /usr/local/vcpkg/scripts/buildsystems/vcpkg.cmake)
# set(CMAKE_BUILD_TYPE Release)
project(BoM)
add_executable(${PROJECT_NAME} src/main.cpp)

find_package(cpr CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE cpr::cpr)

# find_path(BSHOSHANY_THREAD_POOL_INCLUDE_DIRS "thread_pool.hpp")
# target_include_directories(${PROJECT_NAME} PRIVATE ${BSHOSHANY_THREAD_POOL_INCLUDE_DIRS})

# find_package(unofficial-gumbo CONFIG REQUIRED)
# target_link_libraries(${PROJECT_NAME} PRIVATE unofficial::gumbo::gumbo)
