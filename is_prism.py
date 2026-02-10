#!/usr/bin/env python3
# Detects if the current process is running under Prism emulation on Windows on ARM.
# This checks if the process architecture is x86 or x64 while the native machine is ARM64.

import sys
import ctypes

# Define IMAGE_FILE_MACHINE constants
IMAGE_FILE_MACHINE_UNKNOWN = 0x0
IMAGE_FILE_MACHINE_I386 = 0x14C
IMAGE_FILE_MACHINE_AMD64 = 0x8664
IMAGE_FILE_MACHINE_ARM64 = 0xAA64


def is_prism() -> bool:

    if sys.platform != "win32":
        return False

    # Load kernel32 DLL for Windows API
    kernel32 = ctypes.windll.kernel32

    # Create variables for process and native machine types
    process_machine = ctypes.c_ushort(IMAGE_FILE_MACHINE_UNKNOWN)
    native_machine = ctypes.c_ushort(IMAGE_FILE_MACHINE_UNKNOWN)

    # Call IsWow64Process2
    result = kernel32.IsWow64Process2(
        kernel32.GetCurrentProcess(),
        ctypes.byref(process_machine),
        ctypes.byref(native_machine),
    )

    if not result:
        # Failed to query; assume not emulated
        return False

    # Check if process is x86 or x64 and host is ARM64
    return (
        process_machine.value in (IMAGE_FILE_MACHINE_I386, IMAGE_FILE_MACHINE_AMD64)
    ) and native_machine.value == IMAGE_FILE_MACHINE_ARM64


if __name__ == "__main__":

    txt = f"{sys.executable} is "

    if not is_prism():
        txt += "not "

    txt += "using Microsoft Prism emulation."

    print(txt)
