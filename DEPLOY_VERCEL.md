# 部署说明：Vercel 主站 + Playwright PDF

## 结论（能否走 Playwright？）

| 环境 | Playwright 方式 |
|------|-----------------|
| **本机** | 安装 `requirements-local.txt` 并执行 `playwright install chromium`，进程内 Chromium 打印 PDF。 |
| **Vercel Serverless** | **不能**在函数里打包 Chromium（体积与运行时限制）。 |
| **Vercel + 远程服务** | **可以**：设置环境变量 **`PDF_RENDER_URL`**，指向 Railway（或其它）上部署的 **`pdf_render_service`**，由该服务内 **Playwright** 生成 PDF，效果与本地 HTML 路径一致。 |

未配置 `PDF_RENDER_URL` 时，Vercel 上会走 **ReportLab**（与 HTML 版式接近但非同一引擎）。

---

## 如何确认当前用的是哪种引擎？

下载 PDF 时查看响应头：

- **`X-PDF-Engine`**: `playwright` 或 `reportlab`
- **`X-PDF-Detail`**（可选）: 若未走 Playwright 或发生回退，会给出简短英文说明（例如未配置 URL、远程 HTTP 错误等）。

浏览器：**开发者工具 → Network → 选中 PDF 响应 → Response Headers**。

---

## 1. 在 Railway 部署 Playwright 渲染服务

仓库根目录 **`Dockerfile`** + **`railway.json`** 已配置为仅构建 **`pdf_render_service`**（FastAPI + Playwright 官方镜像）。

1. 在 [Railway](https://railway.app) 新建项目，从本 Git 仓库部署。
2. 确保使用根目录 Dockerfile（与 `railway.json` 一致）。
3. 部署完成后得到公网地址，例如 `https://xxx.up.railway.app`。
4. （推荐）设置 **`PDF_RENDER_SECRET`**（任意强随机字符串）；服务端若配置了该变量，则 **`POST /render`** 要求头：`Authorization: Bearer <同一密钥>`。

健康检查：`GET /health` → `{"status":"ok"}`。

---

## 2. 在 Vercel 配置环境变量

在项目 **Settings → Environment Variables** 添加：

| 变量 | 说明 |
|------|------|
| **`PDF_RENDER_URL`** | Railway 服务根 URL，**不要**带路径末尾的 `/render`（代码会自动拼接 `/render`）。例：`https://xxx.up.railway.app` |
| **`PDF_RENDER_SECRET`** | 与 Railway 上 **`PDF_RENDER_SECRET`** **完全一致**（若 Railway 未设置密钥，则 Vercel 也不要设）。 |

**不要**在 Vercel 设置 `USE_REPORTLAB=1`，否则即使用户配置了 `PDF_RENDER_URL` 也会强制 ReportLab。

重新部署 Vercel 后，再生成 PDF，`X-PDF-Engine` 应为 **`playwright`**。

---

## 3. 超时与套餐

- 远程渲染 + 大 HTML 可能较慢；`html_to_pdf_remote` 使用 **180s** 超时。
- Vercel 需在 **`vercel.json`** 中配置足够 **`maxDuration`**（已示例 60s）；若仍超时，需升级套餐或提高函数时限。
- Railway 侧需保证容器有足够内存（Playwright + Chromium）。

---

## 4. 故障排查

1. **`X-PDF-Engine: reportlab`** 且 **`X-PDF-Detail`** 含 `without PDF_RENDER_URL`  
   → 未配置或拼写错误；检查 Vercel 环境变量是否对 **Production** 生效并已重新部署。

2. **`fallback_after_remote_playwright`** 且含 **`HTTP 401`**  
   → 仅一侧配置了 `PDF_RENDER_SECRET`，或 Bearer 不一致。

3. **`HTTP 502/503` / 连接失败**  
   → Railway 服务未启动、域名错误、或冷启动过慢；访问 `/health` 确认。

4. 本地想强制与线上一致（仅 ReportLab）  
   → `USE_REPORTLAB=1` 或 `PDF_BACKEND=reportlab`。

---

## 5. 其它文件

| 文件 | 作用 |
|------|------|
| `api/index.py` | Vercel Serverless 入口 |
| `vercel.json` | 路由与函数 `maxDuration` |
| `pdf_render_service/main.py` | 远程 `POST /render` 实现 |

本地完整 Playwright：`pip install -r requirements-local.txt && playwright install chromium`。
