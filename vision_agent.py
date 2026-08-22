import base64
import os
import time
import requests
import pyautogui
import win32api

LOCAL_VLM_URL = "http://localhost:8080/v1/chat/completions"
VISION_MODEL = "hf.co/unsloth/Qwen3-VL-4B-Instruct-GGUF"

SCREEN_WIDTH = win32api.GetSystemMetrics(0)
SCREEN_HEIGHT = win32api.GetSystemMetrics(1)

def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def run_vision_analysis(user_message: str, overlay) -> str:
    screenshot_path = "live_snapshot.png"
    
    if overlay and overlay.winfo_exists():
        overlay.after(0, lambda: overlay.attributes("-alpha", 0.0))
    
    time.sleep(0.2)
    raw_screenshot = pyautogui.screenshot()
    raw_screenshot.save(screenshot_path, "PNG")
    
    if overlay and overlay.winfo_exists():
        overlay.after(0, lambda: overlay.attributes("-alpha", 1.0))

    base64_image = encode_image_to_base64(screenshot_path)

    system_rules = (
        "You are a precise screen-analysis assistant. "
        "Analyze the user's screenshot and provide a short, concise summary (under 4-5 bullet points) "
        "focusing ONLY on: 1) The active application/software name, 2) The main code, text, or content visible, "
        "and 3) What the user is likely trying to do based on their question. Avoid unnecessary visual fluff."
    )

    payload = {
        "model": VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{system_rules}\n\nContext / User Query: {user_message}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 2048
    }

    try:
        response = requests.post(LOCAL_VLM_URL, json=payload, timeout=60)
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        return f"Vision Error: {response.status_code} - {response.text}"
    except Exception as e:
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
        return f"Error: {str(e)}"
