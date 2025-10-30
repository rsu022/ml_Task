import requests

BASE_URL = "http://127.0.0.1:5000"

# JSON data to send
data = {"name": "RSU"}

# Send POST request
try:
    response = requests.post(f"{BASE_URL}/post-name", json=data)
    print("POST /post-name status:", response.status_code)
    print("POST /post-name response:", response.json())
except Exception as e:
    print("Error:", e)
