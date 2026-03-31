#!/usr/bin/env python3
"""下载 DejaVu 字体到 paygate_receipts/bundled_fonts（供 Vercel 等无系统字体环境使用）。"""

from __future__ import annotations

import ssl
import urllib.request
from pathlib import Path

import certifi

_URLS = (
    (
        "DejaVuSans.ttf",
        "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf",
    ),
    (
        "DejaVuSans-Bold.ttf",
        "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans-Bold.ttf",
    ),
)


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    dest_dir = root / "paygate_receipts" / "bundled_fonts"
    dest_dir.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context(cafile=certifi.where())
    for name, url in _URLS:
        out = dest_dir / name
        if out.is_file() and out.stat().st_size > 10000:
            print("skip existing", out)
            continue
        print("fetch", url)
        req = urllib.request.Request(url, headers={"User-Agent": "UTR-font-fetch/1.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
            out.write_bytes(r.read())
        print("wrote", out, out.stat().st_size)


if __name__ == "__main__":
    main()
