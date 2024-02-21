import pandas as pd

def read_logs_into_dataframe(file_path):
    try:
        # Load logs into a pandas DataFrame
        df = pd.read_json(file_path, lines=True)
        
        # Convert 'timestamp' column to datetime objects for easier analysis
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    except Exception as e:
        print(f"Error reading log file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error