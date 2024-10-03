import requests

def fetch_config(gui):
    try:
        response = requests.get("http://127.0.0.1:5000/get-config")
        if response.status_code == 200:
            config = response.json()
            return config 
        else:
            return None 
    except Exception as e:
        return None  
