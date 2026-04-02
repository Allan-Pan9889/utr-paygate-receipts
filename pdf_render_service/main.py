"""Railway 上独立部署：HTML → Playwright → PDF（与主项目 html_to_pdf 参数对齐）。"""

from __future__ import annotations

import os

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

app = FastAPI(title="UTR PDF Render")


class RenderBody(BaseModel):
    html: str = Field(..., min_length=1)


def _require_auth(authorization: str | None) -> None:
    secret = os.environ.get("PDF_RENDER_SECRET", "").strip()
    if not secret:
        return
    if (authorization or "").strip() != f"Bearer {secret}":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/render")
def render_pdf(
    body: RenderBody,
    authorization: str | None = Header(default=None),
) -> Response:
    _require_auth(authorization)
    html = body.html

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            launch_args = [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
            ]
            browser = p.chromium.launch(args=launch_args)
            page = browser.new_page()
            page.set_content(html, wait_until="load")
            try:
                page.evaluate("() => document.fonts.ready")
            except Exception:
                pass
            page.wait_for_timeout(700)
            page.emulate_media(media="print")
            pdf_bytes = page.pdf(
                format="A4",
                landscape=True,
                print_background=True,
                margin={"top": "8mm", "right": "8mm", "bottom": "8mm", "left": "8mm"},
                prefer_css_page_size=True,
            )
            browser.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF render failed: {e!s}",
        ) from e

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'inline; filename="receipt.pdf"'},
    )
