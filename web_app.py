#!/usr/bin/env python3
"""Web：官网（中英）+ Excel 上传生成 PDF。"""

from __future__ import annotations

import re
import tempfile
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from flask import (
    Flask,
    abort,
    make_response,
    render_template,
    request,
    send_file,
    send_from_directory,
)

from paygate_receipts.excel_io import load_excel
from paygate_receipts.html_pdf import build_receipt_pdf
from paygate_receipts.row_defaults import apply_row_defaults
from paygate_receipts.settings import AppSettings
from paygate_receipts.web_translations import get_ui_strings

_ROOT = Path(__file__).resolve().parent
SAMPLE_XLSX = "UTR001.xlsx"

app = Flask(__name__)
app.secret_key = "paygate-receipt-dev-key-change-in-production"


def resolve_lang() -> str:
    q = request.args.get("lang")
    if q in ("zh", "en"):
        return q
    c = request.cookies.get("ui_lang")
    if c in ("zh", "en"):
        return c
    return "zh"


def _default_time_range_strings() -> tuple[str, str]:
    """随机时间默认：起始 = 当前时间 2 小时前，结束 = 当前时间。"""
    now = datetime.now().replace(microsecond=0)
    start = now - timedelta(hours=2)
    return start.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")


def _set_lang_cookie(resp: object) -> None:
    if request.args.get("lang") in ("zh", "en"):
        resp.set_cookie(  # type: ignore[attr-defined]
            "ui_lang",
            request.args["lang"],
            max_age=365 * 24 * 3600,
            samesite="Lax",
            path="/",
        )


@app.route("/", methods=["GET"])
def landing():
    lang = resolve_lang()
    t = get_ui_strings(lang)
    resp = make_response(render_template("landing.html", t=t, lang=lang))
    _set_lang_cookie(resp)
    return resp


@app.route("/app", methods=["GET", "POST"])
def tool():
    lang = resolve_lang()
    t = get_ui_strings(lang)
    err: str | None = None
    ds, de = _default_time_range_strings()

    if request.method == "POST":
        form_gateway = request.form.get("gateway_name") or ""
        form_txn_prefix = (request.form.get("txn_prefix") or "").strip()
        form_time_start = request.form.get("time_start", "")
        form_time_end = request.form.get("time_end", "")
    else:
        form_gateway = ""
        form_txn_prefix = ""
        form_time_start = ds
        form_time_end = de

    if request.method == "POST":
        f = request.files.get("file")
        if not f or not f.filename:
            err = t["tool"]["err_no_file"]
        elif not f.filename.lower().endswith((".xlsx", ".xls", ".csv")):
            err = t["tool"]["err_ext"]
        elif form_txn_prefix and not re.fullmatch(r"[A-Za-z0-9]{4}", form_txn_prefix):
            err = t["tool"]["err_txn_prefix"]
        else:
            try:
                with tempfile.TemporaryDirectory() as td:
                    src = Path(td) / f.filename
                    f.save(src)
                    rows = load_excel(src)
                    if not rows:
                        err = t["tool"]["err_empty"]
                    else:
                        out = Path(td) / f"receipts_{uuid.uuid4().hex}.pdf"
                        settings = AppSettings.load()
                        settings = settings.merge_overrides(
                            gateway_name=request.form.get("gateway_name"),
                            transaction_no_prefix=request.form.get("txn_prefix"),
                            transaction_time_start=request.form.get("time_start"),
                            transaction_time_end=request.form.get("time_end"),
                        )
                        rows = apply_row_defaults(rows, settings)
                        pdf_engine = build_receipt_pdf(
                            str(out), rows, settings=settings
                        )
                        resp = send_file(
                            out,
                            as_attachment=True,
                            download_name="paygate_receipts.pdf",
                            mimetype="application/pdf",
                        )
                        resp.headers["X-PDF-Engine"] = pdf_engine
                        return resp
            except ValueError as e:
                err = str(e)
            except Exception as e:
                err = f"{t['tool']['err_generic']}{e}"

    resp = make_response(
        render_template(
            "tool.html",
            t=t,
            lang=lang,
            error=err,
            form_gateway=form_gateway,
            form_txn_prefix=form_txn_prefix,
            form_time_start=form_time_start,
            form_time_end=form_time_end,
        )
    )
    _set_lang_cookie(resp)
    return resp


@app.route(f"/sample/{SAMPLE_XLSX}")
def download_sample():
    p = _ROOT / SAMPLE_XLSX
    if not p.is_file():
        abort(404)
    return send_from_directory(
        str(_ROOT),
        SAMPLE_XLSX,
        as_attachment=True,
        download_name=SAMPLE_XLSX,
    )


def main() -> None:
    app.run(host="127.0.0.1", port=5050, debug=False)


if __name__ == "__main__":
    main()
