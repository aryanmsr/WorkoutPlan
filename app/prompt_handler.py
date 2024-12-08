class PromptHandler:
    """Handles loading and formatting prompt templates."""
    
    def __init__(self, template_path: str):
        self.template_path = template_path

    def load_prompt(self) -> str:
        """Load the prompt template from the specified file."""
        with open(self.template_path, 'r') as file:
            return file.read()

    def format_prompt(self, activity_data: dict, summary_statistics: dict) -> str:
        """Format the prompt with activity data and summary statistics."""
        template = self.load_prompt()
        return template.format(
            activity_data=activity_data,
            summary_statistics=summary_statistics
        )
