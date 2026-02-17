#if defined(_WIN32) || defined(__MINGW32__) || defined(__CYGWIN__)
#define WIN_LIKE
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <wow64apiset.h>
#endif

#include <iostream>
#include <iomanip>

bool is_prism() {
#if defined(WIN_LIKE)
    USHORT processMachine = IMAGE_FILE_MACHINE_UNKNOWN;
    USHORT nativeMachine  = IMAGE_FILE_MACHINE_UNKNOWN;

    PROCESS_MACHINE_INFORMATION info = {};
    DWORD size = sizeof(info);

    if (GetProcessInformation(GetCurrentProcess(), ProcessMachineTypeInfo, &info, size)) {
        USHORT actualProcessMachine = info.ProcessMachine;

        std::cout << "Actual process machine (GetProcessInformation): 0x"
                  << std::hex << actualProcessMachine << "\n";

        // If process reports AMD64, check if host is ARM64 (true Prism emulation)
        if (actualProcessMachine == IMAGE_FILE_MACHINE_AMD64) {
            // Need host/native arch → fall back to IsWow64Process2 for nativeMachine
            HMODULE kernel32 = GetModuleHandleW(L"kernel32.dll");
            if (kernel32) {
                typedef BOOL (WINAPI *LPFN_ISWOW64PROCESS2)(HANDLE, USHORT*, USHORT*);
                auto fn = (LPFN_ISWOW64PROCESS2)GetProcAddress(kernel32, "IsWow64Process2");
                if (fn && fn(GetCurrentProcess(), &processMachine, &nativeMachine)) {
                    std::cout << "Native/host machine (IsWow64Process2): 0x"
                              << std::hex << nativeMachine << "\n";
                    return (nativeMachine == IMAGE_FILE_MACHINE_ARM64);
                }
            }
            // If fallback fails, conservatively assume not Prism (native x64 likely)
            return false;
        }

        // Other cases (native ARM64, etc.) → not Prism
        return false;
    }

    // Fallback: IsWow64Process2 (older Windows or if above fails)
    HMODULE kernel32 = GetModuleHandleW(L"kernel32.dll");
    if (!kernel32) return false;

    typedef BOOL (WINAPI *LPFN_ISWOW64PROCESS2)(HANDLE, USHORT*, USHORT*);
    auto fn = (LPFN_ISWOW64PROCESS2)GetProcAddress(kernel32, "IsWow64Process2");
    if (!fn) return false;

    if (!fn(GetCurrentProcess(), &processMachine, &nativeMachine)) return false;

    std::cout << "Process: 0x" << std::hex << processMachine << "\n";
    std::cout << "Native: 0x" << std::hex << nativeMachine << "\n";

    // Prism x64: process=UNKNOWN (0x0), native=ARM64 (0xaa64)
    // Native x64: process=UNKNOWN (0x0), native=AMD64 (0x8664)
    // Classic WOW64 x86: process=0x014c, native=whatever host
    if (processMachine == IMAGE_FILE_MACHINE_UNKNOWN) {
        return (nativeMachine == IMAGE_FILE_MACHINE_ARM64);
    }

    // Any WOW64 process on ARM64 host could be considered "emulated", but for Prism focus → false here
    return false;

#else
    std::cout << "not Windows\n";
    return false;
#endif
}

int main(int argc, char **argv) {

    bool ip = is_prism();

    std::cout << "This program " << argv[0] << " is "
              << (ip ? "" : "not ")
              << "using Microsoft Prism emulation.\n";
    return EXIT_SUCCESS;
}
