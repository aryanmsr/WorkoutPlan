import json
from app.prompt_handler import PromptHandler
from app.llm_processor import LLMAdapter

class FitnessAdviceService:
    """Generates personalized fitness advice using LLM."""
    
    def __init__(self, prompt_path: str, model_name: str = "llama3.2:latest"):
        self.prompt_handler = PromptHandler(prompt_path)
        self.llm_adapter = LLMAdapter(model_name=model_name)

    def generate_advice(self, activity_data_path: str, summary_stats_path: str) -> str:
        """Generates fitness advice based on activity data and statistics."""
        # Load data
        with open(activity_data_path, 'r') as file:
            activity_data = json.load(file)
        with open(summary_stats_path, 'r') as file:
            summary_statistics = json.load(file)

        # Format prompt
        prompt = self.prompt_handler.format_prompt(activity_data, summary_statistics)

        # Get advice
        return self.llm_adapter.generate_summary(prompt)
