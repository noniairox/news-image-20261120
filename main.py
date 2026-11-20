#!/usr/bin/env python3
"""The World Today - 20 November 2026 front page.

The front page is drawn ahead of time and stored in this repository as
entry.png. This program does nothing but copy that file, byte for byte,
into the output directory, so it runs on a bare Python 3.13 with only
the standard library: no third-party packages, no network, no fonts.

The output directory comes from MAKEFUN_OUTPUT_DIR (default /output)
and is created when it does not exist yet.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / "entry.png")


if __name__ == "__main__":
    main()
