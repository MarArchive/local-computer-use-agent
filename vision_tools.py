import os
import ctypes
from PIL import ImageGrab
import pyautogui
import time

# Force Windows DPI awareness
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

pyautogui.FAILSAFE = True

def take_screenshot(filename="screenshot.png") -> str:
    """Takes a screenshot using PIL ImageGrab."""
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    return os.path.abspath(filename)

def click_at_coordinates(model_x: int, model_y: int, is_normalized: bool = True):
    """Clicks at absolute screen coordinates using PyAutoGUI."""
    try:
        screen_w, screen_h = pyautogui.size()
        if is_normalized:
            real_x = int((model_x / 1000.0) * screen_w)
            real_y = int((model_y / 1000.0) * screen_h)
        else:
            real_x, real_y = model_x, model_y

        pyautogui.click(real_x, real_y)
        return {
            "success": True,
            "message": f"Successfully clicked at screen coords ({real_x}, {real_y})",
        }
    except Exception as e:
        return {"success": False, "message": str(e)}

def type_text(text: str):
    """Types text and submits it with Enter."""
    try:
        time.sleep(0.4) # Brief pause to ensure focus is active
        pyautogui.write(text, interval=0.03)
        pyautogui.press('enter')
        return {"success": True, "message": f"Successfully typed and submitted: '{text}'"}
    except Exception as e:
        return {"success": False, "message": str(e)}