# 本地构建：在 pdf_render_service 目录执行 docker build -t utr-pdf .
# Railway 部署请使用仓库根目录的 Dockerfile（构建上下文为整仓）。
# Playwright 官方镜像（含 Chromium）；标签需与 registry 可用版本一致
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
# 仅安装 API 层，避免 pip 升级镜像内已固定的 playwright 与浏览器不一致
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8080
CMD ["sh", "-c", "exec python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
