#NOT IN USE
#Rename it to activate it

import os
import ctypes
from PIL import Image, ImageGrab
import pywinauto
import win32gui
import win32api
import win32con

# Force Windows DPI awareness
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

def take_screenshot(filename="screenshot.png") -> str:
    """Takes a screenshot using PIL ImageGrab without pyautogui."""
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    return os.path.abspath(filename)

def click_at_coordinates(model_x: int, model_y: int, is_normalized: bool = True):
    """
    Clicks at screen coordinates using Win32 messages via pywinauto/win32gui 
    WITHOUT moving the physical mouse cursor.
    """
    # Get actual screen dimensions
    screen_w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    if is_normalized:
        real_x = int((model_x / 1000.0) * screen_w)
        real_y = int((model_y / 1000.0) * screen_h)
    else:
        real_x, real_y = model_x, model_y

    try:
        # Find window handle at the target screen coordinates
        hwnd = win32gui.WindowFromPoint((real_x, real_y))
        if hwnd:
            # Convert screen coordinates to client coordinates of the target window
            client_x, client_y = win32gui.ScreenToClient(hwnd, (real_x, real_y))
            l_param = win32api.MAKELONG(client_x, client_y)
            
            # Send mouse down and mouse up messages directly to the window handle
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, l_param)
            
            return {
                "success": True,
                "message": f"Successfully clicked HWND {hwnd} at client coords ({client_x}, {client_y}) without moving mouse.",
            }
        else:
            return {"success": False, "message": f"No window found at coordinates ({real_x}, {real_y})"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def type_text(text: str):
    """Types text using pywinauto keyboard methods without moving the mouse."""
    try:
        pywinauto.keyboard.send_keys(text)
        return {"success": True, "message": f"Typed text via pywinauto: {text}"}
    except Exception as e:
        return {"success": False, "message": str(e)}