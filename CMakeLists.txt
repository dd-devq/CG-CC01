cmake_minimum_required(VERSION 3.0..3.2)

project(CG-CC01)

option(GLFW_BUILD_DOCS OFF)
option(GLFW_BUILD_EXAMPLES OFF)
option(GLFW_BUILD_TESTS OFF)
add_subdirectory(vendor/glfw)

option(ASSIMP_BUILD_ASSIMP_TOOLS OFF)
option(ASSIMP_BUILD_SAMPLES OFF)
option(ASSIMP_BUILD_TESTS OFF)
add_subdirectory(vendor/assimp)

if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -std=c++11")
    if(NOT WIN32)
        set(GLAD_LIBRARIES dl)
    endif()
endif()

include_directories(
    src/
    src/primitives/
    vendor/assimp/include/
    vendor/glad/include/
    vendor/glfw/include/
    vendor/glm/
    vendor/stb/
    vendor/imgui/
)

file(GLOB VENDOR_SOURCES 
    vendor/glad/src/glad.c
    vendor/imgui/*.cpp
)

file(GLOB PROJECT_HEADERS src/*.h)

file(GLOB PROJECT_SOURCES src/*.cpp)

file(GLOB PROJECT_SHADERS resources/shaders/*.glsl
                          resources/shaders/*.frag
                          resources/shaders/*.vert
                          resources/shaders/lighting/*.glsl
                          resources/shaders/lighting/*.frag
                          resources/shaders/lighting/*.vert
                          resources/shaders/lighting/ibl/*.glsl
                          resources/shaders/lighting/ibl/*.frag
                          resources/shaders/lighting/ibl/*.vert
                          resources/shaders/postprocess/*.glsl
                          resources/shaders/postprocess/*.frag
                          resources/shaders/postprocess/*.vert)

file(GLOB PROJECT_CONFIGS CMakeLists.txt
                          Readme.md
                         .gitattributes
                         .gitignore
                         .gitmodules)

source_group("Headers" FILES ${PROJECT_HEADERS})
source_group("Shaders" FILES ${PROJECT_SHADERS})
source_group("Sources" FILES ${PROJECT_SOURCES})
source_group("Vendor" FILES ${VENDOR_SOURCES})

add_definitions(-DGLFW_INCLUDE_NONE
                -DPROJECT_SOURCE_DIR=\"${PROJECT_SOURCE_DIR}\")

add_executable(${PROJECT_NAME} ${PROJECT_SOURCES} ${PROJECT_HEADERS}
                               ${PROJECT_SHADERS} ${PROJECT_CONFIGS}
                               ${VENDOR_SOURCES})

target_link_libraries(${PROJECT_NAME} assimp glfw
                      ${GLFW_LIBRARIES} ${GLAD_LIBRARIES})
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${PROJECT_NAME})
