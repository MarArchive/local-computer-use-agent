import time
import win32gui
import win32api
import win32con
import pyautogui

# Global spatial registers
curr_x, curr_y = 0, 0
target_window_hwnd = None
cursor_label = None  # Will be bound from the main UI script later

def update_cursor_ui(x, y):
    if cursor_label:
        cursor_label.place(x=int(x), y=int(y))

def glide_fake_cursor(start_x, start_y, target_x, target_y, root):
    current_x, current_y = start_x, start_y
    while current_x != target_x or current_y != target_y:
        if current_x < target_x: current_x = min(current_x + 5, target_x)
        elif current_x > target_x: current_x = max(current_x - 5, target_x)
        if current_y < target_y: current_y = min(current_y + 5, target_y)
        elif current_y > target_y: current_y = max(current_y - 5, target_y)
        
        root.after(0, update_cursor_ui, current_x, current_y)
        time.sleep(0.01)
    return current_x, current_y

def send_background_click(target_x, target_y):
    hwnd = win32gui.WindowFromPoint((target_x, target_y))
    if hwnd:
        local_x, local_y = win32gui.ScreenToClient(hwnd, (target_x, target_y))
        pixel_location = win32api.MAKELONG(local_x, local_y)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pixel_location)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, pixel_location)
        return hwnd
    return None

def background_drag(start_x, start_y, end_x, end_y, steps=50, duration=0.8, root=None):
    global curr_x, curr_y
    curr_x, curr_y = start_x, start_y
    root.after(0, update_cursor_ui, curr_x, curr_y)
    
    hwnd = win32gui.WindowFromPoint((start_x, start_y))
    if not hwnd: return
        
    delay = duration / steps
    local_start_x, local_start_y = win32gui.ScreenToClient(hwnd, (start_x, start_y))
    local_end_x, local_end_y = win32gui.ScreenToClient(hwnd, (end_x, end_y))
    
    start_location = (local_start_y << 16) | local_start_x
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, start_location)
    time.sleep(0.1) 
    
    for i in range(steps + 1):
        progress = i / steps
        win_curr_x = int(local_start_x + (local_end_x - local_start_x) * progress)
        win_curr_y = int(local_start_y + (local_end_y - local_start_y) * progress)
        win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, (win_curr_y << 16) | win_curr_x)
        
        curr_x = int(start_x + (end_x - start_x) * progress)
        curr_y = int(start_y + (end_y - start_y) * progress)
        root.after(0, update_cursor_ui, curr_x, curr_y)
        time.sleep(delay)
        
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, (local_end_y << 16) | local_end_x)


def send_background_text(hwnd, text_string):
    if not hwnd: 
        return
        
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        pass  # focus-steal denied; try anyway
        
    time.sleep(0.05)
    
    # Split the text by lines to isolate the newline behavior
    lines = text_string.split('\n')
    
    for i, line in enumerate(lines):
        if line:
            pyautogui.write(line)
            
        # If this is not the last line, insert the Shift+Enter line break
        if i < len(lines) - 1:
            with pyautogui.hold('shift'):
                pyautogui.press('enter')
            time.sleep(0.05)
            

def perform_click(btn_x, btn_y, root):
    global curr_x, curr_y, target_window_hwnd
    curr_x, curr_y = glide_fake_cursor(curr_x, curr_y, btn_x, btn_y, root)
    target_window_hwnd = send_background_click(int(btn_x), int(btn_y))

def perform_double_click(btn_x,btn_y,root):
    global curr_x, curr_y, target_window_hwnd
    curr_x, curr_y = glide_fake_cursor(curr_x, curr_y, btn_x, btn_y, root)
    target_window_hwnd = send_background_click(int(btn_x), int(btn_y))
    send_background_click(int(btn_x), int(btn_y))
    
    
def perform_drag(dest_x, dest_y, root):
    global curr_x, curr_y
    background_drag(curr_x, curr_y, dest_x, dest_y, root=root)

def perform_type(dest_x, dest_y, msg, root):
    global target_window_hwnd
    perform_click(dest_x, dest_y, root)
    send_background_text(target_window_hwnd, msg)
