import requests

def send_log(webhook_url, status_order, type_order, symbol, message):
    data = {
        "embeds": [
            {
                "title": f"{status_order} {type_order} order {symbol}",
                "color": 5793266,  # Red color, can be dynamic based on severity
                "fields": [
                    {
                        "name": "Status",
                        "value": status_order,
                        "inline": False
                    },
                    {
                        "name": "Order Type",
                        "value": type_order,
                        "inline": False
                    },
                    {
                        "name": "Symbol",
                        "value": symbol,
                        "inline": False
                    }
                ]
            }
        ]
    }
    
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
