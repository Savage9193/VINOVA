import os
import time
import boto3
import schedule
from PIL import ImageGrab, ImageFilter
from datetime import datetime
import requests
import queue
import threading
from config_updater import fetch_config

s3 = boto3.client('s3')
BUCKET_NAME = 'savage-1234'

TEMP_DIR = "temp_screenshots"

upload_queue = queue.Queue()
upload_thread_active = True

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

screenshot_interval = 15
capture_screenshots = True
screenshot_blurred = False

class ConfigManager:
    def __init__(self, gui):
        self.config_url = 'http://127.0.0.1:5000/get-config'
        self.gui = gui
        self.current_config = {}

    def fetch_config(self):
        try:
            response = requests.get(self.config_url)
            if response.status_code == 200:
                self.current_config = response.json()
                self.apply_config()
            else:
                self.gui.log(f"Failed to fetch configuration: HTTP {response.status_code}")
        except requests.RequestException as e:
            self.gui.log(f"Failed to fetch configuration: {e}")

    def apply_config(self):
        global screenshot_interval, screenshot_blurred, capture_screenshots
        screenshot_interval = self.current_config.get('screenshot_interval', 15)
        screenshot_blurred = self.current_config.get('screenshot_blurred', False)
        capture_screenshots = self.current_config.get('capture_screenshots', True)
        self.gui.log(f"Applied config: Interval={screenshot_interval} seconds, Blurred={screenshot_blurred}, Capture Enabled={capture_screenshots}")

    def start_polling(self):
        while True:
            self.fetch_config()
            time.sleep(60)

def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def upload_to_s3(file_name, gui):
    print(f"Attempting to upload {file_name} to S3...")
    try:
        if os.path.getsize(file_name) > 5 * 1024 * 1024:
            multipart_upload(file_name, gui)
        else:
            s3.upload_file(file_name, BUCKET_NAME, file_name, ExtraArgs={'ServerSideEncryption': 'AES256'})
            gui.log(f"Uploaded {file_name} to S3 successfully.")
        return True
    except Exception as e:
        gui.log(f"Error uploading {file_name}: {e}")
        return False

def multipart_upload(file_name, gui):
    try:
        response = s3.create_multipart_upload(Bucket=BUCKET_NAME, Key=file_name, ServerSideEncryption='AES256')
        upload_id = response['UploadId']
        parts = []

        with open(file_name, 'rb') as f:
            part_number = 1
            while True:
                data = f.read(5 * 1024 * 1024)
                if not data:
                    break
                part_response = s3.upload_part(Bucket=BUCKET_NAME, Key=file_name, PartNumber=part_number, UploadId=upload_id, Body=data)
                parts.append({'ETag': part_response['ETag'], 'PartNumber': part_number})
                gui.log(f"Uploaded part {part_number}")
                part_number += 1

        s3.complete_multipart_upload(Bucket=BUCKET_NAME, Key=file_name, UploadId=upload_id, MultipartUpload={'Parts': parts})
        gui.log(f"Completed multipart upload for {file_name}.")
    except Exception as e:
        gui.log(f"Failed multipart upload for {file_name}: {e}")

def take_screenshot(gui):
    if not capture_screenshots:
        return

    screenshot = ImageGrab.grab()

    if screenshot_blurred:
        screenshot = screenshot.filter(ImageFilter.GaussianBlur(15))

    filename = os.path.join(TEMP_DIR, f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
    screenshot.save(filename)

    gui.log(f"Screenshot taken: {filename}")
    gui.log("Applied configuration... ")

    config = fetch_config(gui)
    if config:
        gui.log(f"Config fetched: Interval={config['screenshot_interval']}, Capture={config['capture_screenshots']}, Blurred={config['screenshot_blurred']}")

    if check_internet_connection():
        gui.log("Starting upload to S3...")
        if upload_to_s3(filename, gui):
            os.remove(filename)
        else:
            gui.log(f"Failed to upload {filename}. Adding to upload queue.")
            upload_queue.put(filename)
    else:
        gui.log("No internet connection. Adding to upload queue.")
        upload_queue.put(filename)

def process_upload_queue(gui):
    while upload_thread_active:
        if not upload_queue.empty():
            file_name = upload_queue.get()
            gui.log(f"Retrying upload for {file_name}...")
            while not upload_to_s3(file_name, gui):
                gui.log(f"Retrying upload for {file_name} after failure...")
                time.sleep(5)
            os.remove(file_name)
        time.sleep(1)

def schedule_screenshots(gui):
    schedule.every(screenshot_interval).seconds.do(lambda: take_screenshot(gui))
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_screenshot_manager(gui):
    config_manager = ConfigManager(gui)
    threading.Thread(target=config_manager.start_polling, daemon=True).start()

    threading.Thread(target=schedule_screenshots, args=(gui,), daemon=True).start()
    threading.Thread(target=process_upload_queue, args=(gui,), daemon=True).start()
