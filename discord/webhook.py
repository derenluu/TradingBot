import requests

def send_log(webhook_url, message):
    data = {"content": message}
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Log sent to Discord successfully!")
            return True
        else:
            print(f"Error sending log: {response.status_code}, {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return False