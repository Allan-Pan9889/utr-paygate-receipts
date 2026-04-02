"""注册支持 ₹ 等 Unicode 字符的 TTF 字体。"""

from __future__ import annotations

from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_REGISTERED = False
# 与 pdfmetrics 实际注册一致；避免首次返回 Helvetica、二次误返回 PayGateSans-* 导致 KeyError
_CACHED_NAMES: tuple[str, str, str] | None = None
# True：使用 Helvetica 内置字体，卢比符号以「Rs」代替（无 TTF 时，如部分 Serverless）
_FONT_FALLBACK = False
FONT_REGULAR = "PayGateSans"
FONT_BOLD = "PayGateSans-Bold"
# 单独用于绘制 ₹（U+20B9），优先 DejaVu Sans，避免部分环境下 Arial 粗体缺字显示为方块
FONT_INR = "PayGateINR"


def use_builtin_font_fallback() -> bool:
    return _FONT_FALLBACK


def _bundled_dir() -> Path:
    return Path(__file__).resolve().parent / "bundled_fonts"


def _dejavu_sans_path() -> Path | None:
    for p in (
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/TTF/DejaVuSans.ttf"),
        Path("/Library/Fonts/DejaVuSans.ttf"),
        Path.home() / "Library/Fonts/DejaVuSans.ttf",
    ):
        if p.is_file():
            return p
    try:
        import matplotlib.font_manager as fm

        p = fm.findfont(fm.FontProperties(family="DejaVu Sans"))
        if p and Path(p).is_file() and "DejaVu" in str(p):
            return Path(p)
    except Exception:
        pass
    return None


def _candidates() -> list[Path]:
    roots = [
        Path("/System/Library/Fonts/Supplemental"),
        Path("/Library/Fonts"),
        Path.home() / "Library/Fonts",
    ]
    names_regular = [
        "Arial Unicode.ttf",
        "Arial.ttf",
    ]
    names_bold = ["Arial Bold.ttf", "Arial Unicode.ttf"]
    out: list[Path] = []
    for r in roots:
        for n in names_regular:
            p = r / n
            if p.is_file() and p.suffix.lower() == ".ttf":
                out.append(p)
        for n in names_bold:
            p = r / n
            if p.is_file() and p.suffix.lower() == ".ttf" and p not in out:
                out.append(p)
    # matplotlib 自带的 DejaVu（若已安装）
    try:
        import matplotlib.font_manager as fm

        p = fm.findfont(fm.FontProperties(family="DejaVu Sans"))
        if p and Path(p).is_file() and "DejaVu" in p:
            out.append(Path(p))
        pb = fm.findfont(fm.FontProperties(family="DejaVu Sans", weight="bold"))
        if pb and Path(pb).is_file() and "DejaVu" in pb:
            out.append(Path(pb))
    except Exception:
        pass
    return out


def _try_register_bundled() -> tuple[str, str, str] | None:
    """项目内 bundled_fonts 下的 DejaVu，便于 Vercel 等环境。"""
    d = _bundled_dir()
    reg = d / "DejaVuSans.ttf"
    bold = d / "DejaVuSans-Bold.ttf"
    if not reg.is_file():
        return None
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, str(reg)))
    if bold.is_file():
        pdfmetrics.registerFont(TTFont(FONT_BOLD, str(bold)))
    else:
        pdfmetrics.registerFont(TTFont(FONT_BOLD, str(reg)))
    inr_path = reg
    pdfmetrics.registerFont(TTFont(FONT_INR, str(inr_path)))
    return FONT_REGULAR, FONT_BOLD, FONT_INR


def ensure_fonts() -> tuple[str, str, str]:
    """返回 (常规, 粗体, 卢比符号用) 字体名。"""
    global _REGISTERED, _FONT_FALLBACK, _CACHED_NAMES
    if _REGISTERED and _CACHED_NAMES is not None:
        return _CACHED_NAMES

    bundled = _try_register_bundled()
    if bundled is not None:
        _REGISTERED = True
        _FONT_FALLBACK = False
        _CACHED_NAMES = bundled
        return _CACHED_NAMES

    sup = Path("/System/Library/Fonts/Supplemental")
    regular_path: Path | None = None
    bold_path: Path | None = None
    ar = sup / "Arial.ttf"
    ab = sup / "Arial Bold.ttf"
    if ar.is_file():
        regular_path = ar
    if ab.is_file():
        bold_path = ab

    for p in _candidates():
        if regular_path is None and p.suffix.lower() == ".ttf" and "bold" not in p.name.lower():
            regular_path = p
        if bold_path is None and p.suffix.lower() == ".ttf" and "bold" in p.name.lower():
            bold_path = p

    if regular_path is None:
        for p in _candidates():
            if p.suffix.lower() == ".ttf":
                regular_path = p
                break

    if regular_path is None:
        # Linux 服务器常见路径（部分云镜像含 DejaVu）
        for p in (
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/TTF/DejaVuSans.ttf"),
            Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
        ):
            if p.is_file():
                regular_path = p
                break

    if regular_path is None:
        # 无 TTF：使用 PDF 内置 Helvetica，金额前缀为「Rs」（见 receipt_pdf._fmt_inr_parts）
        _REGISTERED = True
        _FONT_FALLBACK = True
        _CACHED_NAMES = ("Helvetica", "Helvetica-Bold", "Helvetica")
        return _CACHED_NAMES

    pdfmetrics.registerFont(TTFont(FONT_REGULAR, str(regular_path)))

    if bold_path and bold_path.is_file():
        pdfmetrics.registerFont(TTFont(FONT_BOLD, str(bold_path)))
    else:
        # 无粗体文件时复用常规
        pdfmetrics.registerFont(TTFont(FONT_BOLD, str(regular_path)))

    inr_path = _dejavu_sans_path() or regular_path
    pdfmetrics.registerFont(TTFont(FONT_INR, str(inr_path)))

    _REGISTERED = True
    _CACHED_NAMES = (FONT_REGULAR, FONT_BOLD, FONT_INR)
    return _CACHED_NAMES
