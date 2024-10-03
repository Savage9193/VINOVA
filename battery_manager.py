import psutil  
from time import sleep
class BatteryManager:
    def __init__(self, gui, activity_tracker):
        self.gui = gui
        self.activity_tracker = activity_tracker  

    def check_battery_status(self):
        while True:
            battery = psutil.sensors_battery()
            if battery is not None:
                percent = battery.percent
                plugged = battery.power_plugged
                self.gui.log(f"Battery: {percent}% {'(Plugged in)' if plugged else '(Not Plugged in)'}")
                if percent < 20 and not plugged:  
                    self.gui.log("Low battery detected! Please plug in your charger.")
                    self.activity_tracker.suspend_tracking()  
                elif percent >= 20 and plugged:  
                    self.activity_tracker.resume_tracking()  
            sleep(60)  
