"""
Data Preprocessing Script for Strava Activities - mainly runs.

This script encapsulates functionality for fetching activity data from the Strava API,
preprocessing it to generate a semi-structured dataset for run activities,
and computing summary statistics. The processed data and statistics are saved in JSON format
for further use.
"""

import pandas as pd
from app.auth import get_strava_client
from typing import List, Dict, Any


class DataPreprocessor:
    """
    Class for preprocessing Strava activity data and generating summary statistics.
    """

    def __init__(self):
        """
        Initialize the DataPreprocessor with Strava API client and empty data attributes.
        """
        self.client = get_strava_client()
        self.activities = []
        self.run_df = pd.DataFrame()
        self.summary_stats = pd.DataFrame()

    def fetch_activities(self) -> None:
        """
        Fetch activities from the Strava API.

        Parameters:
        - limit (int): Maximum number of activities to fetch (default: 100).
        """
        self.activities = self.client.get_activities()
        print(f"Fetched activities.")

    def process_run_data(self) -> pd.DataFrame:
        """
        Process activity data for 'Run' activities.

        Returns:
        - pd.DataFrame: Processed DataFrame containing unit-converted 'Run' activities.
        """
        activity_data = []
        for activity in self.activities:
            activity_data.append({
                'id': activity.id,
                'name': activity.name,
                'type': activity.type,
                'distance': activity.distance,  # In meters
                'moving_time': activity.moving_time,  # In seconds
                'elapsed_time': activity.elapsed_time,  # In seconds
                'total_elevation_gain': activity.total_elevation_gain,  # In meters
                'start_date': activity.start_date,
                'average_speed': activity.average_speed,  # Speed in m/s
                'max_speed': activity.max_speed if activity.max_speed else None,
                'average_cadence': activity.average_cadence,
                'average_heartrate': activity.average_heartrate,
                'weighted_average_watts': activity.weighted_average_watts,
                'kudos_count': activity.kudos_count,
                'max_heartrate': activity.max_heartrate,
                'suffer_score': activity.suffer_score,
                'calories': activity.kilojoules if activity.kilojoules else None,
            })

        df = pd.DataFrame(activity_data)

        df['start_date'] = pd.to_datetime(df['start_date'])
        run_df = df[df['type'] == 'Run'].copy()

        run_df['distance_km'] = run_df['distance'] / 1000
        run_df['moving_time_min'] = run_df['moving_time'] / 60
        run_df['elapsed_time_min'] = run_df['elapsed_time'] / 60
        run_df['average_speed_kmh'] = run_df['average_speed'] * 3.6
        run_df['max_speed_kmh'] = run_df['max_speed'] * 3.6

        run_df['pace_min_per_km'] = run_df['moving_time_min'] / run_df['distance_km']
        run_df['speed_diff_kmh'] = run_df['max_speed_kmh'] - run_df['average_speed_kmh']
        run_df['rest_time_min'] = run_df['elapsed_time_min'] - run_df['moving_time_min']
        run_df['type'] = run_df['type'].astype(str)

        columns_to_keep = [
            'id', 'name', 'type', 'start_date', 'distance_km', 'moving_time_min',
            'elapsed_time_min', 'total_elevation_gain', 'average_speed_kmh', 'kudos_count',
            'max_speed_kmh', 'pace_min_per_km', 'speed_diff_kmh', 'rest_time_min'
        ]
        self.run_df = run_df[columns_to_keep]
        return self.run_df

    def calculate_summary_statistics(self) -> pd.DataFrame:
        """
        Calculate summary statistics for 'Run' activities.

        Returns:
        - pd.DataFrame: Summary statistics DataFrame.
        """
        self.summary_stats = self.run_df.groupby('type').agg(
            total_activities=('id', 'count'),
            avg_distance_km=('distance_km', 'mean'),
            avg_moving_time_min=('moving_time_min', 'mean'),
            avg_pace_min_per_km=('pace_min_per_km', 'mean'),
            total_distance_km=('distance_km', 'sum'),
            total_moving_time_min=('moving_time_min', 'sum'),
        ).reset_index()
        return self.summary_stats

    def save_to_json(self, processed_file: str, summary_file: str) -> None:
        """
        Save processed data and summary statistics to JSON files.

        Parameters:
        - processed_file (str): File name for processed data JSON.
        - summary_file (str): File name for summary statistics JSON.
        """
        processed_json = self.run_df.to_json(orient='records', date_format='iso', indent=4)
        with open(processed_file, 'w') as file:
            file.write(processed_json)
        print(f"Processed data saved to '{processed_file}'.")

        summary_json = self.summary_stats.to_json(orient='records', date_format='iso', indent=4)
        with open(summary_file, 'w') as file:
            file.write(summary_json)
        print(f"Summary statistics saved to '{summary_file}'.")
