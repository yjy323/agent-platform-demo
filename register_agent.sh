#!/bin/bash

# 기본값 설정
BROKER_URL="http://localhost:8000"

# 사용법 출력 함수
usage() {
  echo "사용법: $0 -n <에이전트이름> -e <엔드포인트> -d <설명> -s <스킬1,스킬2,...> [-t <타입>] [-u <브로커URL>]"
  echo "  -n: 에이전트 이름 (필수)"
  echo "  -e: 에이전트 엔드포인트 URL (필수)"
  echo "  -d: 에이전트 설명 (필수)"
  echo "  -s: 에이전트 스킬 (쉼표로 구분, 필수)"
  echo "  -t: 에이전트 타입 (기본값: llm)"
  echo "  -u: 브로커 URL (기본값: http://localhost:8000)"
  echo "  -h: 도움말"
  exit 1
}

# 명령줄 인자 파싱
while getopts "n:e:d:s:t:u:h" opt; do
  case $opt in
    n) NAME="$OPTARG" ;;
    e) ENDPOINT="$OPTARG" ;;
    d) DESCRIPTION="$OPTARG" ;;
    s) SKILLS="$OPTARG" ;;
    t) TYPE="$OPTARG" ;;
    u) BROKER_URL="$OPTARG" ;;
    h) usage ;;
    \?) usage ;;
  esac
done

# 필수 인자 확인
if [ -z "$NAME" ] || [ -z "$ENDPOINT" ] || [ -z "$DESCRIPTION" ] || [ -z "$SKILLS" ]; then
  echo "오류: 필수 인자가 누락되었습니다."
  usage
fi

# 타입 기본값 설정
if [ -z "$TYPE" ]; then
  TYPE="llm"
fi

# 스킬 문자열을 JSON 배열로 변환
SKILLS_JSON=$(echo $SKILLS | tr ',' '\n' | jq -R . | jq -s .)

# JSON 페이로드 생성
JSON_DATA=$(cat <<EOF
{
  "name": "$NAME",
  "endpoint": "$ENDPOINT",
  "description": "$DESCRIPTION",
  "skills": $SKILLS_JSON,
  "type": "$TYPE"
}
EOF
)

# API 호출
echo "에이전트 등록 중: $NAME"
echo "요청 데이터: $JSON_DATA"

RESPONSE=$(curl -s -X POST "$BROKER_URL/agents" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA")

# 응답 출력
echo "응답: $RESPONSE"
