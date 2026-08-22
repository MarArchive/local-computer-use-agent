import sys
from planner import TaskPlanner
from os_tools import run_command, open_application, press_shortcut
from vision_agent import run_vision_task

class LocalComputerAgent:
    def __init__(self):
        self.planner = TaskPlanner()

    def execute(self, instruction: str):
        print(f"\n[Agent] Received instruction: '{instruction}'")
        
        # 1. Plan route
        plan = self.planner.parse_plan(instruction)
        route = plan["route"]
        print(f"[Agent] Routed to: {route}")

        # 2. Execute based on route
        if route == "os_tools":
            instruction_lower = instruction.lower()
            if instruction_lower.startswith("open "):
                app_name = instruction[5:].strip()
                print(f"[OS Tools] Launching application: {app_name}")
                result = open_application(app_name)
                print(f"[Result] {result}")
            else:
                print(f"[OS Tools] Running shell command: {instruction}")
                result = run_command(instruction)
                print(f"[Result] {result}")
        
        elif route == "vision_agent":
            print("[Vision Agent] Engaging VLM via llama.cpp for visual grounding...")
            result = run_vision_task(instruction)
            print(f"[Result] {result}")

if __name__ == "__main__":
    agent = LocalComputerAgent()
    print("=== Local Computer Use Agent Initialized ===")
    print("Type your instructions below (type 'exit' to quit).\n")
    
    while True:
        try:
            user_input = input("Agent Prompt > ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting agent. Goodbye!")
                break
            if not user_input:
                continue
            agent.execute(user_input)
        except KeyboardInterrupt:
            print("\nExiting agent. Goodbye!")
            break