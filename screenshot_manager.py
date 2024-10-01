# screenshot_manager.py

import os
import time
import boto3
import schedule
from PIL import ImageGrab, ImageFilter
from datetime import datetime
from activity_tracker import log_summary  # Import log_summary

# AWS S3 Setup
s3 = boto3.client('s3')
BUCKET_NAME = 'your-bucket-name'  # Change this to your actual bucket name

# Global Config
screenshot_interval = 5  # In minutes
capture_screenshots = True
screenshot_blurred = False

def take_screenshot():
    if not capture_screenshots:
        return

    screenshot = ImageGrab.grab()
    
    if screenshot_blurred:
        screenshot = screenshot.filter(ImageFilter.GaussianBlur(15))

    # Save to a local file
    filename = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    screenshot.save(filename)

    # Upload to S3
    upload_to_s3(filename)

    # Optionally delete local file after upload
    os.remove(filename)

def upload_to_s3(file_name):
    try:
        s3.upload_file(file_name, BUCKET_NAME, file_name)
        print(f"Uploaded {file_name} to S3")
    except Exception as e:
        print(f"Error uploading {file_name}: {e}")

def schedule_screenshots():
    schedule.every(screenshot_interval).minutes.do(take_screenshot)
    schedule.every(1).minutes.do(log_summary)  # Log activity summary every minute
    while True:
        schedule.run_pending()
        time.sleep(1)
