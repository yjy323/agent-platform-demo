# 베이스 이미지
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app/ /app/app/

# 환경 변수 설정
ENV PORT=8000
ENV HOST=0.0.0.0
ENV DEBUG=False
ENV BROKER_BASE_URL=http://agent-broker:8001

# 컨테이너 포트 노출
EXPOSE 8000

# 서비스 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
