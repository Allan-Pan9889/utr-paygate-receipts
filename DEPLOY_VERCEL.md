# 将本项目部署到 Vercel（说明）

## 0. 如何确认线上用的是哪种 PDF？

生成并下载 PDF 时，响应头里会有 **`X-PDF-Engine`**：

- **`reportlab`**：Vercel 上固定使用（Serverless 单包 **≤245MB**，无法同时打包 Python 依赖与 Playwright+Chromium）。
- **`playwright`**：仅本地安装 `requirements-local.txt` 且未强制 ReportLab 时出现。

在浏览器 **开发者工具 → Network** 里选中 `paygate_receipts.pdf`，查看 **Response Headers** 即可。

---

## 1. PDF 生成策略

- **Vercel（`VERCEL=1`）**：代码中固定走 **ReportLab**，与是否设置 `USE_REPORTLAB` 无关（避免超包体上限）。
- **本地**：安装 **`pip install -r requirements-local.txt && playwright install chromium`** 后，默认 **HTML + Playwright**；也可设 **`USE_REPORTLAB=1`** 与线上一致。

## 2. 仓库里已包含的配置

| 文件 | 作用 |
|------|------|
| `api/index.py` | Serverless 入口，暴露 Flask `app` |
| `vercel.json` | 路由重写到 `/api/index`（依赖由 Vercel 默认 `pip install -r requirements.txt`） |
| `runtime.txt` | Python 版本（如 `python3.12`） |
| `.vercelignore` | 排除 `.venv` 等 |
| `requirements-local.txt` | 本地可选：Playwright |

## 3. 部署命令

```bash
npx vercel login
npx vercel --prod
```

绑定自定义域名：项目 → **Settings** → **Domains**。

## 4. 超时与套餐

- 生成 PDF 可能超过 **Hobby 默认 10s** 函数时限。若经常超时，需在 Vercel 中提高 **Function Max Duration**（通常需 **Pro**）。

## 5. 密钥

- 生产环境请用环境变量配置 `FLASK_SECRET_KEY` 等，勿把密钥写进仓库。

## 6. 本地模拟线上

```bash
vercel dev
```

---

**结论**：线上为 **ReportLab** 水单；需要与 HTML 完全一致的效果请在 **本地** 使用 `requirements-local.txt` + Playwright。
