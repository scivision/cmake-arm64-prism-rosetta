# CMake detect ARM64 x86-64 emulation: Windows Prism / macOS Rosetta

[![ci](https://github.com/scivision/cmake-arm64-prism-rosetta/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/cmake-arm64-prism-rosetta/actions/workflows/ci.yml)

Examples of detecting ARM64 x86-64 emulation using CMake, C++, Python, Matlab for Windows Prism or macOS Rosetta.

For C, C++, Fortran by default the compiler uses native mode.

## macOS Rosetta

To force Rosetta use on macOS with Apple Silicon CPU, build with:

```sh
cmake -DCMAKE_OSX_ARCHITECTURES=x86_64 -B build

cmake --build build

ctest --test-dir build -V
```

## Windows Prism

To force Prism use on Windows with ARM64 CPU, build with:

```sh
cmake -DCMAKE_GENERATOR_PLATFORM=x64 -B build

cmake --build build

ctest --test-dir build -V
```

## Other examples

To get physical CPU count, especially for the number of fast "performance" cores, see
[physical-cpu-count](https://github.com/scivision/physical-cpu-count)
single-file C++ project.
