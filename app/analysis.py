"""
Module for analyzing Strava activity data.

This script contains functionality to analyze activities fetched
from the Strava API, providing metrics such as total distance,
average distance, and activity count.
"""

from typing import List, Dict


def analyze_activities(activities: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Perform basic analysis on activities.

    Args:
        activities (List[Dict[str, float]]): A list of activity data, 
            where each activity is a dictionary with keys like 'distance'.

    Returns:
        Dict[str, float]: A dictionary containing the total distance,
            average distance, and activity count.
    """
    total_distance = sum(activity['distance'] for activity in activities)
    avg_distance = total_distance / len(activities) if activities else 0

    return {
        "total_distance": total_distance,
        "average_distance": avg_distance,
        "activity_count": len(activities)
    }
