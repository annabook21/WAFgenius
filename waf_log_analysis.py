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
        
        def calculate_basic_metrics(df):
    if df.empty:
        print("No data to analyze.")
        return

    total_requests = len(df)
    allowed_requests = len(df[df['action'] == 'ALLOW'])
    blocked_requests = len(df[df['action'] == 'BLOCK'])
    
    # Adjust the following line based on your log structure
    # For example, if you're interested in a different metric, modify accordingly
    threat_types = df['terminatingRuleType'].value_counts().to_dict()
    
    print(f"Total Requests: {total_requests}")
    print(f"Allowed Requests: {allowed_requests}")
    print(f"Blocked Requests: {blocked_requests}")
    print("Threat Types Detected:")
    for threat, count in threat_types.items():
        print(f" - {threat}: {count}")
        
        def main():
    log_file_path = 'path/to/your/logfile.json'  # Update this path to your log file
    df = read_logs_into_dataframe(log_file_path)
    calculate_basic_metrics(df)

if __name__ == "__main__":
    main()