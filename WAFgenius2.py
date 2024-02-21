import pandas as pd
import geoip2.database
import tkinter as tk
from tkinter import filedialog, messagebox
import os

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

def main():
    log_file_path = 'path/to/your/logfile.json'  # Update this path to your log file
    df = read_logs_into_dataframe(log_file_path)
    calculate_advanced_metrics(df)  # Call the enhanced function

# GUI Functions
def open_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("json files", "*.json"), ("all files", "*.*")))
    if filename:
        # Here, integrate your logic to read and process the file
        print(f"File selected: {filename}")

def analyze_logs():
    global selected_file_path  # Assumes you have a variable to hold the selected log file path
    if not selected_file_path:
        messagebox.showerror("Error", "Please select a log file first.")
        return
    
    # Read and analyze the log file
    df = read_logs_into_dataframe(selected_file_path)
    if df.empty:
        messagebox.showinfo("Analysis Result", "The selected log file contains no data.")
    else:
        calculate_advanced_metrics(df)
        # Here you might update the application window with analysis results
        # For example, displaying top source IPs, blocked requests, etc., in the GUI.
        messagebox.showinfo("Analysis Complete", "The log analysis is complete. Check the console/output window for details.")

# GUI Setup
app = tk.Tk()
app.title("WAFgenius")

canvas = tk.Canvas(app, height=600, width=800)
canvas.pack()

openFileBtn = tk.Button(app, text="Open Log File", padx=10, pady=5, fg="white", bg="#263D42", command=open_file)
openFileBtn.pack()

analyzeBtn = tk.Button(app, text="Analyze Logs", padx=10, pady=5, fg="white", bg="#263D42", command=analyze_logs)
analyzeBtn.pack()

app.mainloop()
