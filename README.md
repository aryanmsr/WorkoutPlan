# WorkoutPlan

A Python application that integrates with the Strava API to fetch activities, analyze fitness data, and provide personalized training advice through LLM integration.

## Features
- Authenticate with Strava API and manage access tokens
- Fetch recent activities such as runs, rides, or hikes
- Analyze activities to calculate total distance, average distance, and activity count
- Real-time webhook integration for automatic activity processing
- LLM-powered personalized training advice
- Streaming API for fitness recommendations

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/aryanmsr/WorkoutPlan.git 
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .venv
    source .venv/bin/activate   # On Windows: .venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Add your environment variables in a `.env` file in the root directory:
    ```
    CLIENT_ID=your_strava_client_id
    CLIENT_SECRET=your_strava_client_secret
    STRAVA_VERIFY_TOKEN=your_webhook_verify_token
    ```

## Required Dependencies
- ngrok for public URL access.
- Latest Llama 3.2 model via Ollama (to run LLMs locally)
- FastAPI 

# Strava Webhook Integration Documentation

## Initial Setup

### Environment Variables
Create a `.env` file in your root directory with:
```bash
STRAVA_VERIFY_TOKEN=you_example_verify_token
CLIENT_ID=your_athlete_client_id
CLIENT_SECRET=your_athlete_client_secret
```

### Starting the Services

1. Start ngrok tunnel (Terminal 1):
```bash
ngrok http 8000
```
- Keep this terminal open
- Copy the generated https URL (e.g., `https://xxxx-xxx-xxx-xx.ngrok-free.app`)

2. Start FastAPI server (Terminal 2):
```bash
uvicorn main:app --reload --port 8000
```
- Keep this terminal open to monitor logs

## Managing Webhook Subscriptions

### Check Existing Subscriptions
```bash
curl -G https://www.strava.com/api/v3/push_subscriptions \
    -d client_id=$CLIENT_ID \
    -d client_secret=$CLIENT_SECRET
```

### Delete a Subscription
If you need to delete a subscription (replace {subscription_id} with actual ID):
```bash
curl -X DELETE "https://www.strava.com/api/v3/push_subscriptions/{subscription_id}?client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET"
```

### Create New Subscription
```bash
curl -X POST https://www.strava.com/api/v3/push_subscriptions \
    -F client_id=$CLIENT_ID \
    -F client_secret=$CLIENT_SECRET \
    -F callback_url=https://your-ngrok-url/strava-webhook \
    -F verify_token=$STRAVA_VERIFY_TOKEN
```

## Testing the API

### Test Webhook Endpoint
```bash
curl http://localhost:8000/webhook-test
```
This will:
- Process activity data
- Generate test advice
- Return both success status and generated advice

### Test Streaming Advice Endpoint
```bash
curl -N http://localhost:8000/stream_advice
```
- The `-N` flag enables real-time streaming of the response
- You'll see advice being generated token by token

## Restarting the Service

If you need to restart (e.g., after computer shutdown):

1. Stop both services:
   - FastAPI: Press CTRL+C
   - ngrok: Press CTRL+C

2. Start ngrok (new URL will be generated)
   ```bash
   ngrok http 8000
   ```

3. Start FastAPI
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Create new webhook subscription with new ngrok URL (see "Create New Subscription" above)

## Verifying Webhook Operation

1. Real Activity Test:
   - Upload a new activity to Strava
   - Watch FastAPI logs for webhook trigger
   - You should see:
     - Webhook trigger confirmation
     - Activity processing
     - New advice generation

2. Manual Testing:
   - Use webhook-test endpoint
   - Use stream_advice endpoint
   - Check logs for each operation

## Troubleshooting

### Common Issues:
1. 403 Forbidden:
   - Verify verify_token in .env matches subscription
   - Restart FastAPI server after .env changes

2. Connection Failed:
   - Ensure ngrok is running
   - Check if ngrok URL is current
   - Verify FastAPI server is running

3. Webhook Not Triggering:
   - Check subscription status
   - Verify ngrok tunnel is active
   - Review FastAPI logs for incoming requests

### Verification Steps:
1. Check subscription status using the check subscriptions command
2. Verify ngrok tunnel is active and URL is correct
3. Confirm FastAPI server is running and logs are visible
4. Test webhook endpoint manually
5. Test streaming endpoint manually

## Notes
- ngrok URL changes each time you restart ngrok
- New webhook subscription needed when ngrok URL changes
- Keep both terminals (ngrok and FastAPI) open while operating
- Monitor FastAPI logs for webhook triggers and processing status


