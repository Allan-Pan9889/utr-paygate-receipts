"""
Vercel Serverless 入口：将根目录加入 PYTHONPATH 后暴露 Flask `app`。

本地仍使用：python web_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from web_app import app  # noqa: E402
