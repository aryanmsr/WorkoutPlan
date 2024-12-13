from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from app.data_preprocessing import DataPreprocessor
from app.prompt_handler import PromptHandler
from app.llm_processor import LLMAdapter
from app.email_handler import EmailHandler
from datetime import datetime
import logging
import json
import config
import os
from typing import Set
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

load_dotenv()
VERIFY_TOKEN = os.getenv('STRAVA_VERIFY_TOKEN')
processed_activities: Set[int] = set()  # Track processed activity IDs

app = FastAPI()
email_handler = EmailHandler()

async def process_activity_data():
    """Helper function to process activity data and generate statistics"""
    try:
        preprocessor = DataPreprocessor()
        preprocessor.fetch_activities()
        preprocessor.process_run_data()
        preprocessor.calculate_summary_statistics()
        preprocessor.save_to_json(config.ACTIVITY_DATA_PATH, config.SUMMARY_STATS_PATH)
        logger.info("Activity data processed successfully")
        return True
    except Exception as e:
        logger.error(f"Error processing activity data: {str(e)}")
        return False

@app.get("/strava-webhook")
async def validate_strava_webhook(request: Request):
    """Validate Strava webhook subscription"""
    params = request.query_params
    
    hub_mode = params.get('hub.mode')
    hub_challenge = params.get('hub.challenge')
    hub_verify_token = params.get('hub.verify_token')
    
    logger.info("Webhook validation request received")
    logger.info(f"Mode: {hub_mode}")
    logger.info(f"Challenge: {hub_challenge}")
    logger.info(f"Received Verify Token: {hub_verify_token}")
    logger.info(f"Expected Verify Token: {VERIFY_TOKEN}")

    if (hub_mode == 'subscribe' and 
        hub_verify_token == VERIFY_TOKEN and 
        hub_challenge):
        logger.info("Webhook validation successful")
        return JSONResponse(content={"hub.challenge": hub_challenge})
    
    logger.error("Webhook validation failed")
    logger.error(f"Token match: {hub_verify_token == VERIFY_TOKEN}")
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/strava-webhook")
async def handle_strava_webhook(request: Request):
    """Handle incoming Strava webhook events and generate advice"""
    try:
        payload = await request.json()
        activity_id = int(payload.get('object_id', 0))

        # For some weird reason, I was getting multiple webhook events for the same activity. So need to handle that.
        if activity_id in processed_activities:
            logger.info(f"Skipping already processed activity: {activity_id}")
            return JSONResponse(status_code=200, content={"status": "already processed"})

        logger.info("\n=== WEBHOOK PAYLOAD DETAILS ===")
        logger.info(f"Full payload: {payload}")
        logger.info(f"Time: {datetime.now()}")
        logger.info(f"Event Type: {payload.get('aspect_type')}")
        logger.info(f"Object Type: {payload.get('object_type')}")
        logger.info(f"Activity ID: {activity_id}")
        logger.info(f"Owner ID: {payload.get('owner_id')}")
        logger.info(f"Updates: {payload.get('updates', {})}")
        logger.info("===============================\n")
        
        if (payload.get('object_type') == 'activity' and 
            payload.get('aspect_type') == 'create'):
            
            processed_activities.add(activity_id)  
            logger.info("Processing new activity creation...")

            if await process_activity_data():
                try:
                    with open(config.ACTIVITY_DATA_PATH, "r") as file:
                        activity_data = json.load(file)
                    with open(config.SUMMARY_STATS_PATH, "r") as file:
                        summary_statistics = json.load(file)

                    prompt_handler = PromptHandler(config.PROMPT_TEMPLATE_PATH)
                    prompt = prompt_handler.format_prompt(activity_data, summary_statistics)
                    llm_adapter = LLMAdapter(model_name=config.MODEL_NAME)
                    
                    advice = ""
                    async for token in llm_adapter.generate_summary_stream(prompt):
                        advice += token
                    
                    logger.info("New advice generated:")
                    logger.info(advice)

                    subject = "New Workout Advice Available!"
                    if await email_handler.send_email(subject, advice):
                        logger.info("Email sent successfully")
                        return JSONResponse(status_code=200, content={"status": "processed"})
                    else:
                        logger.error("Failed to send email")
                    
                except Exception as e:
                    logger.error(f"Error generating advice: {str(e)}")
            
        return JSONResponse(status_code=200, content={"status": "received"})
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return JSONResponse(status_code=200, content={"status": "error", "message": str(e)})
    

@app.get("/stream_advice")
async def stream_advice():
    """
    Stream fitness advice based on processed data and summary statistics.
    """
    try:
        # Processing latest activity data
        await process_activity_data()

        # Loading processed data
        with open(config.ACTIVITY_DATA_PATH, "r") as file:
            activity_data = json.load(file)
        with open(config.SUMMARY_STATS_PATH, "r") as file:
            summary_statistics = json.load(file)

        # Generating and streaming advice
        prompt_handler = PromptHandler(config.PROMPT_TEMPLATE_PATH)
        prompt = prompt_handler.format_prompt(activity_data, summary_statistics)
        llm_adapter = LLMAdapter(model_name=config.MODEL_NAME)
        
        async def advice_stream():
            async for token in llm_adapter.generate_summary_stream(prompt):
                yield token

        logger.info("Streaming advice started")
        return StreamingResponse(advice_stream(), media_type="text/plain")
    except Exception as e:
        logger.error(f"Error in stream_advice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/webhook-test")
async def test_webhook():
    """
    Test endpoint to simulate a Strava webhook event
    """
    try:
        logger.info("Starting webhook test...")
        
        # Process activity data
        if await process_activity_data():
            try:
                # Generate advice
                with open(config.ACTIVITY_DATA_PATH, "r") as file:
                    activity_data = json.load(file)
                with open(config.SUMMARY_STATS_PATH, "r") as file:
                    summary_statistics = json.load(file)

                prompt_handler = PromptHandler(config.PROMPT_TEMPLATE_PATH)
                prompt = prompt_handler.format_prompt(activity_data, summary_statistics)
                llm_adapter = LLMAdapter(model_name=config.MODEL_NAME)
                
                advice = ""
                async for token in llm_adapter.generate_summary_stream(prompt):
                    advice += token
                
                logger.info("Test webhook advice generated:")
                logger.info(advice)
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "success",
                        "message": "Test webhook processed successfully",
                        "advice": advice
                    }
                )
            except Exception as e:
                logger.error(f"Error generating test advice: {str(e)}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "status": "error",
                        "message": f"Error generating advice: {str(e)}"
                    }
                )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Failed to process activity data"
                }
            )
    except Exception as e:
        logger.error(f"Unexpected error in webhook test: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.1", port=8000)