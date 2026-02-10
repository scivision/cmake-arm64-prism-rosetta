#ifdef _WIN32

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <wow64apiset.h>

#ifndef IsWow64Process2
typedef BOOL (WINAPI *LPFN_ISWOW64PROCESS2)(HANDLE, USHORT*, USHORT*);
#endif

#endif

#include <iostream>
#include <cstdlib>

// Detects if the current process is running under Prism emulation on Windows on ARM.
// This checks if the process architecture is x86 or x64 while the native machine is ARM64.

bool is_prism() {
// https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-iswow64process2
#if defined(_WIN32)
    USHORT processMachine = IMAGE_FILE_MACHINE_UNKNOWN;
    USHORT nativeMachine = IMAGE_FILE_MACHINE_UNKNOWN;

#ifndef IsWow64Process2
    HMODULE kernel32 = GetModuleHandleW(L"kernel32.dll");
    if (!kernel32) return false;

    LPFN_ISWOW64PROCESS2 fnIsWow64Process2 =
        (LPFN_ISWOW64PROCESS2)GetProcAddress(kernel32, "IsWow64Process2");

    if (!fnIsWow64Process2 || !fnIsWow64Process2(GetCurrentProcess(), &processMachine, &nativeMachine)) {
        return false;
    }
#else
    if (!IsWow64Process2(GetCurrentProcess(), &processMachine, &nativeMachine)) {
        // Failed to query; assume not emulated
        return false;
    }
#endif
    // Check if process is x86 or x64 and host is ARM64
    return (processMachine == IMAGE_FILE_MACHINE_I386 ||
            processMachine == IMAGE_FILE_MACHINE_AMD64) &&
           nativeMachine == IMAGE_FILE_MACHINE_ARM64;
#else
  return false;
#endif
}


int main(int argc, char ** argv) {

  std::cout << argv[0] << " is " << (is_prism() ? "" : "not ") << "using Microsoft Prism emulation.\n";

  return EXIT_SUCCESS;
}
