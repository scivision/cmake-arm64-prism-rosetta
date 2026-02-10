#!/usr/bin/env python3
"""
Python ctypes and system API calls didn't work reliably and didn't discern
the executable types sufficiently to detect Prism.
We found that env vars were simple and reliable.
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
