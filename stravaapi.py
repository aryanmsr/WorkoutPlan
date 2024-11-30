from app.data_preprocessing import DataPreprocessor

def main() -> None:
    """
    Main entry point to preprocess Strava activities and save results.
    """
    preprocessor = DataPreprocessor()
    preprocessor.fetch_activities()
    preprocessor.process_run_data()
    preprocessor.calculate_summary_statistics()
    preprocessor.save_to_json('./data/processed_run_data.json', './data/summary_statistics.json')


if __name__ == "__main__":
    main()
