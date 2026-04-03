"""官网与工具页中英文文案。"""

from __future__ import annotations

from typing import Any

_UI_ZH: dict[str, Any] = {
    "lang": "zh",
    "html_lang": "zh-CN",
    "meta_title": "印度网关支付水单生成器（Excel → PDF）| PayGate 水单",
    "nav": {
        "brand": "PayGate 水单",
        "tool": "生成工具",
        "switch_en": "English",
        "switch_zh": "中文",
    },
    "hero": {
        "title": "印度网关支付水单，一键生成专业 PDF",
        "subtitle": "从 Excel 批量导入交易，统一版式、横向 A4、每页 6 张，便于对账与归档。",
        "badge": "用浏览器打开即可使用，无需安装插件或本地软件。",
        "cta_tool": "上传 Excel 生成 PDF",
        "cta_sample": "下载示例表 slip001.xlsx",
    },
    "pain": {
        "title": "适用场景",
        "lines": [
            "网关导出数据需要整理成统一格式的水单 PDF",
            "多笔交易希望批量排版，减少手工复制粘贴",
            "团队或代理需要可打印、可留痕的对账凭证",
        ],
    },
    "features": {
        "title": "功能要点",
        "blocks": [
            {"t": "Excel / CSV 导入", "d": "首行英文列名，自动映射常见别名。"},
            {"t": "空字段可自动生成", "d": "Transaction No. / Time 为空时，按配置补全（前缀与随机时间区间）。"},
            {"t": "版式统一", "d": "PayGate 风格水单，横向 A4，每页 6 张。"},
            {"t": "示例模板", "d": "提供 slip001.xlsx 示例，对照列名与格式。"},
        ],
    },
    "steps": {
        "title": "使用步骤",
        "lines": [
            "下载示例表格或按列名准备自己的 Excel",
            "按列名填写收款人、IFSC、账号、金额、交易号、时间、UTR 等字段",
            "可选填写网关名、交易号前缀与时间区间",
            "上传文件，下载合并后的 PDF",
        ],
    },
    "tech": {
        "title": "使用方式",
        "body": "用常见浏览器（Chrome、Safari、Edge、Firefox 等）访问本页，上传 Excel 或 CSV，即可下载 PDF。生成在服务端完成，您无需安装 Chromium、Playwright 或任何额外程序。",
    },
    "pricing": {
        "title": "定价参考（上线后可选）",
        "note": "以下为产品规划参考，正式收费以站内公示为准。",
        "plans": [
            {
                "name": "体验版",
                "price": "免费 / 限额",
                "desc": "适合偶尔使用，每月若干次生成或行数上限。",
            },
            {
                "name": "专业版",
                "price": "¥99–299 / 月",
                "desc": "更高次数或行数，适合小团队与代运营。",
            },
            {
                "name": "企业版",
                "price": "面议",
                "desc": "API、定制版式、私有部署或 SLA 可单独洽谈。",
            },
        ],
    },
    "faq": {
        "title": "常见问题",
        "qa": [
            {
                "q": "我需要在电脑上安装 Chromium 或 Playwright 吗？",
                "a": "不需要。那是运行本服务的服务器端环境，由网站运营方在云端维护。您只需用浏览器打开页面、上传表格即可。若您自行在本机部署开源版本，才需要在服务器上配置浏览器内核，与访客无关。",
            },
            {
                "q": "支持哪些文件格式？",
                "a": "支持 .xlsx、.xls 及表格型 .csv。首行需为英文列名，与说明一致。",
            },
            {
                "q": "数据会上传到哪里？",
                "a": "取决于您部署的服务器。请在隐私政策中说明是否暂存、保留多久；建议在服务端处理完毕后尽快删除临时文件。",
            },
            {
                "q": "空着的交易号和时间怎么办？",
                "a": "可在页面或 config.json 中配置前缀与随机时间范围，系统将自动生成。",
            },
            {
                "q": "生成失败怎么办？",
                "a": "请检查首行列名是否与说明一致、文件是否损坏或过大。若仍失败，可稍后重试或联系支持。",
            },
        ],
    },
    "legal": {
        "title": "合规提示",
        "body": "本工具仅用于将您提供的数据排版为 PDF，不对内容真实性负责。请确保用途合法合规，禁止用于欺诈、洗钱等违法活动。是否满足银行或监管表述，请咨询您的法务或合规部门。",
    },
    "footer": {
        "rights": "保留所有权利。",
        "privacy": "隐私政策与服务条款上线后请在此添加链接。",
    },
    "tool": {
        "page_title": "印度网关支付水单生成器（Excel → PDF）",
        "heading": "印度网关支付水单生成器（Excel → PDF）",
        "intro": "首行需包含：Beneficiary Name, IFSC Code, Account Number, Amount, Transaction No., Transaction Time, UTR Number。",
        "auto": "若上传 Excel 文件中 Transaction No. / Transaction Time 为空，将按下方「可选配置」自动生成。",
        "pdf_note": "输出为高清 PDF，横向 A4、每页 6 张，可直接打印或归档。",
        "sample": "示例表格：<strong>slip001.xlsx</strong> — 列名与上文一致；请按此模版进行数据填充。",
        "sample_link": "下载 slip001.xlsx",
        "err_no_file": "请选择文件。",
        "err_ext": "仅支持 .xlsx / .xls / .csv。",
        "err_empty": "表格无数据行。",
        "err_txn_prefix": "Transaction No. 前 4 位须为空（使用配置默认值）或恰好 4 位英文字母与数字，不能包含其他字符。",
        "err_generic": "处理失败：",
        "fieldset": "可选配置（留空则使用 config.json）",
        "gateway": "网关名称（默认 PayGate）",
        "txn_prefix": "Transaction No.",
        "txn_prefix_hint": "如果 Excel 中未包含该项数据，此处可进行前 4 位配置，用于区分不同网关，其余 12 位系统会补充随机数字。",
        "txn_prefix_title": "留空则用配置默认；填写时须恰好 4 位英文字母与数字。",
        "time_start": "随机时间起始",
        "time_end": "随机时间结束",
        "submit": "生成 PDF",
        "back_home": "← 返回首页",
        "pdf_busy": "正在生成 PDF…",
        "pdf_done": "已下载。本次渲染引擎：",
        "pdf_engine_playwright": "Playwright（HTML 打印，与本地效果一致）",
        "pdf_engine_reportlab": "ReportLab（备用矢量排版）",
        "pdf_detail_label": "详情（排错）：",
        "pdf_engine_unknown": "（未读到 X-PDF-Engine，可能被 CDN/网关去掉响应头）",
    },
}

_UI_EN: dict[str, Any] = {
    "lang": "en",
    "html_lang": "en",
    "meta_title": "India Gateway Payment Slip Generator (Excel → PDF) | PayGate Receipt",
    "nav": {
        "brand": "PayGate Receipt",
        "tool": "Generator",
        "switch_en": "English",
        "switch_zh": "中文",
    },
    "hero": {
        "title": "India gateway payment receipts to polished PDFs—in one step",
        "subtitle": "Import transactions from Excel in bulk. Consistent layout, landscape A4, six receipts per page—ready for reconciliation and filing.",
        "badge": "Use it in your browser—no plugins or local software to install.",
        "cta_tool": "Upload Excel & generate PDF",
        "cta_sample": "Download sample slip001.xlsx",
    },
    "pain": {
        "title": "When it helps",
        "lines": [
            "You need clean receipt PDFs from gateway exports",
            "Many rows should be typeset at once—less copy-paste",
            "Teams or agencies need printable, auditable proofs",
        ],
    },
    "features": {
        "title": "Highlights",
        "blocks": [
            {"t": "Excel / CSV import", "d": "English headers in row one; common aliases are mapped."},
            {"t": "Optional auto-fill", "d": "If Transaction No. / Time is empty, values are generated per config (prefix & time window)."},
            {"t": "Consistent layout", "d": "PayGate-style receipts, landscape A4, six per page."},
            {"t": "Sample file", "d": "slip001.xlsx shows required columns; use it as your template."},
        ],
    },
    "steps": {
        "title": "How it works",
        "lines": [
            "Download the sample or prepare your sheet with the required headers",
            "Fill beneficiary, IFSC, account, amount, transaction no., time, UTR, etc.",
            "Optionally set gateway name, txn prefix, and random time range",
            "Upload and download the merged PDF",
        ],
    },
    "tech": {
        "title": "How you use it",
        "body": "Open this site in a normal browser (Chrome, Safari, Edge, Firefox, etc.), upload your Excel or CSV, and download the PDF. Generation runs on the server—you do not install Chromium, Playwright, or anything else.",
    },
    "pricing": {
        "title": "Pricing (draft)",
        "note": "Indicative tiers; official pricing will be published on the site.",
        "plans": [
            {
                "name": "Starter",
                "price": "Free / limited",
                "desc": "Occasional use with monthly caps on runs or rows.",
            },
            {
                "name": "Pro",
                "price": "US$15–49 / mo (TBD)",
                "desc": "Higher limits for small teams and agencies.",
            },
            {
                "name": "Enterprise",
                "price": "Contact us",
                "desc": "API, custom layout, private deployment, or SLA.",
            },
        ],
    },
    "faq": {
        "title": "FAQ",
        "qa": [
            {
                "q": "Do I need to install Chromium or Playwright on my computer?",
                "a": "No. Those are part of the server environment, maintained by whoever hosts the service. You only need a browser. If you self-host the open-source app, you configure the browser engine on the server—that is separate from end users.",
            },
            {
                "q": "Which file formats are supported?",
                "a": ".xlsx, .xls, and tabular .csv. Row one must use the required English column names.",
            },
            {
                "q": "Where is my data processed?",
                "a": "It depends on your deployment. State retention in your privacy policy; delete temporary files promptly when possible.",
            },
            {
                "q": "What if transaction no. or time is blank?",
                "a": "Configure prefix and random time range in the form or config.json; values will be generated automatically.",
            },
            {
                "q": "PDF generation failed?",
                "a": "Check that row-one headers match the requirements and the file is not corrupted. Retry later or contact support if it persists.",
            },
        ],
    },
    "legal": {
        "title": "Disclaimer",
        "body": "This tool only formats the data you provide into PDFs and does not verify accuracy or legality. You are responsible for lawful use. Consult legal/compliance for bank or regulatory wording.",
    },
    "footer": {
        "rights": "All rights reserved.",
        "privacy": "Add Privacy Policy & Terms links here when available.",
    },
    "tool": {
        "page_title": "India Gateway Payment Slip Generator (Excel → PDF)",
        "heading": "India Gateway Payment Slip Generator (Excel → PDF)",
        "intro": "Row one must include: Beneficiary Name, IFSC Code, Account Number, Amount, Transaction No., Transaction Time, UTR Number.",
        "auto": "If Transaction No. / Transaction Time is empty in the uploaded Excel file, values are generated automatically using the optional settings below.",
        "pdf_note": "Output is a high-resolution PDF, landscape A4, six receipts per page—ready to print or archive.",
        "sample": "Sample spreadsheet: <strong>slip001.xlsx</strong> — headers match the list above; fill in your data using this template.",
        "sample_link": "Download slip001.xlsx",
        "err_no_file": "Please choose a file.",
        "err_ext": "Only .xlsx / .xls / .csv are supported.",
        "err_empty": "No data rows in the sheet.",
        "err_txn_prefix": "Transaction No. prefix must be empty (use config) or exactly 4 letters (A–Z, a–z) or digits (0–9).",
        "err_generic": "Error: ",
        "fieldset": "Optional settings (defaults from config.json if empty)",
        "gateway": "Gateway name (default PayGate)",
        "txn_prefix": "Transaction No.",
        "txn_prefix_hint": "If the Excel file has no value for this field, you can set the first 4 characters here to distinguish gateways; the system fills the remaining 12 digits with random numbers.",
        "txn_prefix_title": "Leave blank for the configured default; if set, exactly 4 letters or digits (A–Z, a–z, 0–9).",
        "time_start": "Random time range — start",
        "time_end": "Random time range — end",
        "submit": "Generate PDF",
        "back_home": "← Back to home",
        "pdf_busy": "Generating PDF…",
        "pdf_done": "Download started. Engine used:",
        "pdf_engine_playwright": "Playwright (HTML print, same as local)",
        "pdf_engine_reportlab": "ReportLab (vector fallback)",
        "pdf_detail_label": "Detail (debug):",
        "pdf_engine_unknown": "(X-PDF-Engine missing; CDN may strip custom headers)",
    },
}


def get_ui_strings(lang: str) -> dict[str, Any]:
    if lang == "en":
        return _UI_EN
    return _UI_ZH
