import os
import json
import time

MEMORY_DIR = "memories"

def init_memory_dir():
    """Ensures the memories folder exists."""
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)

def save_memory(user_query: str, ai_response: str):
    """Saves an approved interaction as an individual JSON file."""
    init_memory_dir()
    timestamp = int(time.time())
    filename = os.path.join(MEMORY_DIR, f"memory_{timestamp}.json")
    
    memory_data = {
        "timestamp": timestamp,
        "user_query": user_query,
        "ai_response": ai_response
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=4)

def get_all_memories(limit=5):
    """Reads the most recent JSON memory files from the memories directory."""
    init_memory_dir()
    if not os.path.exists(MEMORY_DIR):
        return []
    
    # Get all json files in the folder
    files = [os.path.join(MEMORY_DIR, f) for f in os.listdir(MEMORY_DIR) if f.endswith(".json")]
    
    # Sort files by modification time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)
    
    memories = []
    for file_path in files[:limit]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                memories.append((data.get("user_query", ""), data.get("ai_response", "")))
        except Exception:
            continue
            
    return memories