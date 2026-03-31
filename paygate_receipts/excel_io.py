"""从 Excel 读取交易行并映射到 ReceiptRow。"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from typing import Any

import pandas as pd

from paygate_receipts.receipt_pdf import ReceiptRow

# 旧版 Excel 97-2003 二进制头（OLE Compound Document）
_OLE_XLS_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def _try_read_csv(path: Path) -> pd.DataFrame:
    """将误命名为 .xlsx 的 CSV，或真正的 .csv 读成表格。"""
    last_err: Exception | None = None
    for enc in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            df = pd.read_csv(
                path,
                encoding=enc,
                sep=None,
                engine="python",
                dtype=str,
                keep_default_na=False,
            )
            if df.shape[1] >= 1:
                return df
        except Exception as e:
            last_err = e
    raise ValueError(
        "无法按表格解析该文件。请确认：\n"
        "1）用 Excel / WPS「另存为」→「Excel 工作簿 (.xlsx)」（不是网页或 CSV 改扩展名）；\n"
        "2）若数据本身是 CSV，请将文件扩展名改为 .csv 后再上传；\n"
        "3）从网页「导出」的表格若实为 HTML，请先粘贴到 Excel 再另存为 .xlsx。"
    ) from last_err


def _load_dataframe(path: Path) -> pd.DataFrame:
    """支持：标准 .xlsx（ZIP）、旧版 .xls、被误命名的 CSV。"""
    p = path.resolve()
    if p.stat().st_size == 0:
        raise ValueError("文件为空。")

    if zipfile.is_zipfile(p):
        try:
            # 全部按字符串读，避免账号/交易号/UTR 等前导零被当成数字丢失
            return pd.read_excel(
                p,
                engine="openpyxl",
                dtype=str,
                keep_default_na=False,
            )
        except Exception as e:
            err = str(e).lower()
            if "not a zip" in err or "badzipfile" in err:
                raise ValueError(
                    "该文件扩展名是 .xlsx，但内容不是有效的 Excel 工作簿。"
                    "请用 Excel / WPS 打开后「另存为」→「Excel 工作簿 (.xlsx)」。"
                ) from e
            raise ValueError(
                "无法读取该 .xlsx（可能已损坏）。请重新另存为新的 .xlsx 后再试。"
            ) from e

    with p.open("rb") as fh:
        head = fh.read(8)

    if len(head) >= 8 and head == _OLE_XLS_MAGIC:
        try:
            return pd.read_excel(
                p,
                engine="xlrd",
                dtype=str,
                keep_default_na=False,
            )
        except ImportError as e:
            raise ValueError(
                "检测到旧版 .xls，但缺少读取组件。请在本机将文件「另存为」.xlsx 后再上传。"
            ) from e
        except Exception as e:
            raise ValueError(
                "无法读取该 .xls。请在 Excel 中「另存为」→「Excel 工作簿 (.xlsx)」后再上传。"
            ) from e

    return _try_read_csv(p)


def _as_cell(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        if s == "" or s.lower() == "nan":
            return None
        return s
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(v, pd.Timestamp):
        return v.strftime("%Y-%m-%d %H:%M:%S")
    return v


# 允许的列名别名（归一化键 → 可能的表头）
COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "amount": (
        "Amount",
        "amount",
        "金额",
        "AMOUNT",
    ),
    "beneficiary_name": (
        "Beneficiary Name",
        "Beneficiary_Name",
        "beneficiary_name",
        "收款人",
        "Beneficiary",
    ),
    "ifsc_code": (
        "IFSC Code",
        "IFSC_Code",
        "ifsc_code",
        "IFSC",
    ),
    "account_number": (
        "Account Number",
        "Account_Number",
        "account_number",
        "账号",
    ),
    "transaction_no": (
        "Transaction No.",
        "Transaction No",  # Excel 默认常无句点
        "Transaction_No",
        "transaction_no",
        "Txn No",
        "Transaction Number",
    ),
    "transaction_time": (
        "Transaction Time",
        "Transaction_Time",
        "transaction_time",
        "交易时间",
    ),
    "utr_number": (
        "UTR Number",
        "UTR_Number",
        "utr_number",
        "UTR",
    ),
}


def _normalize_header(name: str) -> str:
    s = str(name).strip()
    s = re.sub(r"\s+", " ", s)
    return s


def _header_match_key(name: str) -> str:
    """用于列名匹配：去空白、小写、去掉末尾英文句点（兼容 Transaction No / Transaction No.）。"""
    s = _normalize_header(name).lower()
    s = s.replace("\u00a0", " ").strip()
    return s.rstrip(".")


def _build_lookup(df: pd.DataFrame) -> dict[str, str]:
    """表头 → 归一化键。"""
    inv: dict[str, str] = {}
    for key, aliases in COLUMN_ALIASES.items():
        for a in aliases:
            inv[_header_match_key(a)] = key
    # 直接匹配（不区分大小写）
    col_map: dict[str, str] = {}
    for col in df.columns:
        nk = _header_match_key(str(col))
        if nk in inv:
            col_map[col] = inv[nk]
    return col_map


def _cell(row: pd.Series, col_map: dict[str, str], key: str) -> Any:
    for src, dst in col_map.items():
        if dst == key:
            return row[src]
    return None


def load_excel(path: str | Path) -> list[ReceiptRow]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(str(p))

    df = _load_dataframe(p)
    if df.empty:
        return []

    col_map = _build_lookup(df)
    required = [
        "amount",
        "beneficiary_name",
        "ifsc_code",
        "account_number",
        "transaction_no",
        "transaction_time",
        "utr_number",
    ]
    missing = [k for k in required if not any(dst == k for dst in col_map.values())]
    if missing:
        raise ValueError(
            "Excel 表头缺少必需列（或别名不匹配）："
            + ", ".join(missing)
            + "。请使用首行英文列名，例如：Amount, Beneficiary Name, IFSC Code, "
            "Account Number, Transaction No（或 Transaction No.）, Transaction Time, UTR Number"
        )

    rows: list[ReceiptRow] = []
    for _, row in df.iterrows():
        rows.append(
            ReceiptRow(
                amount=_as_cell(_cell(row, col_map, "amount")),
                beneficiary_name=_as_cell(_cell(row, col_map, "beneficiary_name")),
                ifsc_code=_as_cell(_cell(row, col_map, "ifsc_code")),
                account_number=_as_cell(_cell(row, col_map, "account_number")),
                transaction_no=_as_cell(_cell(row, col_map, "transaction_no")),
                transaction_time=_as_cell(_cell(row, col_map, "transaction_time")),
                utr_number=_as_cell(_cell(row, col_map, "utr_number")),
            )
        )
    return rows
