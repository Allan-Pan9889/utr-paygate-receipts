"""水单自定义配置：网关名、交易号前缀、时间区间。"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = _ROOT / "config.json"


@dataclass
class AppSettings:
    """与 config.json 字段对应。"""

    gateway_name: str = "PayGate"
    transaction_no_prefix: str = "8691"
    transaction_time_start: str = "2026-01-01 00:00:00"
    transaction_time_end: str = "2026-12-31 23:59:59"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> AppSettings:
        b = cls()
        return cls(
            gateway_name=str(d.get("gateway_name", b.gateway_name)),
            transaction_no_prefix=str(d.get("transaction_no_prefix", b.transaction_no_prefix)),
            transaction_time_start=str(d.get("transaction_time_start", b.transaction_time_start)),
            transaction_time_end=str(d.get("transaction_time_end", b.transaction_time_end)),
        )

    @classmethod
    def load(cls, path: Path | None = None) -> AppSettings:
        p = path or DEFAULT_CONFIG_PATH
        if not p.is_file():
            return cls()
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return cls()
            return cls.from_dict(data)
        except (OSError, json.JSONDecodeError, TypeError):
            return cls()

    def merge_overrides(
        self,
        gateway_name: str | None = None,
        transaction_no_prefix: str | None = None,
        transaction_time_start: str | None = None,
        transaction_time_end: str | None = None,
    ) -> AppSettings:
        """CLI / 表单传入的非空字符串覆盖当前配置。"""
        d = self.to_dict()
        if gateway_name is not None and str(gateway_name).strip() != "":
            d["gateway_name"] = str(gateway_name).strip()
        if transaction_no_prefix is not None and str(transaction_no_prefix).strip() != "":
            d["transaction_no_prefix"] = str(transaction_no_prefix).strip()
        if transaction_time_start is not None and str(transaction_time_start).strip() != "":
            d["transaction_time_start"] = str(transaction_time_start).strip()
        if transaction_time_end is not None and str(transaction_time_end).strip() != "":
            d["transaction_time_end"] = str(transaction_time_end).strip()
        return AppSettings.from_dict(d)
