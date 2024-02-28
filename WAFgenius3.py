import pandas as pd
import geoip2.database
import tkinter as tk
from tkinter import ttk  # Import ttk module for themed widgets
from tkinter import filedialog, messagebox
import json

# Global variable to hold the path of the selected log file
selected_file_path = None

def read_logs_into_dataframe(file_path):
    try:
        # Load the entire JSON file content
        with open(file_path, 'r') as file:
            data = json.load(file)  # Assuming the file contains an array of objects
        
        # If the data is a single dictionary (i.e., one log entry), wrap it in a list
        if isinstance(data, dict):
            data = [data]

        # Preprocess and flatten the data as needed
        processed_data = []
        for entry in data:
            # Example of extracting specific fields and handling nested data
            processed_entry = {
                'timestamp': pd.to_datetime(entry['timestamp'], unit='ms'),
                'action': entry['action'],
                'sourceIP': entry['httpRequest']['clientIp'],
                'country': entry['httpRequest']['country'],
            }
            processed_data.append(processed_entry)
        
        # Create DataFrame from processed data
        df = pd.DataFrame(processed_data)
        
        return df
    except Exception as e:
        print(f"Error reading log file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def calculate_advanced_metrics(df):
    if df.empty:
        print("No data to analyze.")
        return
    
    # Basic metrics
    total_requests = len(df)
    allowed_requests = len(df[df['action'] == 'ALLOW'])
    blocked_requests = len(df[df['action'] == 'BLOCK'])
    print(f"Total Requests: {total_requests}")
    print(f"Allowed Requests: {allowed_requests}")
    print(f"Blocked Requests: {blocked_requests}")

    # Top Source IP Analysis
    top_source_ips = df['sourceIP'].value_counts().head(5)
    print("\nTop Source IPs:")
    for ip, count in top_source_ips.items():
        print(f" - {ip}: {count} requests")

    # Rule Trigger Analysis
    if 'terminatingRuleId' in df.columns:
        top_rules_triggered = df['terminatingRuleId'].value_counts().head(5)
        print("\nTop Rules Triggered:")
        for rule, count in top_rules_triggered.items():
            print(f" - {rule}: {count} times")

    # Time Analysis (requests over time)
    if 'timestamp' in df.columns:
        df.set_index('timestamp', inplace=True)
        requests_over_time = df.resample('H').size()  # Corrected to 'H' for hourly resampling
        print("\nRequests Over Time (Hourly):")
        for time, count in requests_over_time.items():
            print(f" - {time}: {count} requests")

    # Top Source IPs with GeoIP
    print("\nTop Source IPs with Geo Location:")
    for ip, count in top_source_ips.items():
        country, city = lookup_geoip(ip)
        print(f" - {ip}: {count} requests, Location: {country if country else 'Unknown'}, {city if city else 'Unknown'}")

def lookup_geoip(ip_address):
    db_path = 'GeoLite2-City.mmdb'  # Ensure this path points to your GeoLite2 database
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

def analyze_frequent_terminating_rules(df, output_path='analysis_output.txt'):
    if 'terminatingRuleId' in df.columns:
        top_terminating_rules = df[df['action'] == 'BLOCK']['terminatingRuleId'].value_counts().head(10)
        
        with open(output_path, 'w') as file:
            file.write("Top Terminating Rules for Blocked Requests:\n")
            for rule, count in top_terminating_rules.items():
                file.write(f" - {rule}: {count} times\n")

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

def open_file():
    global selected_file_path
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("json files", "*.json"), ("all files", "*.*")))
    if filename:
        selected_file_path = filename
        print(f"File selected: {selected_file_path}")  # Confirm the selected file path


def setup_classic_windows_look():
    style = ttk.Style()
    style.theme_use('clam')  # Set the theme to 'clam' for a classic look
    
    # Configure the style for buttons
    style.configure('TButton', foreground='black', background='#d3d3d3', font=('MS Sans Serif', 10), borderwidth=1)
    style.map('TButton',
              foreground=[('pressed', 'red'), ('active', 'blue')],
              background=[('pressed', '!disabled', 'black'), ('active', '#c0c0c0')])
    
    # Configure the style for labels
    style.configure('TLabel', foreground='black', background='#f0f0f0', font=('MS Sans Serif', 10))
    
    # Configure the style for frames
    style.configure('TFrame', background='#f0f0f0')

app = tk.Tk()
app.title("WAFgenius")

setup_classic_windows_look()

mainframe = ttk.Frame(app, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

openFileBtn = ttk.Button(mainframe, text="Open Log File", padx=10, pady=5, fg="white", bg="#263D42", command=open_file)
openFileBtn.pack()

analyzeBtn = ttk.Button(mainframe, text="Analyze Logs", padx=10, pady=5, fg="white", bg="#263D42", command=analyze_logs)
analyzeBtn.pack()

saveResultsBtn = ttk.Button(app, text="Save Results", padx=10, pady=5, fg="white", bg="#263D42", command=save_analysis_results)
saveResultsBtn.pack()

app.mainloop()
