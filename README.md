# Strava Activity Analysis

A Python application that integrates with the Strava API to fetch and analyze fitness activities, providing insights through modular and maintainable code.

## Features
- Authenticate with Strava API and manage access tokens.
- Fetch recent activities such as runs, rides, or hikes.
- Analyze activities to calculate total distance, average distance, and activity count.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/aryanmsr/WorkoutPlan.git
    cd strava-activity-analysis
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

1. Perform initial authentication to save tokens:
    ```bash
    python app/auth.py
    ```

2. Run the main application:
    ```bash
    python stravaapi.py
    ```

## File Structure

