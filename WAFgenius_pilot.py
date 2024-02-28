import pandas as pd
import geoip2.database
import tkinter as tk
from tkinter import ttk  # Import ttk module for themed widgets
from tkinter import filedialog, messagebox
import os
import json

# Global variable to hold the path of the selected log file
selected_file_path = None

def analyze_logs():
    global selected_file_path
    if not selected_file_path:
        messagebox.showerror("Error", "Please select a log file first.")
        return

    # Ensure the file is ready for new data
    open(output_file_path, 'w').close()  # Clear the file before writing new data
    
    # Calls to analysis functions
    calculate_advanced_metrics(df, output_file_path)
    analyze_frequent_terminating_rules(df, output_file_path)
    analyze_top_source_ips_with_geoip(df, output_file_path)  # Updated call
    analyze_time_patterns_of_blocked_requests(df, output_file_path)
    analyze_request_patterns(df, output_file_path)
    analyze_blocked_requests_by_source(df, output_file_path)
    
    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not output_file_path:
        return  # User canceled
    
    df = read_logs_into_dataframe(selected_file_path)
    if df.empty:
        with open(output_file_path, 'w') as file:  # Clear or create the file
            file.write("The log file contains no data.\n")
        messagebox.showinfo("Analysis Result", "The log file contains no data.")
        return
    
    # Ensure the file is ready for new data
    open(output_file_path, 'w').close()  # Clear the file before writing new data
    
    # Calls to analysis functions
    calculate_advanced_metrics(df, output_file_path)
    analyze_frequent_terminating_rules(df, output_file_path)
    lookup_geoip(df, output_file_path)
    analyze_time_patterns_of_blocked_requests(df, output_file_path)
    analyze_frequent_terminating_rules(df, output_file_path)
    analyze_request_patterns(df, output_file_path)
    analyze_blocked_requests_by_source(df, output_file_path)
   
    messagebox.showinfo("Analysis Complete", "The log analysis is complete. Check the output file for details.")

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
                # Add more fields as necessary
            }
            processed_data.append(processed_entry)
        
        # Create DataFrame from processed data
        df = pd.DataFrame(processed_data)
        
        return df
    except Exception as e:
        print(f"Error reading log file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def calculate_advanced_metrics(df, output_path):
    with open(output_path, 'a') as file:  # Append mode
        if df.empty:
            file.write("No data to analyze.\n")
            return
        
        total_requests = len(df)
        allowed_requests = len(df[df['action'] == 'ALLOW'])
        blocked_requests = len(df[df['action'] == 'BLOCK'])
        
        # Write analysis results to file
        file.write(f"Total Requests: {total_requests}\n")
        file.write(f"Allowed Requests: {allowed_requests}\n")
        file.write(f"Blocked Requests: {blocked_requests}\n\n")
    
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

def lookup_geoip(ip_address, db_path='GeoLite2-City.mmdb'):
    try:
        with geoip2.database.Reader(db_path) as reader:
            response = reader.city(ip_address)
            country = response.country.name if response.country.name else "Unknown"
            city = response.city.name if response.city.name else "Unknown"
            return country, city
    except Exception as e:
        print(f"GeoIP lookup error for IP {ip_address}: {e}")
        return "Unknown", "Unknown"

def analyze_top_source_ips_with_geoip(df, output_path, db_path='GeoLite2-City.mmdb'):
    top_source_ips = df['sourceIP'].value_counts().head(5)
    with open(output_path, 'a') as file:
        file.write("Top Source IPs with Geo Location:\n")
        for ip, count in top_source_ips.items():
            country, city = lookup_geoip(ip, db_path)
            file.write(f" - {ip}: {count} requests, Location: {country}, {city}\n")
        file.write("\n")

def analyze_time_patterns_of_blocked_requests(df, output_path):
    with open(output_path, 'a') as file:
        if 'timestamp' in df.columns:
            df_blocked = df[df['action'] == 'BLOCK']
            df_blocked['hour'] = df_blocked['timestamp'].dt.hour
            blocked_requests_by_hour = df_blocked.groupby('hour').size()
            
            file.write("Blocked Requests by Hour:\n")
            for hour, count in blocked_requests_by_hour.iteritems():
                file.write(f" - {hour}: {count} requests\n")
            file.write("\n")

def analyze_frequent_terminating_rules(df, output_path):
    if 'terminatingRuleId' in df.columns:
        top_terminating_rules = df[df['action'] == 'BLOCK']['terminatingRuleId'].value_counts().head(10)
        
        with open(output_path, 'a') as file:
            file.write("Top Terminating Rules for Blocked Requests:\n")
            for rule, count in top_terminating_rules.items():
                file.write(f" - {rule}: {count} times\n")
            file.write("\n")

def analyze_request_patterns(df, output_path):
    with open(output_path, 'a') as file:
        if 'httpRequest' in df.columns:
            df_blocked = df[df['action'] == 'BLOCK']
            methods = df_blocked['httpRequest'].apply(lambda x: x['httpMethod']).value_counts()
            paths = df_blocked['httpRequest'].apply(lambda x: x['uri']).value_counts().head(10)
            
            file.write("Most Common HTTP Methods for Blocked Requests:\n")
            for method, count in methods.items():
                file.write(f" - {method}: {count} requests\n")
            file.write("\nMost Common Request Paths for Blocked Requests:\n")
            for path, count in paths.items():
                file.write(f" - {path}: {count} requests\n")
            file.write("\n")

def analyze_blocked_requests_by_source(df, output_path):
    with open(output_path, 'a') as file:
        if 'httpSourceName' in df.columns:
            blocked_by_source = df[df['action'] == 'BLOCK'].groupby('httpSourceName').size().sort_values(ascending=False)
            
            file.write("Blocked Requests by HTTP Source:\n")
            for source, count in blocked_by_source.iteritems():
                file.write(f" - {source}: {count} requests\n")
            file.write("\n")

def main():
    log_file_path = 'path/to/your/logfile.json'  # Update this path to your log file
    df = read_logs_into_dataframe(log_file_path)
    calculate_advanced_metrics(df, output_file_path)  # Call the enhanced function

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
    
    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not output_file_path:
        return  # User cancelled the save operation
    
    # Proceed with analysis using the selected file path
    df = read_logs_into_dataframe(selected_file_path)
    if df.empty:
        messagebox.showinfo("Analysis Result", "The log file contains no data.")
    else:
        calculate_advanced_metrics(df, output_file_path)
        messagebox.showinfo("Analysis Complete", "The log analysis is complete. Check the console/output window for details.")
    
    # Read and analyze the log file
    df = read_logs_into_dataframe(selected_file_path)
    if df.empty:
        messagebox.showinfo("Analysis Result", "The selected log file contains no data.")
    else:
        calculate_advanced_metrics(df, output_file_path)
        # Here you might update the application window with analysis results
        # For example, displaying top source IPs, blocked requests, etc., in the GUI.
        messagebox.showinfo("Analysis Complete", "The log analysis is complete. Check the console/output window for details.")

def setup_classic_windows_look():
    style = ttk.Style()
    style.theme_use('clam')  # Use the 'clam' theme as a base for a classic look
    
    # Configure the style of widgets
    style.configure('TButton', foreground='black', background='#d3d3d3', font=('MS Sans Serif', 10))
    style.configure('TLabel', foreground='black', background='#f0f0f0', font=('MS Sans Serif', 10))
    style.configure('TFrame', background='#f0f0f0')
    
    # Configure specific widget options if needed
    # For example, button styling
    style.map('TButton',
              foreground=[('pressed', 'red'), ('active', 'blue')],
              background=[('pressed', '!disabled', 'black'), ('active', '#c0c0c0')])
    
    # You can customize this further as per your needs

# GUI Setup
app = tk.Tk()
app.title("WAFgenius")

# Apply the classic Windows look to the entire app
setup_classic_windows_look()

mainframe = ttk.Frame(app, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

openFileBtn = ttk.Button(mainframe, text="Open Log File", command=open_file)
openFileBtn.grid(column=1, row=1, sticky=tk.W, pady=4)

analyzeBtn = ttk.Button(mainframe, text="Analyze Logs", command=analyze_logs)
analyzeBtn.grid(column=2, row=1, sticky=tk.W, pady=4)

# Assuming `open_file` and `analyze_logs` are defined elsewhere in your code

app.mainloop()
