# Local Computer-Use-Agent

A local, privacy-first desktop AI assistant powered by **Ollama**, featuring real-time screen inspection (**VisionAI**) and a manual, file-based **JSON Memory System**. 

## 🎯 Project Goals
* **Low Resource Footprint:** Optimized for quantized local models requiring less than 8GB VRAM, making it fully runnable on consumer notebooks and laptops(under **8GB VRAM**).
* **Privacy & Local First:** Keeps all reasoning, planning, and vision processing local to your machine.
* **Smart & Efficient:** Bypasses slow visual navigation by utilizing native OS commands for straightforward tasks, reserving vision-based UI interaction only when necessary.


---

## ✨ Key Features

* **💬 Chat Hub UI:** A clean, responsive Tkinter interface supporting basic markdown styling (bold text, headings) and thread-safe background execution.
* **📸 Screen Context (VisionAI):** Optionally capture and analyze your active desktop screen to give your AI contextual awareness of what you're working on.
* **💾 Curated JSON Memory System:** Prevent AI clutter by manually saving your best Q&A interactions into individual `.json` files. The system automatically pulls recent memories into the AI prompt context.
* **📊 Live Execution Logs:** A built-in terminal/log tab to track background steps, vision summaries, and errors in real-time.

---

## 📁 Project File Structure

```text
collaborative-agent-hub/
│
├── agent_core.py            # Main Tkinter UI, event loops, and window management
├── brainstorming_agent.py   # Ollama API integration and prompt construction
├── vision_agent.py          # Screen capture and visual context analyzer
├── memory_manager.py        # JSON-based memory storage, reading, and sorting
├── functions.py             # Utility helpers and cursor overlay handling
├── requirements.txt         # Python package dependencies
├── cursor.png               # Custom cursor asset for screen tracking
└── memories/                # Automatically generated folder storing JSON memory files
