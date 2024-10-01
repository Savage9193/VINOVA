import requests

# Global Config
screenshot_interval = 5
capture_screenshots = True
screenshot_blurred = False

def update_config_from_server():
    global screenshot_interval, capture_screenshots, screenshot_blurred
    try:
        # Example: Fetch new configuration from a web service
        response = requests.get("https://example.com/get-config")
        if response.status_code == 200:
            config = response.json()
            screenshot_interval = config.get("screenshot_interval", 5)
            capture_screenshots = config.get("capture_screenshots", True)
            screenshot_blurred = config.get("screenshot_blurred", False)
            print("Config updated from server")
    except Exception as e:
        print(f"Failed to update config: {e}")
