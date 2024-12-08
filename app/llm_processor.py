import asyncio
from typing import AsyncGenerator
from langchain.chat_models.ollama import ChatOllama

async def async_generator_wrapper(generator):
    """Convert a generator to an asynchronous iterator."""
    for item in generator:
        yield item
        await asyncio.sleep(0.05)

class LLMAdapter:
    """Encapsulates LLM invocation and streaming."""
    
    def __init__(self, model_name: str = "llama3.2:latest", temperature: float = 0.2):
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature
        )

    async def generate_summary_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Generate a streaming summary from the LLM."""
        token_generator = self.llm.stream(prompt)
        async for chunk in async_generator_wrapper(token_generator):
            yield chunk.content if hasattr(chunk, "content") else str(chunk)

    def generate_summary(self, prompt: str) -> str:
        """Generate a complete summary (non-streaming)."""
        return self.llm.invoke(prompt)
