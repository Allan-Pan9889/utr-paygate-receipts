#!/usr/bin/env python3
"""命令行：Excel → 合并 PDF（横向每页 6 张）。"""

from __future__ import annotations

import argparse
from pathlib import Path

from paygate_receipts.excel_io import load_excel
from paygate_receipts.html_pdf import build_receipt_pdf
from paygate_receipts.row_defaults import apply_row_defaults
from paygate_receipts.settings import AppSettings


def main() -> None:
    ap = argparse.ArgumentParser(
        description="从 Excel 导入交易，使用 HTML+Tailwind 水单模板生成 PDF（横向每页 6 张）。"
    )
    ap.add_argument("excel", type=Path, help="输入 .xlsx 路径")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="输出 PDF 路径（默认同目录下 <excel 基名>_receipts.pdf）",
    )
    ap.add_argument(
        "--config",
        type=Path,
        default=None,
        help="配置文件路径（默认项目根目录 config.json）",
    )
    ap.add_argument("--gateway-name", default=None, help="网关名称（覆盖配置）")
    ap.add_argument(
        "--txn-prefix",
        default=None,
        help="Transaction No. 前 4 位（可字母数字；不足补 0；空则生成的后 12 位为随机数字）",
    )
    ap.add_argument(
        "--time-start",
        default=None,
        help="随机交易时间起始，如 2026-01-01 00:00:00",
    )
    ap.add_argument(
        "--time-end",
        default=None,
        help="随机交易时间结束",
    )
    args = ap.parse_args()

    inp = args.excel.expanduser().resolve()
    out = args.output
    if out is None:
        out = inp.parent / f"{inp.stem}_receipts.pdf"
    else:
        out = out.expanduser().resolve()

    rows = load_excel(inp)
    if not rows:
        raise SystemExit("Excel 无数据行。")

    settings = AppSettings.load(args.config)
    settings = settings.merge_overrides(
        gateway_name=args.gateway_name,
        transaction_no_prefix=args.txn_prefix,
        transaction_time_start=args.time_start,
        transaction_time_end=args.time_end,
    )
    rows = apply_row_defaults(rows, settings)
    engine = build_receipt_pdf(str(out), rows, settings=settings)
    pages = (len(rows) + 5) // 6
    print(
        f"已生成：{out}（共 {len(rows)} 笔；约 {pages} 页；PDF 引擎：{engine}）"
    )


if __name__ == "__main__":
    main()
