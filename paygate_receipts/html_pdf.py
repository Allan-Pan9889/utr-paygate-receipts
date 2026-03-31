"""HTML 水单 → PDF：本地 Playwright；Vercel 可配置 PDF_RENDER_URL 调 Railway 等同效果；否则 ReportLab。"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any, Literal

from jinja2 import Environment, FileSystemLoader, select_autoescape

from paygate_receipts.receipt_pdf import ReceiptRow
from paygate_receipts.settings import AppSettings

_ROOT = Path(__file__).resolve().parent.parent
_TEMPLATES = _ROOT / "templates"


def _safe_str(v: Any) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    s = str(v).strip()
    return s if s else "—"


def _format_inr_display(amount: Any) -> str:
    """展示为「₹ 49,000」。"""
    if amount is None or (isinstance(amount, float) and math.isnan(amount)):
        return "₹ —"
    try:
        if isinstance(amount, str):
            s = amount.strip().replace(",", "").replace("₹", "").strip()
            if not s:
                return "₹ —"
            n = float(s)
        else:
            n = float(amount)
        return f"₹ {n:,.0f}"
    except (ValueError, TypeError):
        return f"₹ {_safe_str(amount)}"


def _row_to_context(r: ReceiptRow) -> dict[str, Any]:
    return {
        "amount_display": _format_inr_display(r.amount),
        "beneficiary_name": _safe_str(r.beneficiary_name),
        "ifsc_code": _safe_str(r.ifsc_code),
        "account_number": _safe_str(r.account_number),
        "transaction_no": _safe_str(r.transaction_no),
        "transaction_time": _safe_str(r.transaction_time),
        "utr_number": _safe_str(r.utr_number),
    }


def _build_pages(rows: list[ReceiptRow]) -> list[list[dict[str, Any]]]:
    """每页最多 6 条，3×2 格子；不足补空位。"""
    pages: list[list[dict[str, Any]]] = []
    i = 0
    while i < len(rows):
        chunk = rows[i : i + 6]
        page: list[dict[str, Any]] = []
        for j in range(6):
            if j < len(chunk):
                page.append({"row": _row_to_context(chunk[j])})
            else:
                page.append({"row": None})
        pages.append(page)
        i += 6
    return pages


def render_receipt_html(rows: list[ReceiptRow], settings: AppSettings | None = None) -> str:
    s = settings or AppSettings()
    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("receipt_document.html")
    pages = _build_pages(rows)
    return template.render(
        pages=pages,
        gateway_name=s.gateway_name,
        page_title=f"{s.gateway_name} Receipt",
    )


def html_to_pdf(html: str, out_path: str) -> None:
    """使用服务端 Chromium（Playwright）将 HTML 打印为横向 A4 PDF；访客无需安装任何本地组件。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError(
            "无法生成 PDF：服务未就绪，请稍后重试或联系管理员。"
            "（仅在自行部署服务器时需安装：pip install playwright && playwright install chromium）"
        ) from e

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as p:
            # Vercel / 部分无头环境需关闭 sandbox，否则 Chromium 无法启动
            _srv = os.environ.get("VERCEL") == "1" or bool(
                os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
            )
            launch_args = (
                ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
                if _srv
                else []
            )
            browser = p.chromium.launch(args=launch_args)
            page = browser.new_page()
            # 模板已无外网字体/CSS，避免 networkidle 在无外联资源时偶发异常
            page.set_content(html, wait_until="load")
            try:
                page.evaluate("() => document.fonts.ready")
            except Exception:
                pass
            _vercel = os.environ.get("VERCEL") == "1"
            page.wait_for_timeout(1400 if _vercel else 700)
            page.emulate_media(media="print")
            page.pdf(
                path=str(out),
                format="A4",
                landscape=True,
                print_background=True,
                margin={"top": "8mm", "right": "8mm", "bottom": "8mm", "left": "8mm"},
                prefer_css_page_size=True,
            )
            browser.close()
    except Exception as e:
        raise RuntimeError(
            "无法生成 PDF：服务暂时不可用，请稍后重试或联系管理员。"
        ) from e


def html_to_pdf_remote(html: str, out_path: str) -> None:
    """通过独立服务（如 Railway）用 Playwright 生成 PDF，与本地 html_to_pdf 效果一致。"""
    import httpx

    base = os.environ.get("PDF_RENDER_URL", "").strip().rstrip("/")
    if not base:
        raise RuntimeError("PDF_RENDER_URL 未配置")
    url = f"{base}/render" if not base.endswith("/render") else base
    secret = os.environ.get("PDF_RENDER_SECRET", "").strip()
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if secret:
        headers["Authorization"] = f"Bearer {secret}"
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        with httpx.Client(timeout=120.0) as client:
            r = client.post(url, json={"html": html}, headers=headers)
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            raise RuntimeError("远程返回非 PDF 内容")
        out.write_bytes(r.content)
    except httpx.HTTPStatusError as e:
        detail = ""
        try:
            detail = e.response.text[:500]
        except Exception:
            pass
        raise RuntimeError(
            f"远程 PDF 服务失败 HTTP {e.response.status_code} {detail}"
        ) from e
    except Exception as e:
        if isinstance(e, RuntimeError):
            raise
        raise RuntimeError(f"远程 PDF 不可用：{e!s}") from e


def _use_reportlab_backend() -> bool:
    """Vercel 无 PDF_RENDER_URL 时用 ReportLab；配置了远程渲染则走 Playwright（远程）。"""
    u = os.environ.get("USE_REPORTLAB", "").strip().lower()
    if u in ("1", "true", "yes", "on"):
        return True
    if os.environ.get("VERCEL") == "1":
        if os.environ.get("PDF_RENDER_URL", "").strip():
            return False
        return True
    if u in ("0", "false", "no", "off"):
        return False
    v = os.environ.get("PDF_BACKEND", "").strip().lower()
    return v in ("reportlab", "rl")


def build_receipt_pdf(
    path: str,
    rows: list[ReceiptRow],
    settings: AppSettings | None = None,
) -> Literal["playwright", "reportlab"]:
    """本地 Playwright；Vercel 配 PDF_RENDER_URL 则远程 Playwright；否则 ReportLab。返回实际引擎。"""
    if _use_reportlab_backend():
        from paygate_receipts.receipt_pdf import build_multi_page_pdf

        build_multi_page_pdf(path, rows, layout="grid6", settings=settings)
        return "reportlab"
    html = render_receipt_html(rows, settings=settings)
    if os.environ.get("PDF_RENDER_URL", "").strip():
        try:
            html_to_pdf_remote(html, path)
            return "playwright"
        except RuntimeError:
            from paygate_receipts.receipt_pdf import build_multi_page_pdf

            build_multi_page_pdf(path, rows, layout="grid6", settings=settings)
            return "reportlab"
    try:
        import playwright  # noqa: F401
    except ImportError:
        from paygate_receipts.receipt_pdf import build_multi_page_pdf

        build_multi_page_pdf(path, rows, layout="grid6", settings=settings)
        return "reportlab"
    try:
        html_to_pdf(html, path)
        return "playwright"
    except RuntimeError:
        from paygate_receipts.receipt_pdf import build_multi_page_pdf

        build_multi_page_pdf(path, rows, layout="grid6", settings=settings)
        return "reportlab"
