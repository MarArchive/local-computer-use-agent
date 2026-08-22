import json

class TaskPlanner:
    def __init__(self):
        # Define keywords or patterns that can be handled instantly by OS tools
        self.fast_path_keywords = ["open", "run", "start", "close", "terminal", "cmd", "file"]

    def decide_route(self, instruction: str) -> str:
        """
        Decides whether to route the task to the fast OS executor 
        or the vision fallback agent.
        """
        instruction_lower = instruction.lower()
        
        # Check if it's a direct OS action
        if any(keyword in instruction_lower for keyword in self.fast_path_keywords):
            return "os_tools"
        
        # Otherwise, route to the vision-language model agent for UI navigation
        return "vision_agent"

    def parse_plan(self, instruction: str):
        route = self.decide_route(instruction)
        return {
            "instruction": instruction,
            "route": route,
            "status": "ready"
        }