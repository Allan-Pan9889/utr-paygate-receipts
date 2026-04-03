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
- 函数 **`maxDuration`** 在 Vercel **项目 Settings → Functions** 中配置（勿在 `vercel.json` 的 `functions` 里写 `api/index.py`，否则构建会报 unmatched pattern）。若生成 PDF 超时，需提高时限或升级套餐。
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
| `vercel.json` | 路由（`rewrites`）；**勿**在 `functions` 里写死 `api/index.py`（Vercel CLI 50+ 会校验失败）。函数时长在 Vercel 项目 **Settings → Functions** 里配置。 |
| `pdf_render_service/main.py` | 远程 `POST /render` 实现 |

本地完整 Playwright：`pip install -r requirements-local.txt && playwright install chromium`。

---

## 6. PayRam 收银台：Railway 跑服务 + Vercel 入口页

架构：**PayRam（Docker）部署在 Railway**；**Vercel 仅提供跳转页** `https://你的域名/payram`，通过环境变量指向 Railway 公网地址。

### 6.1 Vercel

1. 在 **Settings → Environment Variables** 增加：
   - **`PAYRAM_PUBLIC_URL`**：Railway 服务的 **https 根地址**，例如 `https://payram-production-xxxx.up.railway.app`，**不要**末尾斜杠。
2. 保存后 **Redeploy**。
3. 访问 **`/payram`**：若已配置 URL，会显示「打开 PayRam」按钮（新标签页打开 Railway）；未配置则显示设置说明。

### 6.2 Railway（概要）

PayRam 官方安装脚本面向「单机 Docker」，迁到 Railway 时需自行对齐镜像与环境（详见 [PayRam / payram-scripts](https://github.com/PayRam/payram-scripts)）：

1. **新建 Railway 项目** → **Deploy from Docker Hub**（或自定义 Dockerfile），镜像示例：`payramapp/payram`（标签以官方为准，如 `latest` 或脚本中的 `DEFAULT_IMAGE_TAG`）。
2. **HTTP 端口**：安装脚本将应用暴露在容器 **8080**（见脚本中 `--publish 8080:8080`）。在 Railway **Networking** 中为服务生成公网域名，并将入站流量指向容器 **8080**（若 Railway 使用 `PORT`，需确认镜像内进程是否监听该变量；若不监听，请在文档或镜像说明中固定使用 8080）。
3. **持久化**：脚本挂载 `PAYRAM_CORE_DIR`、PostgreSQL 数据目录等；在 Railway 为对应路径配置 **Volume**，避免重启丢数据。
4. **环境变量**（与脚本中 `docker run -e` 一致，按你的环境填写）：`AES_KEY`、`BLOCKCHAIN_NETWORK_TYPE`、`SERVER`、`POSTGRES_HOST`、`POSTGRES_PORT`、`POSTGRES_DATABASE`、`POSTGRES_USERNAME`、`POSTGRES_PASSWORD`、`POSTGRES_SSLMODE`、`SSL_CERT_PATH` 等。数据库可使用 **Railway PostgreSQL** 插件，将内网 host/port/user/password 填入上述变量。
5. **对外 URL**：将 PayRam 内与回调相关的配置（如脚本里的 `PAYMENTS_APP_SERVER_URL`）改为你的 **Railway https 公网地址**，避免仍指向官方示例域。

Railway 部署细节以 PayRam 官方文档与镜像说明为准；若官方后续提供 Compose / Railway 模板，优先跟随官方。

### 6.3 本地脚本参考

仓库内 **`scripts/setup_payram.sh`** 为官方安装脚本副本，便于查阅 `docker run` 参数与默认镜像标签；**生产部署仍以官方仓库为准**。
