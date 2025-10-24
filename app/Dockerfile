# =========================
# Dockerfile (portal)
# 이미지 빌드 명령어 : docker build -t shinwoohipo/portal-flask:1.0.0 .
# 이미지 실행 명령어 : docker run -p 5000:5000 shinwoohipo/portal-flask:1.0.0
# =========================
FROM python:3.10-slim

WORKDIR /app

# 필요 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# Flask 실행 (Gunicorn 사용 권장)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]