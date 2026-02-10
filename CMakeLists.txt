cmake_minimum_required(VERSION 3.20...4.2)

project(DetectRosetta LANGUAGES C CXX)

enable_testing()

message(STATUS "CMAKE_HOST_SYSTEM_PROCESSOR: ${CMAKE_HOST_SYSTEM_PROCESSOR}")

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  add_executable(has_avx has_avx.cpp)
  add_test(NAME HasAVX COMMAND has_avx)
endif()

add_executable(is_rosetta_c is_rosetta.c)
add_test(NAME C_Rosetta COMMAND is_rosetta_c)

add_executable(is_rosetta_cpp is_rosetta.cpp)
get_target_property(osx_arch is_rosetta_cpp OSX_ARCHITECTURES)
add_test(NAME CPP_Rosetta COMMAND is_rosetta_cpp)

add_executable(is_prism is_prism.cpp)
add_test(NAME CPP_Prism COMMAND is_prism)

if(APPLE)
message(STATUS "OSX_ARCHITECTURES: ${osx_arch}")
endif()


find_package(Python COMPONENTS Interpreter)
if(Python_FOUND)
  add_test(NAME PythonRosetta
  COMMAND Python::Interpreter ${CMAKE_CURRENT_SOURCE_DIR}/is_rosetta.py
  )

  add_test(NAME PythonWindowsPrism
  COMMAND Python::Interpreter ${CMAKE_CURRENT_SOURCE_DIR}/is_prism.py
  )
endif()


get_property(test_names DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY TESTS)

set_tests_properties(${test_names} PROPERTIES TIMEOUT 5)

if(APPLE AND CMAKE_HOST_SYSTEM_PROCESSOR STREQUAL "arm64" AND ${osx_arch} STREQUAL "x86_64")
  set_tests_properties(CPP_Rosetta PROPERTIES PASS_REGULAR_EXPRESSION "is using Rosetta")
else()
  set_tests_properties(CPP_Rosetta PROPERTIES PASS_REGULAR_EXPRESSION "is not using Rosetta")
endif()

if(WIN32 AND CMAKE_HOST_SYSTEM_PROCESSOR STREQUAL "x86_64" AND CMAKE_SYSTEM_PROCESSOR STREQUAL "arm64")
  set_tests_properties(CPP_Prism PROPERTIES PASS_REGULAR_EXPRESSION "is using Microsoft Prism")
else()
  set_tests_properties(CPP_Prism PROPERTIES PASS_REGULAR_EXPRESSION "is not using Microsoft Prism")
endif()


file(GENERATE OUTPUT .gitignore CONTENT "*")
