import pandas as pd
import geoip2.database
import tkinter as tk
from tkinter import ttk  # Import ttk module for themed widgets
from tkinter import filedialog, messagebox
import os
import json

# Global variable to hold the path of the selected log file
selected_file_path = None

def read_logs_into_dataframe(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load JSON data
        
        # If the data is a single dictionary, wrap it in a list
        if isinstance(data, dict):
            data = [data]

        # Preprocess and flatten the data as needed
        processed_data = []
        for entry in data:
            # Parse the timestamp and handle the format correctly
            timestamp = pd.to_datetime(entry['@timestamp'].split('.')[0], format='%Y-%m-%d %H:%M:%S')
            
            # Process other fields as needed
            processed_entry = {
                'timestamp': timestamp,
                'action': entry['event.alert.action'],
                'sourceIP': entry['event.src_ip'],
                # Include other fields as necessary
            }
            processed_data.append(processed_entry)
        
        # Create a DataFrame from the processed data
        df = pd.DataFrame(processed_data)
        return df
    except Exception as e:
        print(f"Error reading log file: {e}")
        return pd.DataFrame()


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
        requests_over_time = df.resample('h').size()  # Resampling by hour
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
    # Assumes GeoLite2-City file is in same path as application.
    db_path = 'GeoLite2-City.mmdb'
    try:
        with geoip2.database.Reader(db_path) as reader:
            response = reader.city(ip_address)
            country = response.country.name
            city = response.city.name
            return country, city
    except Exception as e:
        print(f"GeoIP lookup error: {e}")
        return None, None

def analyze_time_patterns_of_blocked_requests(df):
    if 'timestamp' in df.columns:
        df_blocked = df[df['action'] == 'BLOCK']
        df_blocked['hour'] = df_blocked['timestamp'].dt.hour
        blocked_requests_by_hour = df_blocked.groupby('hour').size()
        
        print("Blocked Requests by Hour:")
        print(blocked_requests_by_hour)

def analyze_frequent_terminating_rules(df):
    if 'terminatingRuleId' in df.columns:
        top_terminating_rules = df[df['action'] == 'BLOCK']['terminatingRuleId'].value_counts().head(10)
        
        print("Top Terminating Rules for Blocked Requests:")
        print(top_terminating_rules)

def analyze_request_patterns(df):
    if 'httpRequest' in df.columns:
        df_blocked = df[df['action'] == 'BLOCK']
        methods = df_blocked['httpRequest'].apply(lambda x: x['httpMethod']).value_counts()
        paths = df_blocked['httpRequest'].apply(lambda x: x['uri']).value_counts().head(10)
        
        print("Most Common HTTP Methods for Blocked Requests:")
        print(methods)
        print("\nMost Common Request Paths for Blocked Requests:")
        print(paths)

def analyze_blocked_requests_by_source(df):
    if 'httpSourceName' in df.columns:
        blocked_by_source = df[df['action'] == 'BLOCK'].groupby('httpSourceName').size().sort_values(ascending=False)
        
        print("Blocked Requests by HTTP Source:")
        print(blocked_by_source)

def main():
    log_file_path = 'path/to/your/logfile.json'  # Update this path to your log file
    df = read_logs_into_dataframe(log_file_path)
    calculate_advanced_metrics(df)  # Call the enhanced function

# GUI Functions
def open_file():
    global selected_file_path  # Use the global variable
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("json files", "*.json"), ("all files", "*.*")))
    if filename:
        selected_file_path = filename  # Update the global variable
        print(f"File selected: {selected_file_path}")  # Optional: confirm the selected file path

def analyze_logs():
    global selected_file_path  
    if not selected_file_path:
        messagebox.showerror("Error", "Please select a log file first.")
        return
    
    # Proceed with analysis using the selected file path
    df = read_logs_into_dataframe(selected_file_path)
    if df.empty:
        messagebox.showinfo("Analysis Result", "The log file contains no data.")
    else:
        calculate_advanced_metrics(df)
        messagebox.showinfo("Analysis Complete", "The log analysis is complete. Check the console/output window for details.")

def setup_app_look():
    style = ttk.Style()
    style.theme_use('clam')  # Use the 'clam' theme as a base for a classic look
    
    # style of widgets
    style.configure('TButton', foreground='black', background='#d3d3d3', font=('MS Sans Serif', 10))
    style.configure('TLabel', foreground='black', background='#f0f0f0', font=('MS Sans Serif', 10))
    style.configure('TFrame', background='#f0f0f0')
    
    # button styling
    style.map('TButton',
              foreground=[('pressed', 'red'), ('active', 'blue')],
              background=[('pressed', '!disabled', 'black'), ('active', '#c0c0c0')])

# GUI Setup
app = tk.Tk()
app.title("WAFgenius")

# Apply the style to the entire app
setup_app_look()

mainframe = ttk.Frame(app, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

openFileBtn = ttk.Button(mainframe, text="Open Log File", command=open_file)
openFileBtn.grid(column=1, row=1, sticky=tk.W, pady=4)

analyzeBtn = ttk.Button(mainframe, text="Analyze Logs", command=analyze_logs)
analyzeBtn.grid(column=2, row=1, sticky=tk.W, pady=4)

app.mainloop()

