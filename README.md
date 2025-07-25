# voice-rag-assistant

A voice-based AI assistant (EN/TR) with:
- Real-time speech recognition
- Conversational GPT memory
- Wikipedia (RAG) context
- Hallucination control
- Language switching (EN/TR)
- Error logging

## Structure
```
main.py              # Classic loop
main_modular.py      # LangGraph orchestrator
runner.py            # Alternative entry
requirements.txt     # Dependencies
logs/assistant.log
nodes/
  gpt_node.py, rag_node.py, hallucination_node.py, transcribe_node.py, speak_node.py, command_node.py, langchain_rag_node.py, a2a_orchestration.py
orchestration/voice_graph.py
api.py               # FastAPI REST API
```

## Install & Run
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_key
python main.py
```

## Commands
| Command           | Description          |
|-------------------|---------------------|
| help              | List commands       |
| quit / exit       | Exit                |
| reset             | Clear memory        |
| switch to English | Switch to English   |
| switch to Turkish | Switch to Turkish   |

## Requirements
openai, speechrecognition, pyttsx3, gtts, playsound, wikipedia, langgraph, langchain, fastapi, uvicorn  
*(For audio errors: install `pyaudio` or `simpleaudio`.)*

## Flow
Transcribe → Command → [RAG] → GPT → Hallucination → Speak → repeat

## License
MIT © 2024
