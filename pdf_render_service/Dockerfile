# 与 Playwright 官方镜像版本保持一致（含 Chromium）
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
# Railway 会注入 PORT
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"
