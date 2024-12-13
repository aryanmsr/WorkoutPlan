"""
Service for generating personalized fitness advice using local LLM.
Processes activity data and generates training recommendations.
"""

import json
from typing import Dict, Any
from app.prompt_handler import PromptHandler
from app.llm_processor import LLMAdapter

class FitnessAdviceService:
   """
   Handles generation of fitness advice using activity data and LLM.
   """
   
   def __init__(self, prompt_path: str, model_name: str = "llama3.2:latest") -> None:
       """Initialize with prompt template and model configuration."""
       self.prompt_handler = PromptHandler(prompt_path)
       self.llm_adapter = LLMAdapter(model_name=model_name)

   def generate_advice(self, activity_data_path: str, summary_stats_path: str) -> str:
       """
       Generate fitness advice from activity data and statistics.
       
       Args:
           activity_data_path: Path to activity data JSON
           summary_stats_path: Path to statistics JSON
           
       Returns:
           Generated advice text
       """
       with open(activity_data_path, 'r') as file:
           activity_data: Dict[str, Any] = json.load(file)
       with open(summary_stats_path, 'r') as file:
           summary_statistics: Dict[str, Any] = json.load(file)

       prompt: str = self.prompt_handler.format_prompt(activity_data, summary_statistics)
       return self.llm_adapter.generate_summary(prompt)