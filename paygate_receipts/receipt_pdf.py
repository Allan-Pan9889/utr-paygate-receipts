"""水单 PDF：PayGate 风格卡片 + 横向 A4 每页 6 张（3 列 × 2 行）。"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Literal

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen.canvas import Canvas

from paygate_receipts.fonts import ensure_fonts_safe, use_builtin_font_fallback
from paygate_receipts.settings import AppSettings

# PayGate 卡片 / 参考稿配色
COLOR_PAGE_BG = colors.HexColor("#e8eaed")
COLOR_CARD = colors.white
COLOR_SHADOW = colors.Color(0.82, 0.84, 0.86)
COLOR_BRAND = colors.HexColor("#2563eb")
COLOR_TEXT = colors.HexColor("#333333")
COLOR_LABEL = colors.HexColor("#6b7280")
COLOR_SUCCESS = colors.HexColor("#16a34a")
COLOR_LINE = colors.HexColor("#e0e0e0")
COLOR_SECTION_LABEL = colors.HexColor("#9ca3af")
COLOR_FOOTER = colors.HexColor("#666666")
COLOR_PCI = colors.HexColor("#1e7e34")
COLOR_SSL = colors.HexColor("#1565c0")


@dataclass
class ReceiptRow:
    amount: str
    beneficiary_name: str
    ifsc_code: str
    account_number: str
    transaction_no: str
    transaction_time: str
    utr_number: str


def _fmt_inr_parts(amount: Any) -> tuple[str, str]:
    sym = "Rs " if use_builtin_font_fallback() else "₹ "
    if amount is None or (isinstance(amount, float) and math.isnan(amount)):
        return sym, "—"
    try:
        if isinstance(amount, str):
            s = amount.strip().replace(",", "").replace("₹", "").strip()
            if not s:
                return sym, "—"
            n = float(s)
        else:
            n = float(amount)
        return sym, f"{n:,.0f}"
    except (ValueError, TypeError):
        return sym, str(amount).strip()


def _safe_str(v: Any) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    s = str(v).strip()
    return s if s else "—"


def _beneficiary_display(v: Any) -> str:
    """与 HTML 水单一致：收款人姓名展示为大写。"""
    s = _safe_str(v)
    return s.upper() if s != "—" else s


def _draw_amount_scaled(
    c: Canvas,
    cx: float,
    y: float,
    amount: Any,
    fb: str,
    fs: float,
    f_inr: str,
) -> None:
    """金额：₹ 用专用字体（含 U+20B9），数字用粗体。"""
    rupee, num = _fmt_inr_parts(amount)
    c.setFillColor(COLOR_TEXT)
    c.setFont(f_inr, fs)
    wr = c.stringWidth(rupee, f_inr, fs)
    c.setFont(fb, fs)
    wn = c.stringWidth(num, fb, fs)
    x0 = cx - (wr + wn) / 2
    c.setFont(f_inr, fs)
    c.drawString(x0, y, rupee)
    c.setFont(fb, fs)
    c.drawString(x0 + wr, y, num)


def _draw_success_row(
    c: Canvas, cx: float, y_baseline: float, fb: str, amt_fs: float
) -> float:
    """
    圆环对勾 +「Success」，与 HTML 水单一致；图标不向 y 正方向侵入金额区（旧盾牌会叠在 Rs/₹ 上）。
    返回本行占用高度（用于下移游标）。
    """
    fs = max(amt_fs * 0.92, 13.0)
    R = fs * 0.48
    gap = fs * 0.25
    c.setFont(fb, fs)
    tw = c.stringWidth("Success", fb, fs)
    group_w = 2 * R + gap + tw
    icon_cx = cx - group_w / 2 + R
    cy = y_baseline + fs * 0.32

    c.saveState()
    c.setStrokeColor(COLOR_SUCCESS)
    c.setLineWidth(max(1.15, fs * 0.11))
    c.circle(icon_cx, cy, R, stroke=1, fill=0)

    # 圆内对勾（与 HTML SVG 视觉接近）
    c.setLineCap(1)
    c.setLineJoin(1)
    c.setLineWidth(max(1.05, fs * 0.095))
    ck = R * 0.42
    x1 = icon_cx - ck * 0.55
    y1 = cy - ck * 0.08
    x2 = icon_cx - ck * 0.08
    y2 = cy - ck * 0.52
    x3 = icon_cx + ck * 0.85
    y3 = cy + ck * 0.48
    p = c.beginPath()
    p.moveTo(x1, y1)
    p.lineTo(x2, y2)
    p.lineTo(x3, y3)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()

    c.setFont(fb, fs)
    c.setFillColor(COLOR_SUCCESS)
    tx = icon_cx + R + gap
    c.drawString(tx, y_baseline, "Success")
    return max(2.1 * R + fs * 0.15, fs + 6.0)


def _divider_title(
    c: Canvas,
    cx: float,
    y_baseline: float,
    x_left: float,
    x_right: float,
    title: str,
    font: str,
    fs: float,
) -> None:
    """中间被标题打断的细横线；横线与标题基线对齐，避免与上下行重叠。"""
    tw = c.stringWidth(title, font, fs)
    gap = max(5.0, fs * 0.45)
    # 细线略低于标题大写字母的中线，视觉更稳
    y_line = y_baseline + fs * 0.28
    c.setStrokeColor(COLOR_LINE)
    c.setLineWidth(0.45)
    c.line(x_left, y_line, cx - tw / 2 - gap, y_line)
    c.line(cx + tw / 2 + gap, y_line, x_right, y_line)
    c.setFillColor(COLOR_SECTION_LABEL)
    c.setFont(font, fs)
    c.drawString(cx - tw / 2, y_baseline, title)


def draw_noahpay_slip(
    c: Canvas,
    row: ReceiptRow,
    x0: float,
    y0: float,
    w: float,
    h: float,
    fr: str,
    fb: str,
    f_inr: str,
    brand_name: str = "PayGate",
) -> None:
    """
    在矩形 (x0, y0, w, h) 内绘制 PayGate 风格水单（y0 为底边）。
    """
    top = y0 + h
    rr = min(14.0, w * 0.045)
    pad = max(8.0, w * 0.055)
    cx = x0 + w / 2
    scale = min(w, h) / 268.0

    # 轻阴影（略偏移的圆角矩形）
    c.saveState()
    c.setFillColor(COLOR_SHADOW)
    p_sh = c.beginPath()
    p_sh.roundRect(x0 + 1.8, y0 - 1.2, w, h, rr)
    c.drawPath(p_sh, stroke=0, fill=1)
    c.restoreState()

    # 白卡片
    c.saveState()
    p_card = c.beginPath()
    p_card.roundRect(x0, y0, w, h, rr)
    c.setFillColor(COLOR_CARD)
    c.drawPath(p_card, stroke=0, fill=1)
    c.restoreState()

    xl = x0 + pad
    xr = x0 + w - pad

    # cur = 从卡片顶边向下的累计距离（越大越靠下），用 top - cur 得到各元素基线 y
    cur = pad + 8 * scale

    brand_fs = max(11.0, 12.5 * scale)
    c.setFont(fb, brand_fs)
    c.setFillColor(COLOR_BRAND)
    c.drawCentredString(cx, top - cur, brand_name)
    # 原钥匙行已去掉，略留间距再接金额
    cur += brand_fs + 8 * scale

    amt_fs = max(13.0, 15.5 * scale)
    y_amt = top - cur
    _draw_amount_scaled(c, cx, y_amt, row.amount, fb, amt_fs, f_inr)
    # 金额与 Success 之间留出足够垂直距离，避免状态图标与数字重叠
    cur += amt_fs + max(11.0, 13.0 * scale)

    row_h = _draw_success_row(c, cx, top - cur, fb, amt_fs)
    cur += row_h + 10 * scale

    sec_fs = max(6.0, 6.8 * scale)
    row_fs = max(5.8, 6.4 * scale)
    lh = max(9.0, 9.8 * scale)

    _divider_title(
        c, cx, top - cur, xl, xr, "BENEFICIARY DETAILS", fb, sec_fs
    )
    cur += sec_fs + 5 * scale

    for label, val in (
        ("Beneficiary Name", _beneficiary_display(row.beneficiary_name)),
        ("IFSC Code", _safe_str(row.ifsc_code)),
        ("Account Number", _safe_str(row.account_number)),
    ):
        c.setFont(fr, row_fs)
        c.setFillColor(COLOR_LABEL)
        c.drawString(xl, top - cur, label)
        c.setFont(fb, row_fs)
        c.setFillColor(COLOR_TEXT)
        tw = c.stringWidth(val, fb, row_fs)
        c.drawString(xr - tw, top - cur, val)
        cur += lh

    cur += 5 * scale
    _divider_title(
        c, cx, top - cur, xl, xr, "TRANSACTION PARTICULARS", fb, sec_fs
    )
    cur += sec_fs + 5 * scale

    for label, val in (
        ("Transaction No.", _safe_str(row.transaction_no)),
        ("Transaction Time", _safe_str(row.transaction_time)),
        ("UTR Number", _safe_str(row.utr_number)),
    ):
        c.setFont(fr, row_fs)
        c.setFillColor(COLOR_LABEL)
        c.drawString(xl, top - cur, label)
        c.setFont(fb, row_fs)
        c.setFillColor(COLOR_TEXT)
        tw = c.stringWidth(val, fb, row_fs)
        c.drawString(xr - tw, top - cur, val)
        cur += lh

    # 页脚：固定在卡片底部区域，避免与正文重叠
    foot_fs = max(4.2, 4.8 * scale)
    fy = y0 + 11
    c.setFont(fr, foot_fs)
    c.setFillColor(COLOR_PCI)
    c.rect(xl, fy, 21, 9, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont(fb, foot_fs)
    c.drawString(xl + 3, fy + 1.8, "PCI")
    c.setStrokeColor(COLOR_SSL)
    c.setLineWidth(0.5)
    lx2 = xl + 26
    c.rect(lx2, fy + 1, 5, 6.5, stroke=1, fill=0)
    c.line(lx2 + 2.5, fy + 7.5, lx2 + 2.5, fy + 9)
    c.setFillColor(COLOR_SSL)
    c.setFont(fr, foot_fs)
    c.drawString(lx2 + 8, fy + 1.2, "256 bit SSL")

    c.setFillColor(COLOR_FOOTER)
    c.setFont(fr, foot_fs)
    t1 = "* This is an electronically generated secure receipt."
    t2 = "  Verify with your banking statement."
    t3 = f"* Generated via {brand_name} India Ltd."
    for i, t in enumerate((t1, t2, t3)):
        tw = c.stringWidth(t, fr, foot_fs)
        c.drawString(xr - tw, fy + 22 - i * (foot_fs + 0.6), t)


def _landscape_grid_geometry() -> tuple[float, float, float, float, float, float]:
    """返回 (page_w, page_h, slip_w, slip_h, margin, gutter)。"""
    W, H = landscape(A4)
    margin = 16.0
    gutter = 10.0
    usable_w = W - 2 * margin
    usable_h = H - 2 * margin
    slip_w = (usable_w - 2 * gutter) / 3.0
    slip_h = (usable_h - gutter) / 2.0
    return W, H, slip_w, slip_h, margin, gutter


def build_multi_page_pdf(
    path: str,
    rows: list[ReceiptRow],
    layout: Literal["grid6", "single"] = "grid6",
    settings: AppSettings | None = None,
) -> None:
    """
    layout:
      - grid6: 横向 A4，每页 3×2=6 张 PayGate 水单
      - single: 纵向 A4，每页 1 张（放大卡片）
    """
    s = settings or AppSettings()
    brand = (s.gateway_name or "PayGate").strip() or "PayGate"
    fr, fb, f_inr = ensure_fonts_safe()

    if layout == "grid6":
        W, H, slip_w, slip_h, margin, gutter = _landscape_grid_geometry()
        c = Canvas(path, pagesize=(W, H))
        idx = 0
        while idx < len(rows):
            c.saveState()
            c.setFillColor(COLOR_PAGE_BG)
            c.rect(0, 0, W, H, stroke=0, fill=1)
            c.restoreState()
            for slot in range(6):
                if idx >= len(rows):
                    break
                row_i = slot // 3
                col_i = slot % 3
                sx = margin + col_i * (slip_w + gutter)
                sy = margin + row_i * (slip_h + gutter)
                draw_noahpay_slip(
                    c, rows[idx], sx, sy, slip_w, slip_h, fr, fb, f_inr, brand_name=brand
                )
                idx += 1
            if idx < len(rows):
                c.showPage()
        c.save()
        return

    # single: portrait one card per page
    W, H = A4
    m = 56.0
    cw = W - 2 * m
    ch = H - 2 * m
    c = Canvas(path, pagesize=A4)
    for i, row in enumerate(rows):
        c.saveState()
        c.setFillColor(COLOR_PAGE_BG)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        c.restoreState()
        draw_noahpay_slip(c, row, m, m, cw, ch, fr, fb, f_inr, brand_name=brand)
        if i < len(rows) - 1:
            c.showPage()
    c.save()
