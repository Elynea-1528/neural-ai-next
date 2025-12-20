#!/usr/bin/env python3
"""Neural AI Next - Main GUI Application
Desktop application for data collection monitoring and control.
"""

import os
import subprocess
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

import pytz
import requests


class NeuralAIGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Neural AI Next - Data Collection Monitor")
        self.root.geometry("1400x900")

        # Timezone setup
        self.timezone = pytz.timezone("Europe/Budapest")

        # Collector process
        self.collector_process = None

        # File tree state tracking
        self.last_tree_state = None

        self.create_widgets()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Data Folder", command=self.open_data_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Start Historical Collection", command=self.start_historical)
        tools_menu.add_command(label="View Logs", command=self.view_logs)
        tools_menu.add_command(label="Check Data Status", command=self.check_data_status)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        # Create paned window for resizable panels
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Control and File Tree
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)

        # Control Panel
        control_frame = ttk.LabelFrame(left_frame, text="Control Panel")
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(control_frame, text="Start Collector", command=self.start_collector).pack(
            side=tk.LEFT, padx=5, pady=5
        )
        ttk.Button(control_frame, text="Stop Collector", command=self.stop_collector).pack(
            side=tk.LEFT, padx=5, pady=5
        )
        ttk.Button(control_frame, text="Start Historical", command=self.start_historical).pack(
            side=tk.LEFT, padx=5, pady=5
        )

        # ÚJ GOMB: Trigger Historical Request
        ttk.Button(control_frame, text="Trigger Historical", command=self.trigger_historical).pack(
            side=tk.LEFT, padx=5, pady=5
        )

        # Status Panel
        status_frame = ttk.LabelFrame(left_frame, text="Status")
        status_frame.pack(fill=tk.X, padx=5, pady=5)

        self.collector_status = tk.StringVar(value="Stopped")
        ttk.Label(status_frame, text="Collector:").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.collector_status).pack(side=tk.LEFT, padx=(5, 20))

        self.historical_status = tk.StringVar(value="Idle")
        ttk.Label(status_frame, text="Historical:").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.historical_status).pack(side=tk.LEFT, padx=5)

        # File Tree
        tree_frame = ttk.LabelFrame(left_frame, text="Data Structure")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure tree columns
        self.tree["columns"] = ("Size", "Modified")
        self.tree.column("#0", width=300, minwidth=200)
        self.tree.column("Size", width=100, minwidth=80)
        self.tree.column("Modified", width=150, minwidth=120)

        self.tree.heading("#0", text="File/Folder")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Modified", text="Modified")

        # Right panel - Log Viewer and Data Info
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)

        # Log Viewer
        log_frame = ttk.LabelFrame(right_frame, text="Log Viewer")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Data Info
        info_frame = ttk.LabelFrame(right_frame, text="Data Information")
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        self.info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, height=8)
        self.info_text.pack(fill=tk.X, padx=5, pady=5)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - " + datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S"))
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Start update loops
        self.update_file_tree()
        self.update_logs()
        self.update_status()

    def start_collector(self):
        def run_collector():
            try:
                self.collector_process = subprocess.Popen(
                    ["python", "scripts/run_collector.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                self.collector_status.set("Running")
                self.log_message("Collector started successfully")

                # Read output
                for line in iter(self.collector_process.stdout.readline, ""):
                    self.log_message(line.strip())

            except Exception as e:
                self.log_message(f"Error starting collector: {e}")
                self.collector_status.set("Error")

        threading.Thread(target=run_collector, daemon=True).start()

    def stop_collector(self):
        if self.collector_process:
            self.collector_process.terminate()
            self.collector_process = None
            self.collector_status.set("Stopped")
            self.log_message("Collector stopped")

    def start_historical(self):
        def run_historical():
            try:
                self.historical_status.set("Running")
                self.log_message("Starting historical data collection...")

                # Call the historical collection script
                result = subprocess.run(
                    [
                        "python",
                        "scripts/start_historical_collection.py",
                        "--auto-start",
                    ],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    self.log_message("Historical data collection completed successfully")
                    self.historical_status.set("Completed")
                else:
                    self.log_message(f"Historical collection failed: {result.stderr}")
                    self.historical_status.set("Failed")

            except Exception as e:
                self.log_message(f"Error starting historical collection: {e}")
                self.historical_status.set("Error")

        threading.Thread(target=run_historical, daemon=True).start()

    def trigger_historical(self):
        """Trigger immediate historical data request."""

        def run_trigger():
            try:
                self.historical_status.set("Triggering...")
                self.log_message("Triggering historical request...")

                # HTTP kérés küldése a kollektor API-hoz
                response = requests.post(
                    "http://localhost:8000/api/v1/historical/trigger", timeout=10
                )

                if response.status_code == 200:
                    result = response.json()

                    if result["status"] == "success":
                        job_id = result["job_id"]
                        self.log_message("Historical request triggered successfully")
                        self.log_message(f"Job ID: {job_id}")
                        self.historical_status.set("Triggered")

                        # Frissítsd a job listát
                        self.update_job_list()
                    else:
                        self.log_message(f"Error: {result['message']}")
                        self.historical_status.set("Failed")
                else:
                    self.log_message(f"HTTP Error: {response.status_code}")
                    self.historical_status.set("Failed")

            except requests.exceptions.RequestException as e:
                self.log_message(f"Connection error: {e}")
                self.historical_status.set("Error")
            except Exception as e:
                self.log_message(f"Error: {e}")
                self.historical_status.set("Error")

        threading.Thread(target=run_trigger, daemon=True).start()

    def update_job_list(self):
        """Update the historical job list."""
        try:
            response = requests.get("http://localhost:8000/api/v1/historical/pending", timeout=5)

            if response.status_code == 200:
                result = response.json()
                jobs = result.get("jobs", [])

                # Frissítsd a job listát az info_text-ben
                self.info_text.delete(1.0, tk.END)

                if jobs:
                    self.info_text.insert(tk.END, "Pending Historical Jobs:\n")
                    self.info_text.insert(tk.END, "=" * 50 + "\n")

                    for job in jobs:
                        self.info_text.insert(tk.END, f"Job ID: {job['job_id']}\n")
                        self.info_text.insert(tk.END, f"Symbol: {job['symbol']}\n")
                        self.info_text.insert(tk.END, f"Timeframe: {job['timeframe']}\n")
                        self.info_text.insert(tk.END, f"Status: {job['status']}\n")
                        self.info_text.insert(tk.END, f"Created: {job['created_at']}\n")
                        self.info_text.insert(tk.END, "-" * 50 + "\n")
                else:
                    self.info_text.insert(tk.END, "No pending jobs found\n")
            else:
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(tk.END, f"Error: {response.status_code}\n")

        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Error: {e}\n")

    def view_logs(self):
        log_file = "logs/neural_ai.log"
        if os.path.exists(log_file):
            with open(log_file) as f:
                content = f.read()
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, content)
        else:
            self.log_message("Log file not found")

    def check_data_status(self):
        try:
            data_path = Path("data/warehouse")
            if not data_path.exists():
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(tk.END, "Data warehouse not found!")
                return

            info = []
            for instrument_dir in data_path.iterdir():
                if instrument_dir.is_dir():
                    instrument_name = instrument_dir.name
                    validated_path = instrument_dir / "validated"

                    if validated_path.exists():
                        tick_file = validated_path / f"{instrument_name}_ticks.jsonl"
                        if tick_file.exists():
                            tick_count = sum(1 for _ in open(tick_file))
                            info.append(f"{instrument_name}: {tick_count} ticks")

                        for tf_dir in validated_path.iterdir():
                            if tf_dir.is_dir():
                                ohlcv_files = list(tf_dir.glob("*_ohlcv.csv"))
                                if ohlcv_files:
                                    info.append(f"  {tf_dir.name}: {len(ohlcv_files)} files")

            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "\n".join(info) if info else "No data found")

        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Error checking data: {e}")

    def open_data_folder(self):
        data_path = Path("data")
        if data_path.exists():
            subprocess.run(["xdg-open", str(data_path.absolute())])
        else:
            messagebox.showwarning("Warning", "Data folder not found!")

    def show_about(self):
        about_text = """
Neural AI Next - Data Collection Monitor
Version: 1.0.0

A comprehensive trading data collection system
for machine learning applications.

Features:
- Real-time data collection from MetaTrader 5
- Historical data collection (25 years)
- Data quality validation
- Data warehouse management
- Training dataset generation

Timezone: Europe/Budapest
        """
        messagebox.showinfo("About", about_text)

    def log_message(self, message):
        timestamp = datetime.now(self.timezone).strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def update_file_tree(self):
        try:
            # Csak akkor építsd újra, ha változás történt
            current_state = self.get_tree_state()
            if current_state != self.last_tree_state:
                self.tree.delete(*self.tree.get_children())

                data_path = Path("data")
                if data_path.exists():
                    self.populate_tree("", data_path)

                self.last_tree_state = current_state

        except Exception as e:
            self.log_message(f"Error updating file tree: {e}")

        self.root.after(5000, self.update_file_tree)  # Update every 5 seconds

    def populate_tree(self, parent, path):
        try:
            for item in sorted(path.iterdir()):
                if item.is_dir():
                    # Mappa létrehozása CSUKOTT állapotban (alapértelmezett)
                    node = self.tree.insert(
                        parent, "end", text=item.name, values=("", item.stat().st_mtime)
                    )
                    self.populate_tree(node, item)
                else:
                    size = f"{item.stat().st_size / 1024:.1f} KB"
                    modified = datetime.fromtimestamp(item.stat().st_mtime).strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    self.tree.insert(parent, "end", text=item.name, values=(size, modified))
        except PermissionError:
            pass

    def update_logs(self):
        log_file = Path("logs/neural_ai.log")
        if log_file.exists():
            try:
                with open(log_file) as f:
                    lines = f.readlines()
                    if len(lines) > 100:
                        lines = lines[-100:]
                    content = "".join(lines)

                    if self.log_text.get(1.0, tk.END) != content + "\n":
                        self.log_text.delete(1.0, tk.END)
                        self.log_text.insert(tk.END, content)

            except Exception as e:
                self.log_message(f"Error reading log file: {e}")

        self.root.after(2000, self.update_logs)  # Update every 2 seconds

    def get_tree_state(self):
        """Visszaadja a fájlfa aktuális állapotát."""
        state = []
        try:
            for item in Path("data").rglob("*"):
                state.append((str(item), item.stat().st_mtime if item.exists() else 0))
        except Exception:
            pass
        return tuple(sorted(state))

    def update_status(self):
        # Update collector status
        try:
            response = requests.get("http://localhost:8000/api/v1/health", timeout=1)
            if response.status_code == 200:
                self.collector_status.set("Running")
            else:
                self.collector_status.set("Stopped")
        except:
            self.collector_status.set("Stopped")

        # Update timestamp
        timestamp = datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")
        self.status_var.set(f"Ready - {timestamp}")

        self.root.after(1000, self.update_status)  # Update every 1 second


if __name__ == "__main__":
    app = NeuralAIGUI()
    app.root.mainloop()
