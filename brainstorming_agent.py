import requests
from memory_manager import get_all_memories

OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
BRAIN_MODEL = "gemma4:e4b"

def get_memory_context():
    memories = get_all_memories(limit=5)
    if not memories:
        return ""
    memory_str = "\n".join([f"- User asked: {q}\n  Saved Answer: {a}" for q, a in memories])
    return f"\n\nHere are some past approved memories and context from your JSON files:\n{memory_str}"

def get_standard_response(user_input: str) -> str:
    """Handles normal chat when screen capture is turned off."""
    memory_context = get_memory_context()
    system_content = "You are a helpful, intelligent personal AI assistant." + memory_context
    
    payload = {
        "model": BRAIN_MODEL,
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "options": {
            "num_predict": 8192
        }
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        return "I'm here to help!"
    except Exception as e:
        return f"Error: {str(e)}"

def get_brainstorming_response_with_vision(user_message: str, vision_feedback: str) -> str:
    """Receives user message and VisionAI screen analysis with the requested system prompt structure."""
    memory_context = get_memory_context()
    system_prompt = (
        "You are an intelligent brainstorming and desktop assistant. "
        "Now the user will ask you a question, and the VisionAI will tell you what the screen looks like. "
        "Use the screen description provided below to understand the user's current context and formulate your response. "
        "Include a [Plan: ...] section in your response if outlining steps or guidance."
        + memory_context
    )
    
    context_content = (
        f"User Question: {user_message}\n\n"
        f"VisionAI Screen Description:\n{vision_feedback}"
    )

    payload = {
        "model": BRAIN_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context_content}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        return vision_feedback
    except Exception as e:
        return f"Error connecting to Brainstorming AI: {str(e)}"
