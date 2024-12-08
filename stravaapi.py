from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.data_preprocessing import DataPreprocessor
from app.prompt_handler import PromptHandler
from app.llm_processor import LLMAdapter
import json
import config

app = FastAPI()

@app.get("/stream_advice")
async def stream_advice():
    """
    Stream fitness advice based on processed data and summary statistics.
    """
    #Processsing and saving my latest fitness data
    preprocessor = DataPreprocessor()
    preprocessor.fetch_activities()
    preprocessor.process_run_data()
    preprocessor.calculate_summary_statistics()
    preprocessor.save_to_json(config.ACTIVITY_DATA_PATH, config.SUMMARY_STATS_PATH)

    with open(config.ACTIVITY_DATA_PATH, "r") as file:
        activity_data = json.load(file)
    with open(config.SUMMARY_STATS_PATH, "r") as file:
        summary_statistics = json.load(file)

    #Preparing the system prompt
    prompt_handler = PromptHandler(config.PROMPT_TEMPLATE_PATH)
    prompt = prompt_handler.format_prompt(activity_data, summary_statistics)

    #Streaming LLM response
    llm_adapter = LLMAdapter(model_name=config.MODEL_NAME)
    async def advice_stream():
        async for token in llm_adapter.generate_summary_stream(prompt):
            yield token

    return StreamingResponse(advice_stream(), media_type="text/plain")

