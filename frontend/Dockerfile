FROM python:3.11-slim

WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY app.py .

# 환경 변수 설정
ENV API_URL=http://backend:8000

# 포트 노출
EXPOSE 8501

# Streamlit 실행 옵션 설정
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 실행 명령을 명확히 지정
CMD ["streamlit", "run", "app.py"]
