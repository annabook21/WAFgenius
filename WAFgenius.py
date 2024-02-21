import pandas as pd
import geoip2.database

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
        
        def calculate_advanced_metrics(df):
    if df.empty:
        print("No data to analyze.")
        return
    
    # Continue with basic metrics
    total_requests = len(df)
    allowed_requests = len(df[df['action'] == 'ALLOW'])
    blocked_requests = len(df[df['action'] == 'BLOCK'])
    print(f"Total Requests: {total_requests}")
    print(f"Allowed Requests: {allowed_requests}")
    print(f"Blocked Requests: {blocked_requests}")

    # Top Source IP Analysis
    top_source_ips = df['sourceIP'].value_counts().head(5)  # Adjust column name if necessary
    print("\nTop Source IPs:")
    for ip, count in top_source_ips.items():
        print(f" - {ip}: {count} requests")

    # Rule Trigger Analysis
    if 'terminatingRuleId' in df.columns:  # Adjust if using a different column for rules
        top_rules_triggered = df['terminatingRuleId'].value_counts().head(5)
        print("\nTop Rules Triggered:")
        for rule, count in top_rules_triggered.items():
            print(f" - {rule}: {count} times")

    # Time Analysis (requests over time)
    if 'timestamp' in df.columns:
        df.set_index('timestamp', inplace=True)
        requests_over_time = df.resample('H').size()  # Resampling by hour
        print("\nRequests Over Time (Hourly):")
        for time, count in requests_over_time.items():
            print(f" - {time}: {count} requests")
            
            # Top Source IPs with GeoIP
   top_source_ips = df['sourceIP'].value_counts().head(5)
    print("\nTop Source IPs with Geo Location:")
    for ip, count in top_source_ips.items():
        country, city = lookup_geoip(ip)
        print(f" - {ip}: {count} requests, Location: {country}, {city}")
            
            def main():
    log_file_path = 'path/to/your/logfile.json'  # Update this path to your log file
    df = read_logs_into_dataframe(log_file_path)
    calculate_advanced_metrics(df)  # Call the enhanced function
    
def lookup_geoip(ip_address):
    # Adjust the path to your GeoLite2 database file
    db_path = 'path/to/GeoLite2-City.mmdb'
    try:
        with geoip2.database.Reader(db_path) as reader:
            response = reader.city(ip_address)
            country = response.country.name
            city = response.city.name
            return country, city
    except Exception as e:
        print(f"GeoIP lookup error: {e}")
        return None, None
