FROM agent-base:latest

WORKDIR /app

# 추가 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 에이전트 코드 복사
COPY app/ /app/app/
COPY README.md .

# 환경 변수 설정
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# 서비스 시작
CMD ["python", "-m", "app.main"]
