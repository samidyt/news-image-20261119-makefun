#!/usr/bin/env python3
"""news-image-20261119 entry: copy the prepared summary image to /output/entry.png.

The image (entry.png, 1024x1024, under 1 MiB) sums up the world news of
Thursday 19 November 2026 in six panels: the International Court of Justice
ruling that Myanmar committed genocide against the Rohingya, the first-ever
trilateral Trump-Xi-Putin summit in Shenzhen ending in a joint Declaration
toward Peace, tanker attacks escalating in the Strait of Hormuz with an
ADNOC vessel hit and crew injured, Ukrainian strikes on the Kerch Bridge
halting road traffic to Crimea, COP31 climate talks entering their decisive
phase in Antalya, and a Van Gogh painting selling for a record $190.4
million. Runs with no network; deterministic by construction (a byte copy).
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    src = HERE / "entry.png"
    if not src.is_file():
        raise SystemExit(f"missing image next to {__file__}: entry.png")
    # fail fast on a corrupt or non-PNG source instead of copying garbage
    with src.open("rb") as f:
        if f.read(8) != PNG_SIGNATURE:
            raise SystemExit(f"not a valid PNG file: {src}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    # copyfile preserves bytes exactly, so repeated runs are identical
    shutil.copyfile(src, out)
    # catch a partial write (disk full, interrupted copy) instead of
    # silently submitting a truncated image
    if out.stat().st_size != src.stat().st_size:
        raise SystemExit(
            f"copy incomplete: {out} is {out.stat().st_size} bytes, "
            f"expected {src.stat().st_size}"
        )


if __name__ == "__main__":
    main()
