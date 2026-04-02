# Railway：仅用于部署「PDF 渲染」微服务（Playwright + FastAPI）。
# 主站（Flask）部署在 Vercel；构建上下文为仓库根目录。
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY pdf_render_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pdf_render_service/main.py .
EXPOSE 8080
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"
