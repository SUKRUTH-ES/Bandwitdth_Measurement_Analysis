#!/usr/bin/env python3
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RYU_SRC = PROJECT_ROOT / "vendor" / "ryu-src"

if str(RYU_SRC) not in sys.path:
    sys.path.insert(0, str(RYU_SRC))

os.environ.setdefault("EVENTLET_NO_GREENDNS", "yes")

import setuptools._distutils as setuptools_distutils  # noqa: E402

sys.modules.setdefault("distutils", setuptools_distutils)

from ryu.cmd import manager  # noqa: E402


if __name__ == "__main__":
    manager.main()
