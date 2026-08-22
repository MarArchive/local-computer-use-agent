import subprocess
import os
import platform
import pyautogui

# Safety fail-safe for PyAutoGUI (moving mouse to any corner aborts automation)
pyautogui.FAILSAFE = True

def run_command(command: str) -> dict:
    """Runs a shell command safely and returns output or error."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }
    except Exception as e:
        return {"success": False, "output": "", "error": str(e)}

def open_application(app_name: str) -> dict:
    """Opens an application based on OS type."""
    system = platform.system()
    try:
        if system == "Windows":
            # On Windows, os.startfile or start command works best
            os.startfile(app_name)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", "-a", app_name])
        else:  # Linux
            subprocess.run([app_name])
        return {"success": True, "message": f"Successfully launched {app_name}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def press_shortcut(*keys):
    """Simulates a keyboard shortcut (e.g., 'ctrl', 'c')."""
    try:
        pyautogui.hotkey(*keys)
        return {"success": True, "message": f"Pressed shortcut: {'+'.join(keys)}"}
    except Exception as e:
        return {"success": False, "message": str(e)}