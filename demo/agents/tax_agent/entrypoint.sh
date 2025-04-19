#!/bin/bash

# Register the agent with the broker
echo "Registering agent with broker..."

curl -X POST http://agent-broker:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "tax-expert",
    "endpoint": "http://tax-agent:8000/agent/run",
    "description": "한국 세법 전문가. 세금 관련 법률 해석, 공제 항목 안내, 부동산 세금 상담 등을 전문으로 합니다.",
    "skills": ["세법 해석", "공제 계산", "부동산 세금 분석", "사업자 등록 상담"]
  }'

# Start the agent service
echo "Starting agent service..."
python -m app.main
