<b>Activity Tracker Agent</b>

Overview

The Activity Tracker Agent is a Python-based program that runs in the background on a user's machine to track system activity. It captures screenshots at configurable intervals, tracks user inputs, and uploads activity data to AWS S3. It also monitors timezone changes and handles other configurable options such as blurring screenshots.

<b>Group Members: </b>  
<b>Anjali Chaudhary (Group Leader)</b>  
<b>Mohd shahvez tyagi, </b>
<b>Shaurya gahlot,</b>
<b>Aditya gupta </b>

<b>Features</b>

Activity Tracking:

Detect genuine user inputs and discard scripted activities (e.g., irregular mouse movement or unnatural keyboard inputs).
Configurable Screenshot Intervals: Screenshots can be taken at configurable intervals (e.g., every 5 or 10 minutes). Users can enable/disable screenshots and toggle between blurred/unblurred captures.
Time Zone Management: Detects timezone changes and updates logs accordingly.
Cloud Data Upload: Automatically uploads screenshots and activity logs to AWS S3 with compression and encryption.
Error Handling and Resilience: Robust error handling for scenarios like no internet connection, abrupt disconnection, or firewall restrictions.
Instance Management: Prevents multiple instances of the agent from running simultaneously using a lock file.

Libraries Used

The following libraries are required to run the Activity Tracker Agent:

Pillow: For taking screenshots and image processing (blurring, compression).
Boto3: AWS SDK for Python to interface with AWS services like S3.
Pytz: For timezone handling.
Psutil: For tracking user activity such as CPU usage, memory, and disk IO.
Logging: Native Python logging module for event logging.
To install these dependencies, run:

bash
Copy code
pip install -r requirements.txt
AWS Platform Usage
This project utilizes AWS S3 for cloud storage of screenshots. Here's a breakdown of how AWS services are integrated:

Amazon S3:

Stores the captured screenshots securely in the cloud.
Uploaded files are compressed and encrypted before storage.
Provides a scalable storage solution for managing large data uploads.
IAM (Identity and Access Management):

The application uses an IAM user with programmatic access (access key and secret key) to upload files to S3. Ensure that you have set up your AWS credentials properly in the config.ini file.
AWS Security:

Always follow best practices for managing AWS keys. Avoid using long-term keys for production and use roles or short-term credentials wherever possible.
In this project, bucket policies can be used to enforce permissions on the uploaded files. Ensure that your S3 bucket policies and ACLs prevent unwanted public access.
Configuration
The agent configuration is handled through a config.ini file:

ini
Copy code
[settings]
screenshot_interval = 5
screenshot_blur = False
aws_access_key = YOUR_AWS_ACCESS_KEY
aws_secret_key = YOUR_AWS_SECRET_KEY
bucket_name = your-s3-bucket-name
Configurable Parameters
screenshot_interval: Time (in minutes) between screenshots.
screenshot_blur: Boolean value (True or False) to determine if screenshots should be blurred before upload.
aws_access_key & aws_secret_key: AWS credentials for accessing S3.
bucket_name: The name of the S3 bucket where the screenshots will be uploaded.
The agent listens for configuration updates and applies changes in real time.

Project Structure
bash
Copy code
VINOVA/
│
├── app.py # Firstly run the server (Python app.py)
├── main.py # Run the main.py to initialise project
├── activity_tracker.py # No Need to Run manually. This for user activity tracking
├── auth_manager.py # No Need to Run manually. Handling Authentication using MFA
├── battery_manager.py # No Need to Run manually. Manage battery status
├── config_updater.py # No Need to Run manually. fetch configuration
├── screenshot_manager.py # No Need to Run manually. Managing --taking screenshot uploading to s3 aws and resize big photo and check blurred screenshot.
├── time_manager.py # No Need to Run manually. Manages timezone locally and UTC
└── requirements.txt # List of project dependencies.
<b>After succesfully run you have to login with username ="tyagi" then password =test and then enter your email for otp ...check your email and enter otp then you got UI to see agent woking ....</b>
Code Patterns
The project follows a modular design with the following patterns:

Separation of Concerns: Each Python file is responsible for a specific functionality (e.g., tracker.py for tracking, uploader.py for AWS interactions).
Background Processes: The agent runs in the background, tracking activity and taking screenshots without interrupting the user's workflow.
Threading: Timezone changes and configuration updates are handled in separate background threads to ensure the main process remains uninterrupted.
Error Handling: Exception handling is integrated into all file uploads and activities to ensure graceful degradation in case of errors.
Single Instance Enforcement: A lock file mechanism prevents multiple instances of the agent from running simultaneously.
Running the Project
Prerequisites
Ensure you have Python 3.x installed on your system. Install the required dependencies by running:

bash
Copy code
pip install -r requirements.txt
firstly run app.py (using python app.py)
bash
Copy code
python main.py
The agent will run in the background, tracking activity and uploading screenshots to the specified S3 bucket. Press Ctrl+C to stop the agent.

Error Handling & Resilience
No Internet Connection: If the internet connection is lost, the agent queues uploads and retries when the connection is restored.
Firewall Issues: The agent detects when uploads are blocked due to firewall settings and logs relevant errors.
Abrupt Disconnections: If the agent is stopped abruptly (e.g., power outage), it attempts to recover and resume from where it left off.
File Integrity: Ensures data is compressed before upload to reduce size and maintain file integrity.
Security Considerations
AWS Credentials: Avoid hardcoding AWS credentials directly in your code. Use IAM roles, environment variables, or external configuration files like config.ini.
Secure Uploads: Data is encrypted during transit to S3 using secure protocols like HTTPS.
Access Control: Apply strict access controls to your S3 bucket to avoid public access to sensitive data. Ensure that sensitive information is stored securely and appropriately managed.
License
This project is licensed under the MIT License. See the LICENSE file for details.
