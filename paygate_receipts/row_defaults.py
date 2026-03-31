"""当 Excel 中 Transaction No. / Transaction Time 为空时，按配置生成。"""

from __future__ import annotations

import math
import random
import re
import secrets
from datetime import datetime, timedelta
from typing import Any

from paygate_receipts.receipt_pdf import ReceiptRow
from paygate_receipts.settings import AppSettings

def _is_blank(v: Any) -> bool:
    if v is None:
        return True
    try:
        if isinstance(v, float) and math.isnan(v):
            return True
    except (TypeError, ValueError):
        pass
    s = str(v).strip()
    return s == "" or s.lower() == "nan"


def normalize_prefix(prefix: str) -> str:
    """取前 4 位可配置字符（字母数字），不足右侧用 0 补齐。"""
    raw = re.sub(r"[^A-Za-z0-9]", "", (prefix or ""))[:4].upper()
    if len(raw) >= 4:
        return raw[:4]
    return (raw + "0000")[:4]


def generate_transaction_no(prefix: str) -> str:
    """16 位：前 4 位来自配置，后 12 位为随机数字（0–9）。"""
    head = normalize_prefix(prefix)
    tail = f"{secrets.randbelow(10**12):012d}"
    return head + tail


def _parse_dt(s: str) -> datetime:
    s = (s or "").strip()
    if not s:
        raise ValueError("empty datetime")
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
    ):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    try:
        t = s.replace("Z", "").split("+")[0].strip()
        if "T" in t:
            return datetime.fromisoformat(t)
    except ValueError:
        pass
    raise ValueError(f"无法解析时间：{s!r}")


def random_time_string(start: datetime, end: datetime) -> str:
    if end <= start:
        end = start + timedelta(days=1)
    delta = (end - start).total_seconds()
    sec = random.uniform(0, delta)
    t = start + timedelta(seconds=sec)
    return t.strftime("%Y-%m-%d %H:%M:%S")


def apply_row_defaults(rows: list[ReceiptRow], settings: AppSettings) -> list[ReceiptRow]:
    """
    若某行的 Transaction No. 或 Transaction Time 在 Excel 中为空，则按配置生成。
    已有非空值则原样保留。
    """
    try:
        t0 = _parse_dt(settings.transaction_time_start)
        t1 = _parse_dt(settings.transaction_time_end)
    except (ValueError, OSError):
        t0 = datetime(2026, 1, 1, 0, 0, 0)
        t1 = datetime(2026, 12, 31, 23, 59, 59)

    out: list[ReceiptRow] = []
    for r in rows:
        txn_no = r.transaction_no
        if _is_blank(txn_no):
            txn_no = generate_transaction_no(settings.transaction_no_prefix)

        txn_time = r.transaction_time
        if _is_blank(txn_time):
            txn_time = random_time_string(t0, t1)

        out.append(
            ReceiptRow(
                amount=r.amount,
                beneficiary_name=r.beneficiary_name,
                ifsc_code=r.ifsc_code,
                account_number=r.account_number,
                transaction_no=txn_no,
                transaction_time=txn_time,
                utr_number=r.utr_number,
            )
        )
    return out
