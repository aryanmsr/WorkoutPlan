"""
Handles prompt template loading and formatting for LLM input.
"""

from typing import Dict, Any

class PromptHandler:
   """
   Class to handle loading and formatting of prompt templates.
   """
   
   def __init__(self, template_path: str) -> None:
       """Initialize with path to prompt template file."""
       self.template_path = template_path

   def load_prompt(self) -> str:
       """Load prompt template from file."""
       with open(self.template_path, 'r') as file:
           return file.read()

   def format_prompt(self, activity_data: Dict[str, Any], summary_statistics: Dict[str, Any]) -> str:
       """
       Format prompt with activity data and statistics.
       
       Args:
           activity_data: Activity details
           summary_statistics: Aggregated statistics
           
       Returns:
           Formatted prompt for LLM
       """
       template = self.load_prompt()
       return template.format(
           activity_data=activity_data,
           summary_statistics=summary_statistics
       )
   
