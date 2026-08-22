import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import os
import re

import functions
from brainstorming_agent import get_standard_response, get_brainstorming_response_with_vision
from vision_agent import run_vision_analysis
from memory_manager import save_memory

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Global state to keep track of the latest interaction for saving
latest_interaction = {"user_query": "", "ai_response": ""}

def insert_formatted_text(text_widget, text, tag_prefix="ai"):
    """Parses basic markdown (bold **text**, headings ###) and inserts styled text into Tkinter."""
    parts = re.split(r'(\*\*.*?\*\*|###\s*.*?\n)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            text_widget.insert(tk.END, part[2:-2], f"{tag_prefix}_bold")
        elif part.startswith('###'):
            text_widget.insert(tk.END, part.replace('###', '').strip() + "\n", f"{tag_prefix}_heading")
        else:
            text_widget.insert(tk.END, part, f"{tag_prefix}_normal")
    text_widget.insert(tk.END, "\n\n")
    text_widget.see(tk.END)

def run_agent_pipeline(user_message, capture_enabled, chat_window, log_window, overlay):
    global latest_interaction
    latest_interaction["user_query"] = user_message
    latest_interaction["ai_response"] = ""

    def update_chat(prefix, text, tag_prefix):
        chat_window.after(0, lambda: chat_window.insert(tk.END, prefix, f"{tag_prefix}_bold"))
        chat_window.after(0, lambda: insert_formatted_text(chat_window, text, tag_prefix))

    def update_log(text):
        log_window.after(0, lambda: log_window.insert(tk.END, text + "\n"))
        log_window.after(0, lambda: log_window.see(tk.END))

    try:
        update_chat("👤 You: ", user_message, "user")
        update_log(f"--- New Request: '{user_message}' ---")

        if capture_enabled:
            update_log("📸 Step 1: VisionAI analyzing the screen...")
            chat_window.after(0, lambda: chat_window.insert(tk.END, "🤖 Brainstorming AI: Inspecting your screen...\n", "ai_normal"))
            
            vision_feedback = run_vision_analysis(user_message, overlay)
            update_log(f"👁️ VisionAI Screen Description:\n{vision_feedback}")

            update_log("🧠 Step 2: Sending user message and VisionAI description to Brainstorming AI...")
            final_answer = get_brainstorming_response_with_vision(user_message, vision_feedback)
            
            update_chat("🤖 Brainstorming AI: ", final_answer, "ai")
            latest_interaction["ai_response"] = final_answer
            update_log("✨ Response delivered successfully.\n")
        else:
            update_log("💬 Executing standard chat response (No screen capture)...")
            response = get_standard_response(user_message)
            update_chat("🤖 Brainstorming AI: ", response, "ai")
            latest_interaction["ai_response"] = response
            update_log("✨ Response delivered.\n")

    except Exception as e:
        update_log(f"❌ Error: {str(e)}")
        chat_window.after(0, lambda: chat_window.insert(tk.END, f"❌ An error occurred: {str(e)}\n\n", "user_bold"))

# --- UI Setup ---
root = tk.Tk()
root.title("Collaborative Agent Hub")
root.geometry("700x780")
root.minsize(500, 500)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Main Container Frame
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
main_frame.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)

# Tabbed Notebook Layout
notebook = ttk.Notebook(main_frame)
notebook.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 10))

# Tab 1: Chat Hub
tab_chat = ttk.Frame(notebook)
notebook.add(tab_chat, text="💬 Chat Hub")
tab_chat.rowconfigure(0, weight=1)
tab_chat.columnconfigure(0, weight=1)

chat_display = scrolledtext.ScrolledText(tab_chat, wrap='word', font=("Segoe UI", 10))
chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Configure text tags for clean readability
chat_display.tag_configure("user_bold", font=("Segoe UI", 10, "bold"), foreground="#005fb8")
chat_display.tag_configure("user_normal", font=("Segoe UI", 10), foreground="#333333")
chat_display.tag_configure("ai_bold", font=("Segoe UI", 10, "bold"), foreground="#107c41")
chat_display.tag_configure("ai_normal", font=("Segoe UI", 10), foreground="#222222")
chat_display.tag_configure("ai_heading", font=("Segoe UI", 11, "bold"), foreground="#004578")

# Tab 2: Execution Logs
tab_logs = ttk.Frame(notebook)
notebook.add(tab_logs, text="📊 Live Execution Logs")
tab_logs.rowconfigure(0, weight=1)
tab_logs.columnconfigure(0, weight=1)

log_display = scrolledtext.ScrolledText(tab_logs, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
log_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Bottom Controls Frame (Fixed at bottom, stays visible when resizing)
control_frame = tk.Frame(main_frame)
control_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
control_frame.columnconfigure(0, weight=1)

# Top row inside control frame: Checkbox and Save to Memory button
options_row = tk.Frame(control_frame)
options_row.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 6))
options_row.columnconfigure(0, weight=1)

capture_var = tk.BooleanVar(value=False)
capture_checkbox = tk.Checkbutton(
    options_row, 
    text="📸 Capture screen & analyze before answering", 
    variable=capture_var,
    font=("Segoe UI", 10)
)
capture_checkbox.pack(side="left")

def handle_save_memory():
    if not latest_interaction["ai_response"]:
        log_display.insert(tk.END, "⚠️ No recent response available to save.\n")
        return
    save_memory(latest_interaction["user_query"], latest_interaction["ai_response"])
    log_display.insert(tk.END, "💾 Successfully saved interaction to memory!\n")
    log_display.see(tk.END)

save_mem_button = tk.Button(
    options_row, 
    text="💾 Save Last Response to Memory", 
    command=handle_save_memory, 
    font=("Segoe UI", 9, "bold"), 
    bg="#107c41", 
    fg="white",
    padx=8, pady=2
)
save_mem_button.pack(side="right")

# Input and Send Button Row
input_row = tk.Frame(control_frame)
input_row.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
input_row.columnconfigure(0, weight=1)

chat_input = tk.Entry(input_row, font=("Segoe UI", 11))
chat_input.grid(row=0, column=0, sticky="ew", padx=(0, 8), ipady=4)

def handle_send():
    user_query = chat_input.get()
    if not user_query.strip():
        return
    chat_input.delete(0, tk.END)
    is_capture_checked = capture_var.get()
    threading.Thread(
        target=run_agent_pipeline, 
        args=(user_query, is_capture_checked, chat_display, log_display, overlay_root), 
        daemon=True
    ).start()

chat_input.bind("<Return>", lambda event: handle_send())
send_button = tk.Button(input_row, text="Send Message", command=handle_send, font=("Segoe UI", 10, "bold"), bg="#0078d7", fg="white", padx=10, pady=2)
send_button.grid(row=0, column=1, sticky="e")

# Invisible Overlay for Cursor Tracking
overlay_root = tk.Toplevel(root)
overlay_root.attributes("-fullscreen", True, "-topmost", True)
overlay_root.config(bg="gray")
overlay_root.attributes("-transparentcolor", "gray")

cursor_img_file = os.path.join(SCRIPT_DIR, "cursor.png")
if os.path.exists(cursor_img_file):
    cursor_asset = tk.PhotoImage(file=cursor_img_file)
    functions.cursor_label = tk.Label(overlay_root, image=cursor_asset, bg="gray", bd=0)
    functions.cursor_label.image = cursor_asset
    functions.cursor_label.place(x=0, y=0)

root.mainloop()