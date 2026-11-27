#!/usr/bin/env python3
"""Entrypoint for the news-image-20261127 entry.

Copies the front page drawn for Friday 27 November 2026 (entry.png,
which sits beside this file) into the grader's output directory.
Standard library only, no network, fully deterministic: the same
input file always produces the same output bytes.
"""

import os
import shutil
import sys

SOURCE = "entry.png"
TARGET = "entry.png"
OUTPUT_VAR = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT = "/output"


def output_dir():
    """Directory the grader wants entry.png in."""
    return os.environ.get(OUTPUT_VAR, DEFAULT_OUTPUT)


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SOURCE)
    dest = os.path.join(output_dir(), TARGET)
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    shutil.copyfile(src, dest)
    # Confirm the copy landed whole: same byte count as the source.
    if os.path.getsize(dest) != os.path.getsize(src):
        raise SystemExit("entry.png copy is incomplete")


if __name__ == "__main__":
    run()
    sys.exit(0)
