import base64
import re
import requests
from vision_tools import (
    take_screenshot, 
    click_at_coordinates, 
    double_click_at_coordinates, 
    type_at_coordinates, 
    drag_coordinates
)

LOCAL_VLM_URL = "http://localhost:8080/v1/chat/completions"

def encode_image_to_base64(image_path: str) -> str:
    """Encodes a local image file into base64 format for VLM inference."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def run_vision_task(instruction: str) -> dict:
    """
    Captures screen state, queries the local VLM with the structured command prompt,
    parses task sequences (Click, Drag, Type, Double-Click), and executes them.
    """
    screenshot_path = take_screenshot("current_state.png")
    base64_image = encode_image_to_base64(screenshot_path)

    system_prompt = (
        "You are a computer vision OS automation router.\n"
        "You are looking at a fullscreen screenshot of the user's desktop workspace.\n"
        "Analyze the layout to locate UI elements, textboxes, and buttons needed for the request.\n"
        "Output your automation sequence in a strict parseable pattern. Use a separate line for each step:\n"
        "Task IDs: 1 = Click, 2 = Drag, 3 = Type, 4 = Double-click\n"
        "Format:\n"
        "1(GridX,GridY) -> For clicking once\n"
        "2(StartX,StartY,EndX,EndY) -> For dragging\n"
        "3(GridX,GridY,\"Message Text\") -> For typing (it will automatically click once)\n"
        "4(GridX,GridY) -> For clicking twice\n"
        "CRITICAL FORMAT RULES:\n"
        "Coordinates MUST map strictly to a standard scale from 0 to 1000.\n"
        "Where 0,0 is the TOP-LEFT corner of the screen, and 1000,1000 is the BOTTOM-RIGHT corner of the visible screen.\n"
        "Do not output markdown wrappers, chat responses, or notes. Example:\n"
        "1(150,450)\n"
        "3(820,900,\"test message\")"
    )

    payload = {
        "model": "hf.co/unsloth/Qwen3-VL-4B-Instruct-GGUF",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
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
        response = requests.post(LOCAL_VLM_URL, json=payload, timeout=60)
        if response.status_code == 200:
            result_text = response.json()["choices"][0]["message"]["content"].strip()
            print(f"[Vision Agent] Model output:\n{result_text}")
            
            results = []
            lines = result_text.splitlines()
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Match Task 3: Typing -> 3(x, y, "text")
                match_type = re.search(r'^3\(\s*(\d+)\s*,\s*(\d+)\s*,\s*"([^"]+)"\s*\)', line)
                if match_type:
                    x, y, text = int(match_type.group(1)), int(match_type.group(2)), match_type.group(3)
                    print(f"[Vision Agent] Executing Type at ({x}, {y}): '{text}'")
                    res = type_at_coordinates(x, y, text, is_normalized=True)
                    results.append(res)
                    continue

                # Match Task 2: Dragging -> 2(x1, y1, x2, y2)
                match_drag = re.search(r'^2\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', line)
                if match_drag:
                    x1, y1, x2, y2 = int(match_drag.group(1)), int(match_drag.group(2)), int(match_drag.group(3)), int(match_drag.group(4))
                    print(f"[Vision Agent] Executing Drag from ({x1}, {y1}) to ({x2}, {y2})")
                    res = drag_coordinates(x1, y1, x2, y2, is_normalized=True)
                    results.append(res)
                    continue

                # Match Task 4: Double Click -> 4(x, y)
                match_dbl = re.search(r'^4\(\s*(\d+)\s*,\s*(\d+)\s*\)', line)
                if match_dbl:
                    x, y = int(match_dbl.group(1)), int(match_dbl.group(2))
                    print(f"[Vision Agent] Executing Double-Click at ({x}, {y})")
                    res = double_click_at_coordinates(x, y, is_normalized=True)
                    results.append(res)
                    continue

                # Match Task 1: Single Click -> 1(x, y)
                match_click = re.search(r'^1\(\s*(\d+)\s*,\s*(\d+)\s*\)', line)
                if match_click:
                    x, y = int(match_click.group(1)), int(match_click.group(2))
                    print(f"[Vision Agent] Executing Click at ({x}, {y})")
                    res = click_at_coordinates(x, y, is_normalized=True)
                    results.append(res)
                    continue

            return {"success": True, "action_plan": result_text, "execution_results": results}
        else:
            return {"success": False, "error": f"Local server error: {response.status_code} - {response.text}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Could not connect to local server on port 8080."}
    except Exception as e:
        return {"success": False, "error": str(e)}