FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app/ /app/app/
COPY README.md .

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV PORT=8000

# 컨테이너 실행 시 사용될 명령어
CMD ["echo", "This is a base image. Create a derived image with an agent implementation."]
