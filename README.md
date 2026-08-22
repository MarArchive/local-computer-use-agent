# Local Computer-Use-Agent

> ⚠️ **Note:** This project is under active development. AI-generated outputs are experimental and may contain inaccuracies.

A local, privacy-first desktop AI assistant powered by **Ollama**, featuring real-time screen inspection (**VisionAI**) and a manual, file-based **JSON Memory System**. 

## 🎯 Project Goals
* **Low Resource Footprint:** Optimized for quantized local models requiring **less than 8GB VRAM**, making it fully runnable on consumer notebooks and laptops.
* **Privacy & Local First:** Keeps all reasoning, planning, and vision processing completely local to your machine.
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
local-computer-use-agent/
│
├── agent_core.py            # Main Tkinter UI, event loops, and window management
├── brainstorming_agent.py   # Ollama API integration and prompt construction
├── vision_agent.py          # Screen capture and visual context analyzer
├── memory_manager.py        # JSON-based memory storage, reading, and sorting
├── functions.py             # Utility helpers and cursor overlay handling
├── requirements.txt         # Python package dependencies
├── cursor.png               # Custom cursor asset for screen tracking
└── memories/                # Automatically generated folder storing JSON memory files
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MarArchive/local-computer-use-agent.git
cd local-computer-use-agent
```

### 2. Set Up a Virtual Environment & Install Dependencies

* **Windows (PowerShell / CMD):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

* **Mac or Linux:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

---

## 🧠 Running Ollama & The Models

This project uses **two local models** running via Ollama:

1. **Brainstorming Model (`gemma4:e4b`):** Handles general reasoning, chat text, and detailed responses.
2. **Vision Model (`Qwen3-VL-4B-Instruct-GGUF`):** Handles real-time screen inspection and visual context.

Make sure you have both models pulled/ready in Ollama:

```bash
ollama pull gemma4:e4b
ollama pull hf.co/unsloth/Qwen3-VL-4B-Instruct-GGUF
```

If you need to configure a specific host or port for your Ollama instance, set your environment variables before launching:

* **Windows PowerShell:**
  ```powershell
  \$env:OLLAMA_HOST="127.0.0.1:8080"
  ```

* **Windows CMD:**
  ```cmd
  set OLLAMA_HOST=127.0.0.1:8080
  ```

* **Mac or Linux:**
  ```bash
  export OLLAMA_HOST=127.0.0.1:8080
  ```

---

## ▶️ Launching the Application

Once Ollama is running in the background and your virtual environment is active, start the desktop assistant UI:

```bash
python agent_core.py
```
