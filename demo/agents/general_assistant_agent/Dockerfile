FROM agent-base:latest

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 에이전트 코드 복사
COPY app/ /app/app/
COPY entrypoint.sh .
COPY README.md .

# 환경 변수 설정
ENV PORT=8000
ENV PYTHONUNBUFFERED=1
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
