#!/usr/bin/env python3
"""
Python ctypes and system API calls didn't work reliably and didn't discern
the executable types sufficiently to detect Prism.
We found that env vars were simple and reliable.

For example, with MSYS2 python
UCRT64:

sys.platform → win32
sys.executable → C:/msys64/ucrt64/bin/python.exe
platform.architecture() → ('64bit', 'WindowsPE')
platform.machine() → ARM64
platform.processor() → ARMv8 (64-bit) Family 8 Model 0 Revision   0, QEMU
platform.uname() → uname_result(system='Windows', node='', release='11', version='10.0.26200', machine='ARM64')
os.environ.get('PROCESSOR_ARCHITECTURE') → AMD64
os.environ.get('PROCESSOR_ARCHITEW6432') → None
GetCurrentProcess() handle → -1
Direct IsWow64Process2 success? → 0
  GetLastError → 6

CLANGARM64:
sys.platform → win32
sys.executable → C:/msys64/clangarm64/bin/python.exe
platform.architecture() → ('64bit', 'WindowsPE')
platform.machine() → ARM64
platform.processor() → ARMv8 (64-bit) Family 8 Model 0 Revision   0, QEMU
platform.uname() → uname_result(system='Windows', node='', release='11', version='10.0.26200', machine='ARM64')
os.environ.get('PROCESSOR_ARCHITECTURE') → ARM64
os.environ.get('PROCESSOR_ARCHITEW6432') → None
GetCurrentProcess() handle → -1
Direct IsWow64Process2 success? → 1
  process machine → 0x0
  native machine  → 0xaa64
"""

import os
import sys
import platform


def is_prism() -> bool:
    """Return True if running under Microsoft Prism emulation (x64 on ARM64)."""
    # PROCESSOR_ARCHITECTURE    = effective process arch
    # PROCESSOR_ARCHITEW6432    = native arch when running 32-bit on 64-bit (WOW64)
    # Under Prism x64 → effective = AMD64, native = ARM64 → PROCESSOR_ARCHITECTURE = AMD64
    # Native ARM64   → PROCESSOR_ARCHITECTURE = ARM64

    if os.name != "nt" or platform.machine().upper() != "ARM64":
        return False

    arch = os.environ.get("PROCESSOR_ARCHITECTURE", "").upper()
    arch_wow64 = os.environ.get("PROCESSOR_ARCHITEW6432", "").upper()
    effective_arch = arch_wow64 or arch
    return effective_arch == "AMD64"


if __name__ == "__main__":
    exe = sys.executable
    status = "" if is_prism() else "not "
    print(f"{exe} is {status}using Microsoft Prism emulation.")
