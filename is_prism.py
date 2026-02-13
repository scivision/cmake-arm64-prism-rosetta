#!/usr/bin/env python3
"""
Detecting CPU arch on Windows is non-trivial.
We use function windows_detect_native_arch() from mesonbuild (Apache 2.0 license).
"""

import os
import sys
import platform


def windows_detect_native_arch() -> str:
    # adapted from mesonbuild/meson/utils/universal.py L723ff commit 4e9ba3d
    """
    The architecture of Windows itself: x86, amd64 or arm64
    """

    av = {0x8664: "amd64", 0x014C: "x86", 0xAA64: "arm64", 0x01C4: "arm"}

    if sys.platform != "win32":
        return ""
    try:
        import ctypes

        process_arch = ctypes.c_ushort()
        native_arch = ctypes.c_ushort()
        kernel32 = ctypes.windll.kernel32
        process = ctypes.c_void_p(kernel32.GetCurrentProcess())
        # This is the only reliable way to detect an arm system if we are an x86/x64 process being emulated
        if kernel32.IsWow64Process2(
            process, ctypes.byref(process_arch), ctypes.byref(native_arch)
        ):
            # https://docs.microsoft.com/en-us/windows/win32/sysinfo/image-file-machine-constants
            return av[native_arch.value]
    except (OSError, AttributeError, KeyError):
        pass
    # These env variables are always available. See:
    # https://msdn.microsoft.com/en-us/library/aa384274(VS.85).aspx
    # https://blogs.msdn.microsoft.com/david.wang/2006/03/27/howto-detect-process-bitness/
    arch = os.environ.get("PROCESSOR_ARCHITEW6432", "").lower()
    if not arch:
        try:
            # If this doesn't exist, something is messing with the environment
            arch = os.environ["PROCESSOR_ARCHITECTURE"].lower()
        except KeyError:
            raise EnvironmentError("Unable to detect native OS architecture")

    return arch


def is_prism() -> bool:
    """Return True if running under Microsoft Prism emulation (x64 on ARM64).

    For example, with MSYS2 python
    UCRT64
    C:/msys64/ucrt64/bin/python.exe is using Microsoft Prism emulation.
    sys.platform → win32
    sys.executable → C:/msys64/ucrt64/bin/python.exe
    platform.architecture() → ('64bit', 'WindowsPE')
    platform.machine() → AMD64
    platform.processor() → ARMv8 (64-bit) Family 8 Model 1 Revision 201, Qualcomm Technologies Inc
    platform.uname() → uname_result(system='Windows', node='sl7', release='11', version='10.0.26200', machine='AMD64')
    os.environ.get('PROCESSOR_ARCHITECTURE') → AMD64
    os.environ.get('PROCESSOR_ARCHITEW6432') → None


    CLANGARM64:
    C:/msys64/clangarm64/bin/python.exe is not using Microsoft Prism emulation.
    sys.platform → win32
    sys.executable → C:/msys64/clangarm64/bin/python.exe
    platform.architecture() → ('64bit', 'WindowsPE')
    platform.machine() → ARM64
    platform.processor() → ARMv8 (64-bit) Family 8 Model 1 Revision 201, Qualcomm Technologies Inc
    platform.uname() → uname_result(system='Windows', node='sl7', release='11', version='10.0.26200', machine='ARM64')
    os.environ.get('PROCESSOR_ARCHITECTURE') → ARM64
    os.environ.get('PROCESSOR_ARCHITEW6432') → None
    """

    if os.name != "nt":
        return False

    if platform.machine().lower() not in ("amd64", "x86"):
        # If we're not running on x86/x64, we can't be emulated
        return False

    return windows_detect_native_arch() in ("arm64", "arm")


if __name__ == "__main__":
    exe = sys.executable
    status = "" if is_prism() else "not "
    print(f"{exe} is {status}using Microsoft Prism emulation.")
    print()
    print(f"sys.platform → {sys.platform}")
    print(f"sys.executable → {sys.executable}")
    print(f"platform.architecture() → {platform.architecture()}")
    print(f"platform.machine() → {platform.machine()}")
    print(f"platform.processor() → {platform.processor()}")
    print(f"platform.uname() → {platform.uname()}")
    print(
        f"os.environ.get('PROCESSOR_ARCHITECTURE') → {os.environ.get('PROCESSOR_ARCHITECTURE')}"
    )
    print(
        f"os.environ.get('PROCESSOR_ARCHITEW6432') → {os.environ.get('PROCESSOR_ARCHITEW6432')}"
    )
