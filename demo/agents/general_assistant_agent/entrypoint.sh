#!/bin/bash

# Register the agent with the broker
echo "Registering agent with broker..."

curl -X POST http://agent-broker:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "general-assistant",
    "endpoint": "http://general-assistant-agent:8000/agent/run",
    "description": "General purpose AI assistant",
    "skills": ["general_assistance", "conversation", "information_retrieval"]
  }'

# Start the agent service
echo "Starting agent service..."
python -m app.main
