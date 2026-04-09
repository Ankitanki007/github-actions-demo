# Stage 1: Build and install dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production runtime image
FROM python:3.12-slim
WORKDIR /app

# Security: non-root user
RUN useradd --create-home appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ ./app/

USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
ENV APP_VERSION=1.0.0

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.main:app"]
