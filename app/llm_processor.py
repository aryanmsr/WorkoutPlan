"""
Handles LLM interactions using Hugging Face's API for text generation.
"""

from huggingface_hub import InferenceClient
import os
from typing import AsyncGenerator
from dotenv import load_dotenv
import asyncio

load_dotenv()

class LLMAdapter:
   """Handles LLM interactions for text generation."""
   
   def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.3", temperature: float = 0.7) -> None:
       """Initialize with model configuration."""
       self.client = InferenceClient(api_key=os.getenv('HUGGINGFACE_TOKEN'))
       self.model_name = model_name
       self.temperature = temperature

   def generate_summary(self, prompt: str) -> str:
       """
       Generate complete response from LLM.
       
       Args:
           prompt: Input text for LLM
           
       Returns:
           Complete generated text
       """
       try:
           messages = [{"role": "user", "content": prompt}]
           
           completion = self.client.chat.completions.create(
               model=self.model_name,
               messages=messages,
               temperature=self.temperature,
               max_tokens=10000
           )
           
           return completion.choices[0].message.content
           
       except Exception as e:
           print(f"Exception occurred: {str(e)}")
           return f"Error: {str(e)}"

   async def generate_summary_stream(self, prompt: str) -> AsyncGenerator[str, None]:
       """
       Generate streaming response from LLM.
       
       Args:
           prompt: Input text for LLM
           
       Returns:
           AsyncGenerator yielding text chunks
       """
       try:
           messages = [{"role": "user", "content": prompt}]
           
           stream = self.client.chat.completions.create(
               model=self.model_name,
               messages=messages,
               temperature=self.temperature,
               max_tokens=10000,
               stream=True
           )
           
           for chunk in stream:
               if chunk.choices[0].delta.content is not None:
                   yield chunk.choices[0].delta.content
                   await asyncio.sleep(0.01)  # Small delay to control stream rate
               
       except Exception as e:
           print(f"Exception occurred in stream: {str(e)}")
           yield f"Error: {str(e)}"