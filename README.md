# WorkoutPlan

A Python application that integrates with the Strava API to fetch and analyze my fitness activities.

## Features
- Authenticate with Strava API and manage access tokens.
- Fetch recent activities such as runs, rides, or hikes.
- Analyze activities to calculate total distance, average distance, and activity count.

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
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

## Usage

1. Perform initial authentication to save tokens from root dir:
    ```bash
    python -m app.auth
    ```

2. Start the FastAPI server:
    ```bash
    uvicorn stravaapi:app --reload
    ```
    This will stream tokens of fitness advice directly to your terminal. 



