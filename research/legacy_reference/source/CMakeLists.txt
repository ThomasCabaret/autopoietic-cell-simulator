cmake_minimum_required(VERSION 3.24 FATAL_ERROR)

# Preserve the historical "cmake -S . -B build" workflow when the vcpkg
# submodule is present. Presets and explicit -D values still take precedence.
if(NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(_particle_life_vcpkg_toolchain
        "${CMAKE_CURRENT_SOURCE_DIR}/external/vcpkg/scripts/buildsystems/vcpkg.cmake")
    if(EXISTS "${_particle_life_vcpkg_toolchain}")
        set(CMAKE_TOOLCHAIN_FILE "${_particle_life_vcpkg_toolchain}"
            CACHE FILEPATH "vcpkg toolchain file")
    endif()
endif()

project(ParticleLife VERSION 0.1.0 LANGUAGES CXX)

include(CTest)

option(PARTICLE_LIFE_BUILD_GUI "Build the SFML/ImGui interactive viewer" ON)
option(PARTICLE_LIFE_BUILD_HEADLESS "Build the command-line runner" ON)
option(PARTICLE_LIFE_BUILD_REGRESSION "Build the spatial-grid regression executable" ON)
option(PARTICLE_LIFE_BUILD_TEMPLATE_COPY_DEMO "Build the standalone template-copy demonstrator" ON)

if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS Debug Release RelWithDebInfo MinSizeRel)
endif()

set(PARTICLE_LIFE_CORE_SOURCES
    src/checkpoint.cpp
    src/experiment.cpp
    src/metrics.cpp
    src/runner.cpp
    src/simulation.cpp
    src/spatial_grid.cpp
)

add_library(particle_life_core STATIC ${PARTICLE_LIFE_CORE_SOURCES})
add_library(ParticleLife::Core ALIAS particle_life_core)

target_include_directories(particle_life_core
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)
target_compile_features(particle_life_core PUBLIC cxx_std_17)

if(MSVC)
    target_compile_options(particle_life_core PRIVATE /W4 /permissive- /Zc:__cplusplus)
else()
    target_compile_options(particle_life_core PRIVATE -Wall -Wextra -Wpedantic)
endif()


add_library(template_copy_core STATIC src/template_copy.cpp)
add_library(ParticleLife::TemplateCopy ALIAS template_copy_core)
target_include_directories(template_copy_core
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)
target_compile_features(template_copy_core PUBLIC cxx_std_17)

if(MSVC)
    target_compile_options(template_copy_core PRIVATE /W4 /permissive- /Zc:__cplusplus)
else()
    target_compile_options(template_copy_core PRIVATE -Wall -Wextra -Wpedantic)
endif()

if(PARTICLE_LIFE_BUILD_GUI)
    find_package(imgui CONFIG REQUIRED)
    find_package(SFML 2.6 CONFIG REQUIRED COMPONENTS graphics window system)
    find_package(ImGui-SFML CONFIG REQUIRED)

    add_executable(ParticleLife src/interactive_main.cpp)
    target_link_libraries(ParticleLife
        PRIVATE
            ParticleLife::Core
            imgui::imgui
            sfml-graphics
            sfml-window
            sfml-system
            ImGui-SFML::ImGui-SFML
    )
    target_compile_features(ParticleLife PRIVATE cxx_std_17)

    add_custom_command(
        TARGET ParticleLife POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "${CMAKE_CURRENT_SOURCE_DIR}/imgui.ini"
            "$<TARGET_FILE_DIR:ParticleLife>/imgui.ini"
        VERBATIM
    )

    if(PARTICLE_LIFE_BUILD_TEMPLATE_COPY_DEMO)
        add_executable(TemplateCopyDemo src/template_copy_demo_main.cpp)
        target_link_libraries(TemplateCopyDemo
            PRIVATE
                ParticleLife::TemplateCopy
                imgui::imgui
                sfml-graphics
                sfml-window
                sfml-system
                ImGui-SFML::ImGui-SFML
        )
        target_compile_features(TemplateCopyDemo PRIVATE cxx_std_17)

        add_custom_command(
            TARGET TemplateCopyDemo POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
                "${CMAKE_CURRENT_SOURCE_DIR}/imgui.ini"
                "$<TARGET_FILE_DIR:TemplateCopyDemo>/imgui.ini"
            VERBATIM
        )
    endif()
endif()

if(PARTICLE_LIFE_BUILD_HEADLESS)
    add_executable(ParticleLifeHeadless src/headless_main.cpp)
    target_link_libraries(ParticleLifeHeadless PRIVATE ParticleLife::Core)
    target_compile_features(ParticleLifeHeadless PRIVATE cxx_std_17)

    if(PARTICLE_LIFE_BUILD_TEMPLATE_COPY_DEMO)
        add_executable(TemplateCopyHeadless src/template_copy_headless_main.cpp)
        target_link_libraries(TemplateCopyHeadless PRIVATE ParticleLife::TemplateCopy)
        target_compile_features(TemplateCopyHeadless PRIVATE cxx_std_17)
    endif()
endif()

if(PARTICLE_LIFE_BUILD_REGRESSION)
    add_executable(ParticleLifeSpatialGridRegression src/spatial_grid_regression_main.cpp)
    target_link_libraries(ParticleLifeSpatialGridRegression PRIVATE ParticleLife::Core)
    target_compile_features(ParticleLifeSpatialGridRegression PRIVATE cxx_std_17)

    add_executable(TemplateCopySmoke src/template_copy_smoke_main.cpp)
    target_link_libraries(TemplateCopySmoke PRIVATE ParticleLife::TemplateCopy)
    target_compile_features(TemplateCopySmoke PRIVATE cxx_std_17)

    if(BUILD_TESTING)
        add_test(
            NAME spatial_grid_matches_bruteforce
            COMMAND ParticleLifeSpatialGridRegression
        )
        add_test(
            NAME template_copy_smoke
            COMMAND TemplateCopySmoke
        )
        set_tests_properties(template_copy_smoke PROPERTIES TIMEOUT 60)
    endif()
endif()
