# Workstatus-Python-Agent

# User Activity Monitor

## Overview
The **User Activity Monitor** is a comprehensive Python-based desktop application designed to monitor user activity, capture screenshots, and manage these activities securely. The application periodically captures screenshots, tracks keyboard and mouse activities, checks the battery status, and supports multi-factor authentication (MFA) for secure user login. It integrates with Amazon S3 to store screenshots and includes real-time configuration updates via a Flask-based API.

### Project Structure

- **main.py**:The main GUI application that coordinates activity tracking, screenshot     
      management, authentication, time management and configuration fetching.
- **screenshot_manager.py**: Manages the screenshot capturing, AWS S3 uploads, and configuration updates from the Flask API.
- **auth_manager.py**: Handles multi-factor authentication (MFA) for enhanced security.
- **battery_manager.py**: Detects low battery status and suspends activity tracking to save power.
- **config_updater.py**: Fetches real-time configuration settings (like screenshot interval) from the Flask API.
- **time_manager.py**: Handles the time zone management and logging of current time.
- **app.py**: Flask backend providing configuration values for screenshot intervals, capture enabling, and blurring.

## Features
- **Activity Tracking**: Tracks mouse movement and keypress events in real-time.
- **Screenshot Capture:**  Periodically captures screenshots at configurable intervals, with an option to blur for privacy.
- **AWS S3 Integration**: Automatically uploads screenshots to an Amazon S3 bucket for secure storage. Screenshots are queued for upload if there is no internet connection.
- **Configurable Intervals**: Fetches screenshot interval, capture enable/disable, and blur settings from a Flask-based API.
- **Multi-Factor Authentication (MFA):** Secures the application login with MFA, requiring users to enter a one-time password (OTP) sent to their email.
- **Low Battery Detection:** Monitors the battery status and automatically suspends activity tracking when the battery is low (below 20%).
- **GUI-based Application**: Displays logs of the user's activity, screenshots taken, and configuration updates in real-time with an easy-to-use graphical interface.
- **Real-time Updates**: Activity logs and screenshots are updated every 30 seconds.
- **Time Zone Management**: Logs the current UTC time and converts it to the local time zone, displaying the time information in the application.
- **Error Handling and Resilience**:
- Implement robust error handling to manage scenarios such as:
- **No Internet Connection:** Queue uploads and retry when the connection is restored.
- **Abrupt Disconnection**: Safely handle application shutdowns to ensure data integrity.
- **File Size Management:**
- Compress screenshots before uploading to reduce file size.
- Implement logic to automatically delete or archive old screenshots to prevent
excessive local storage usage.

## Dependencies
The following libraries are required to run the project.

- **boto3**: For AWS S3 integration.
- **schedule**: For identifying the operating system.
- **time**: For managing time-related functions.
- **datetime**: For handling date and time.
- **threading**: For running background tasks concurrently.
- **psutil**: For fetching system and process information.
- **Pillow (PIL)**: For handling image processing, specifically screenshot capture and display.
- **pytz**: For timezone handling.
- **pyotp**: For handling multi-factor authentication.
- **tkinter**: For building the GUI.
- **queue**: For managing the upload queue.
- **requests**: For making HTTP requests to the Flask API.

## Install Dependencies
pip install boto3 Pillow schedule requests psutil datetime threading tkinter queue pyotp pytz datetime time


## AWS Credentials Setup
Before running the application, you need to set up your AWS credentials for boto3 to upload screenshots to your S3 bucket.

1.**Configure AWS credentials using the following command**: **aws configure**
This command will prompt you to enter your AWS Access Key ID, Secret Access Key, Region, and Default Output Format.

2.**AWS Credentials File**: Ensure that your AWS credentials are correctly set up by adding them to the C:\Users\<YourUsername>\.aws\credentials file:

    aws_access_key_id = your_access_key_id
    aws_secret_access_key = your_secret_access_key

Replace your_access_key_id and your_secret_access_key with your actual AWS credentials.


3.**Permissions**: Ensure you have the necessary permissions to write to the specified S3 bucket.


## Environmental Setup

**1**.Flask API: The Flask API serves configuration values for the screenshot intervals, blurring, and capture enabling. To start the Flask server, run:**python app.py**
The Flask API will run on http://127.0.0.1:5000/get-config and will provide configuration settings for the screenshot manager.

## Multi-Factor Authentication (MFA) Setup

This project uses multi-factor authentication (MFA) for securing user login. You need to provide a valid username and password, followed by a one-time password (OTP) sent to your email for verification.



### Steps for MFA Setup:

1.**Login**: Upon starting the application, you will be prompted for your username(tyagi), password(test), and email for OTP(yoursemail.com).
2.**Receive OTP**: An OTP will be sent to your email, and you must enter it to complete authentication.

## Note
- MFA is required for each session to ensure the security of the monitored data.

## run the project
1.Start the Flask API: **python app.py**
2. Run the Main application: **python main.py**


## On first run, you'll be prompted to set up Multi-Factor Authentication (MFA).

### Configuration

During startup, you can configure:
- Whether to capture screenshots
- Whether to blur screenshots
- Screenshot capture interval


In this license is attached please read license....
