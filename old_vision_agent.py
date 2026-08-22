#NOT IN USE
#Rename it to activate

import base64
import re
import requests
from vision_tools import take_screenshot, click_at_coordinates

# Local llama.cpp OpenAI-compatible endpoint
LOCAL_VLM_URL = "http://localhost:8080/v1/chat/completions"

def encode_image_to_base64(image_path: str) -> str:
    """Encodes a local image file into base64 format for VLM inference."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def run_vision_task(instruction: str) -> dict:
    """
    Captures screen state, queries the local VLM model, 
    parses coordinates, and executes visual grounding actions.
    """
    # 1. Take screenshot
    screenshot_path = take_screenshot("current_state.png")
    base64_image = encode_image_to_base64(screenshot_path)

    # 2. prompt for local VLM
    payload = {
        "model": "hf.co/unsloth/Qwen3-VL-4B-Instruct-GGUF",
        "messages": [
            {
                "role": "system",
                "content": "You are a desktop UI navigation agent. Look at the screenshot and respond with the exact pixel coordinates [x, y] to click to fulfill the user's request."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

    try:
        # 3. Call local server
        response = requests.post(LOCAL_VLM_URL, json=payload, timeout=60)
        if response.status_code == 200:
            result_text = response.json()["choices"][0]["message"]["content"].strip()
            print(f"[Vision Agent] Model output: {result_text}")
            
            # 4. Parse coordinates like [130, 579] using regex and execute click
            match = re.search(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', result_text)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                print(f"[Vision Agent] Extracted coordinates -> X: {x}, Y: {y}. Executing click...")
                click_result = click_at_coordinates(x, y, is_normalized=True)
                return {"success": True, "action_plan": result_text, "click_result": click_result}
            else:
                return {"success": True, "action_plan": result_text, "warning": "Could not parse coordinates from model response."}
        else:
            return {"success": False, "error": f"Local server error: {response.status_code} - {response.text}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Could not connect to local llama.cpp server. Is it running on port 8080?"}
    except Exception as e:
        return {"success": False, "error": str(e)}