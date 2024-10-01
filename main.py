import threading
from activity_tracker import start_activity_tracking
from screenshot_manager import schedule_screenshots
from config_updater import update_config_from_server
from time_manager import handle_time_zone

def main():
    print("Starting agent...")

    # Start tracking activity
    activity_thread = threading.Thread(target=start_activity_tracking)
    activity_thread.start()

    # Start taking screenshots
    screenshot_thread = threading.Thread(target=schedule_screenshots)
    screenshot_thread.start()

    # Periodically update configuration from a server
    update_thread = threading.Thread(target=update_config_from_server)
    update_thread.start()

    # Monitor time zone changes
    handle_time_zone()

    activity_thread.join()
    screenshot_thread.join()
    update_thread.join()


if __name__ == '__main__':
    main()
