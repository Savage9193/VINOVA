import pytz
from datetime import datetime
from tzlocal import get_localzone  
import time  

def handle_time_zone(gui):
    local_tz = get_localzone() 
    current_time = datetime.now(pytz.utc)
    gui.log(f"Current time in UTC is {current_time}")
    localized_time = current_time.astimezone(local_tz)
    gui.log(f"Localized time: {localized_time}")
    gui.log(f"Local time zone: {str(local_tz)}")  


