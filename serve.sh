#!/bin/bash

# Load .env file (if exists)
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Export extra env variables if needed (e.g., tracing/logging)
export LANGCHAIN_TRACING_V2=true

# Start backend with Uvicorn (main_modular.py or api.py)
# Example: for FastAPI
if [ -f api.py ]; then
    uvicorn api:app --host 0.0.0.0 --port 8000 --reload
# Or for LangGraph orchestrator (e.g. runner.py or main_modular.py)
elif [ -f main_modular.py ]; then
    python main_modular.py
# Classic main.py
elif [ -f main.py ]; then
    python main.py
else
    echo "No app found to start!"
    exit 1
fi
