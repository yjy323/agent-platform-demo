FROM python:3.11-slim

WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY app/ ./app/

# 포트 노출
EXPOSE 8000

# 실행 명령 수정
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
