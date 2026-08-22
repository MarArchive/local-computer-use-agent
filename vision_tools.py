import os
import ctypes
import time
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

def get_screen_size():
    """Returns actual screen dimensions."""
    return win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

def normalize_coords(x: int, y: int):
    """Maps 0-1000 grid coordinates to actual screen pixels."""
    screen_w, screen_h = get_screen_size()
    real_x = int((x / 1000.0) * screen_w)
    real_y = int((y / 1000.0) * screen_h)
    return real_x, real_y

def click_at_coordinates(model_x: int, model_y: int, is_normalized: bool = True):
    """Task ID 1: Single click without moving physical mouse."""
    real_x, real_y = normalize_coords(model_x, model_y) if is_normalized else (model_x, model_y)
    try:
        hwnd = win32gui.WindowFromPoint((real_x, real_y))
        if hwnd:
            # Bring window to foreground to give it keyboard focus without moving the mouse
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                pass

            client_x, client_y = win32gui.ScreenToClient(hwnd, (real_x, real_y))
            l_param = win32api.MAKELONG(client_x, client_y)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, l_param)
            return {"success": True, "message": f"Clicked at screen ({real_x}, {real_y})"}
        return {"success": False, "message": "No window found at coordinates."}
    except Exception as e:
        return {"success": False, "message": str(e)}

def double_click_at_coordinates(model_x: int, model_y: int, is_normalized: bool = True):
    """Task ID 4: Double click."""
    real_x, real_y = normalize_coords(model_x, model_y) if is_normalized else (model_x, model_y)
    try:
        hwnd = win32gui.WindowFromPoint((real_x, real_y))
        if hwnd:
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                pass

            client_x, client_y = win32gui.ScreenToClient(hwnd, (real_x, real_y))
            l_param = win32api.MAKELONG(client_x, client_y)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, l_param)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDBLCLK, win32con.MK_LBUTTON, l_param)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, l_param)
            return {"success": True, "message": f"Double-clicked at screen ({real_x}, {real_y})"}
        return {"success": False, "message": "No window found."}
    except Exception as e:
        return {"success": False, "message": str(e)}

def type_at_coordinates(model_x: int, model_y: int, text: str, is_normalized: bool = True):
    """Task ID 3: Click field first, bring window to focus, then type text."""
    click_res = click_at_coordinates(model_x, model_y, is_normalized)
    if not click_res.get("success"):
        return click_res
    
    # Give the OS a moment to focus the window/input field
    time.sleep(0.4)
    try:
        # Added with_spaces=True so spaces between words are properly typed
        pywinauto.keyboard.send_keys(text, with_spaces=True)
        return {"success": True, "message": f"Clicked and typed text: '{text}'"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def drag_coordinates(x1: int, y1: int, x2: int, y2: int, is_normalized: bool = True):
    """Task ID 2: Drag from start to end coordinates."""
    rx1, ry1 = normalize_coords(x1, y1) if is_normalized else (x1, y1)
    rx2, ry2 = normalize_coords(x2, y2) if is_normalized else (x2, y2)
    try:
        hwnd = win32gui.WindowFromPoint((rx1, ry1))
        if hwnd:
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                pass

            cx1, cy1 = win32gui.ScreenToClient(hwnd, (rx1, ry1))
            cx2, cy2 = win32gui.ScreenToClient(hwnd, (rx2, ry2))
            l_param1 = win32api.MAKELONG(cx1, cy1)
            l_param2 = win32api.MAKELONG(cx2, cy2)
            
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param1)
            time.sleep(0.1)
            win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, l_param2)
            time.sleep(0.1)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, l_param2)
            return {"success": True, "message": f"Dragged from ({rx1}, {ry1}) to ({rx2}, {ry2})"}
        return {"success": False, "message": "No window found."}
    except Exception as e:
        return {"success": False, "message": str(e)}