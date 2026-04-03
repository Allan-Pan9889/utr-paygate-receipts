"""官网与工具页中英文文案。"""

from __future__ import annotations

from typing import Any

_UI_ZH: dict[str, Any] = {
    "lang": "zh",
    "html_lang": "zh-CN",
    "meta_title": "印度网关支付水单生成器（Excel → PDF）| slip.ink",
    "nav": {
        "brand": "slip.ink",
        "tool": "生成工具",
        "switch_en": "English",
        "switch_zh": "中文",
    },
    "hero": {
        "title": "印度网关支付水单，一键生成专业 PDF",
        "subtitle": "从 Excel 批量导入交易，统一版式、横向 A4、每页 3 张，便于对账与归档。",
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
            {"t": "版式统一", "d": "PayGate 风格水单，横向 A4，每页 3 张。"},
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
                "q": "支持哪些文件格式？",
                "a": "支持 .xlsx、.xls 及表格型 .csv。首行需为英文列名，与说明一致。",
            },
            {
                "q": "数据会上传到哪里？",
                "a": "上传和生成的文件都不会保存在服务器，每次生成完都会立即清理删除。",
            },
            {
                "q": "空着的交易号和时间怎么办？",
                "a": "可在页面配置前缀与随机时间范围，系统将自动生成。",
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
        "pdf_note": "输出为高清 PDF，横向 A4、每页 3 张，可直接打印或归档。",
        "sample": "示例表格：<strong>slip001.xlsx</strong> — 列名与上文一致；请按此模版进行数据填充。",
        "sample_link": "下载 slip001.xlsx",
        "err_no_file": "请选择文件。",
        "err_ext": "仅支持 .xlsx / .xls / .csv。",
        "err_empty": "表格无数据行。",
        "err_txn_prefix": "Transaction No. 前 4 位须为空（使用配置默认值）或恰好 4 位英文字母与数字，不能包含其他字符。",
        "err_generic": "处理失败：",
        "fieldset": "可选配置（Excel 中 Transaction No. 和 Transaction Time 两项数据为空时使用）",
        "gateway": "网关名称（默认 PayGate）",
        "txn_prefix": "Transaction No.",
        "txn_prefix_hint": "（前 4 位配置，可用于区分不同网关，其余 12 位系统会补充随机数字）",
        "txn_prefix_title": "留空则用配置默认；填写时须恰好 4 位英文字母与数字。",
        "time_start": "随机时间起始",
        "time_end": "随机时间结束",
        "submit": "生成 PDF",
        "back_home": "← 返回首页",
        "pdf_busy": "正在生成 PDF…",
        "step1_title": "第一步：选择表格文件",
        "step1_desc": "请上传 .xlsx、.xls 或 .csv；首行需包含要求的英文列名。",
        "step2_title": "第二步：可选配置",
        "step2_desc": "仅当 Excel 中「交易号 / 交易时间」为空时使用；两列均已填写可保持默认。",
        "step3_title": "第三步：生成 PDF",
        "step3_desc": "确认无误后点击按钮，浏览器将下载合并后的水单 PDF。",
        "file_empty": "尚未选择文件",
        "prelude_title": "填写说明",
    },
}

_UI_EN: dict[str, Any] = {
    "lang": "en",
    "html_lang": "en",
    "meta_title": "India Gateway Payment Slip Generator (Excel → PDF) | slip.ink",
    "nav": {
        "brand": "slip.ink",
        "tool": "Generator",
        "switch_en": "English",
        "switch_zh": "中文",
    },
    "hero": {
        "title": "India gateway payment receipts to polished PDFs—in one step",
        "subtitle": "Import transactions from Excel in bulk. Consistent layout, landscape A4, three receipts per page—ready for reconciliation and filing.",
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
            {"t": "Consistent layout", "d": "PayGate-style receipts, landscape A4, three per page."},
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
                "q": "Which file formats are supported?",
                "a": ".xlsx, .xls, and tabular .csv. Row one must use the required English column names.",
            },
            {
                "q": "Where does my upload go? Are files kept on the server?",
                "a": "Uploaded files and generated PDFs are not stored on the server; they are removed immediately after each generation finishes.",
            },
            {
                "q": "What if transaction no. or time is blank?",
                "a": "Set the prefix and random time range on the page; the system will generate values automatically.",
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
        "pdf_note": "Output is a high-resolution PDF, landscape A4, three receipts per page—ready to print or archive.",
        "sample": "Sample spreadsheet: <strong>slip001.xlsx</strong> — headers match the list above; fill in your data using this template.",
        "sample_link": "Download slip001.xlsx",
        "err_no_file": "Please choose a file.",
        "err_ext": "Only .xlsx / .xls / .csv are supported.",
        "err_empty": "No data rows in the sheet.",
        "err_txn_prefix": "Transaction No. prefix must be empty (use config) or exactly 4 letters (A–Z, a–z) or digits (0–9).",
        "err_generic": "Error: ",
        "fieldset": "Optional settings (used when Transaction No. and Transaction Time are empty in Excel)",
        "gateway": "Gateway name (default PayGate)",
        "txn_prefix": "Transaction No.",
        "txn_prefix_hint": "(First 4 characters—use them to distinguish gateways; the system fills the remaining 12 digits with random numbers.)",
        "txn_prefix_title": "Leave blank for the configured default; if set, exactly 4 letters or digits (A–Z, a–z, 0–9).",
        "time_start": "Random time range — start",
        "time_end": "Random time range — end",
        "submit": "Generate PDF",
        "back_home": "← Back to home",
        "pdf_busy": "Generating PDF…",
        "step1_title": "Step 1 — Choose your spreadsheet",
        "step1_desc": "Upload .xlsx, .xls, or .csv with the required English headers in row one.",
        "step2_title": "Step 2 — Optional settings",
        "step2_desc": "Only needed when Transaction No. or Transaction Time is blank; skip if both are filled.",
        "step3_title": "Step 3 — Generate PDF",
        "step3_desc": "Click the button to download the merged receipt PDF.",
        "file_empty": "No file selected yet",
        "prelude_title": "Before you start",
    },
}


def get_ui_strings(lang: str) -> dict[str, Any]:
    if lang == "en":
        return _UI_EN
    return _UI_ZH
