# Local Computer-Use-Agent

A lightweight, dual-agent desktop automation system designed to run entirely locally on standard notebooks (under **8GB VRAM**). By combining direct OS-level execution with a quantized visual fallback, this agent delivers high efficiency, strong accuracy, and complete privacy without requiring heavy cloud infrastructure.

## 🎯 Project Goals
* **Low Resource Footprint:** Optimized for quantized local models requiring less than 8GB VRAM, making it fully runnable on consumer notebooks and laptops.
* **Privacy & Local First:** Keeps all reasoning, planning, and vision processing local to your machine.
* **Smart & Efficient:** Bypasses slow visual navigation by utilizing native OS commands for straightforward tasks, reserving vision-based UI interaction only when necessary.

---

## 🏗️ System Architecture

Built from the ground up as a clean, modular system divided into distinct functional components:

* **User Interface & Orchestrator:** Handles user communication and routes the request to the primary reasoning engine.
* **The Brainstorming AI (The Planner):** A lightweight, quantized local LLM that analyzes user requests, plans the execution steps, and determines whether an OS command or visual action is required.
* **OS Execution Tools:** Direct system-level commands (`os` / `subprocess`) allowing the agent to launch apps, manage files, and execute terminal workflows instantly.
* **Vision Subsystem (The Visual Fallback):** A specialized grid-based vision agent that wakes up to interpret complex graphical interfaces and handle precise mouse/keyboard interactions when OS shortcuts aren't enough.

### 📂 Recommended Modular Structure
```text
├── agent_core.py       # Main orchestrator and user interface loop
├── planner.py          # Brainstorming AI logic and execution planning
├── vision_agent.py     # Grid-based visual UI interpretation module
├── os_tools.py         # Native system operation tools (App launching, file management)
├── vision_tools.py     # Screen capture, coordinate calculation, and mouse/keyboard control
└── requirements.txt    # Clean dependencies list
