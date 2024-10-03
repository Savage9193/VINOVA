import ctypes
import sys
import tkinter as tk
import threading
from time import sleep
import requests
import psutil
from activity_tracker import start_activity_tracking
from screenshot_manager import schedule_screenshots, process_upload_queue
from config_updater import fetch_config
from time_manager import handle_time_zone
from battery_manager import BatteryManager
from auth_manager import AuthManager
from tkinter import simpledialog

class SingleInstance:
    def __init__(self, mutex_name):
        self.mutex_name = mutex_name
        self.mutex = None

    def acquire_lock(self):
        self.mutex = ctypes.windll.kernel32.CreateMutexW(None, False, self.mutex_name)
        if ctypes.GetLastError() == 183:
            return False
        return True

    def release_lock(self):
        if self.mutex:
            ctypes.windll.kernel32.ReleaseMutex(self.mutex)

MUTEX_NAME = "Global\\MyAppMutex"

class RedirectedOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

class TrackingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Activity Tracking Dashboard")
        self.geometry("800x600")

        self.log_display = tk.Text(self, height=50, width=100)
        self.log_display.pack(pady=20)

        sys.stdout = RedirectedOutput(self.log_display)
        sys.stderr = RedirectedOutput(self.log_display)
        
        
        self.auth_manager = AuthManager() 
        self.tracking_suspended = False
        
        self.login_user() #*++

    def login_user(self):
        self.username = simpledialog.askstring("Username", "Enter your username:")
        self.password = simpledialog.askstring("Password", "Enter your password:", show='*')
        self.email = simpledialog.askstring("Email", "Enter your email for OTP:")

        if self.auth_manager.login(self.username, self.password, self.email):
            self.prompt_for_otp()
        else:
            self.log("Invalid username or password.")

    def prompt_for_otp(self):
        user_otp = simpledialog.askstring("OTP", "Enter the OTP sent to your email:")
        if self.auth_manager.verify_otp(user_otp):
            self.log("Login successful!")
            self.start_tracking()
        else:
            self.log("Invalid OTP. Login failed.")

    def start_tracking(self):
        threading.Thread(target=self.run_activity_tracking).start()
        threading.Thread(target=self.run_screenshot_scheduling).start()
        threading.Thread(target=self.run_config_updater).start()
        threading.Thread(target=self.run_time_manager).start()
        threading.Thread(target=process_upload_queue, args=(self,), daemon=True).start()
        threading.Thread(target=self.check_battery_status, daemon=True).start()

    def log(self, message):
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.see(tk.END)

    def run_activity_tracking(self):
        while True:
            if not self.tracking_suspended:
                start_activity_tracking(self)
            else:
                sleep(5)

    def run_screenshot_scheduling(self):
        schedule_screenshots(self)

    def run_config_updater(self):
        # while True:
        #     fetch_config(self)  # Pass the GUI instance to fetch_config
        #     sleep(17)  # Fetch every 30 seconds
        pass

    def run_time_manager(self):
        while True:
            handle_time_zone(self)
            sleep(15)

    def check_battery_status(self):
        battery_manager = BatteryManager(self, self)
        battery_manager.check_battery_status()

    def suspend_tracking(self):
        self.tracking_suspended = True

    def resume_tracking(self):
        self.tracking_suspended = False

if __name__ == "__main__":
    instance = SingleInstance(MUTEX_NAME)
    if not instance.acquire_lock():
        print("Another instance of the application is already running.")
        sys.exit(1)

    try:
        app = TrackingApp()
        app.mainloop()
    finally:
        instance.release_lock()
