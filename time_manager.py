from datetime import datetime
import pytz

def handle_time_zone():
    current_time = datetime.now(pytz.utc)
    print(f"Current time in UTC is {current_time}")

    # Replace 'Asia/Kolkata' with your desired time zone
    local_tz = pytz.timezone('Asia/Kolkata')
    localized_time = current_time.astimezone(local_tz)
    print(f"Localized time: {localized_time}")
