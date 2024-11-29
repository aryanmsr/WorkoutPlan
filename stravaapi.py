"""
Main script to fetch and analyze Strava data.

This script uses the auth and analysis modules to authenticate
with the Strava API, fetch activities, and perform basic analysis
on the fetched data.
"""

from app.auth import get_strava_client, fetch_activities
from app.analysis import analyze_activities
from dotenv import load_dotenv


def main() -> None:
    """
    Main script to fetch and analyze Strava data.

    Fetches activities using the Strava API and provides analysis
    of the activities including total distance, average distance,
    and activity count.
    """
    # Load environment variables
    load_dotenv()

    try:
        # Authenticate and fetch activities
        client = get_strava_client()
        activities = fetch_activities(client, limit=10)
        print(f"Fetched {len(activities)} activities:")
        for activity in activities:
            print(f"- {activity['name']} ({activity['distance']} meters)")

        # Analyze activities
        analysis = analyze_activities(activities)
        print("\nAnalysis Results:")
        print(f"Total Distance: {analysis['total_distance']} meters")
        print(f"Average Distance: {analysis['average_distance']} meters")
        print(f"Activity Count: {analysis['activity_count']}")

    except RuntimeError as error:
        print(f"Error: {error}")
        print("Please run the authorization process to get initial tokens.")


if __name__ == "__main__":
    main()
