import pandas as pd
import geoip2.database
import tkinter as tk
from tkinter import ttk  # Import ttk module for themed widgets
from tkinter import filedialog, messagebox
import os
import json

# Define a class to manage the application state
class LogAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.selected_file_path = None
        self.setup_gui()

    def read_logs_into_dataframe(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            if isinstance(data, dict):
                data = [data]
            processed_data = [{
                'timestamp': pd.to_datetime(entry['timestamp'], unit='ms'),
                'action': entry['action'],
                'sourceIP': entry.get('httpRequest', {}).get('clientIp', 'N/A'),
                'country': entry.get('httpRequest', {}).get('country', 'N/A'),
            } for entry in data]
            return pd.DataFrame(processed_data)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading log file: {e}")
            return pd.DataFrame()

    def analyze_logs(self):
        if not self.selected_file_path:
            messagebox.showerror("Error", "Please select a log file first.")
            return
        df = self.read_logs_into_dataframe(self.selected_file_path)
        if df.empty:
            messagebox.showinfo("Analysis Result", "The log file contains no data.")
            return
        # Example analysis function call
        # You can implement more analysis functions and call them here
        messagebox.showinfo("Analysis Complete", "Analysis is complete. Check the output file for details.")
    
    def open_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if filename:
            self.selected_file_path = filename
            messagebox.showinfo("File Selected", f"File selected: {self.selected_file_path}")
    
    def setup_gui(self):
        self.root.title("WAFgenius")
        setup_classic_windows_look(self.root)
        
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        openFileBtn = ttk.Button(mainframe, text="Open Log File", command=self.open_file)
        openFileBtn.grid(column=1, row=1, sticky=tk.W, pady=4)
        
        analyzeBtn = ttk.Button(mainframe, text="Analyze Logs", command=self.analyze_logs)
        analyzeBtn.grid(column=2, row=1, sticky=tk.W, pady=4)

def setup_classic_windows_look(root):
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('TButton', foreground='black', background='#d3d3d3', font=('MS Sans Serif', 10))
    style.configure('TLabel', foreground='black', background='#f0f0f0', font=('MS Sans Serif', 10))
    style.configure('TFrame', background='#f0f0f0')

if __name__ == "__main__":
    root = tk.Tk()
    app = LogAnalyzerApp(root)
    root.mainloop()
