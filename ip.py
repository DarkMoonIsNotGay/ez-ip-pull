import requests
import json
import datetime

# ur webhook url
WEBHOOK_URL = ""

try:
    response = requests.get('https://ifconfig.me/all.json', timeout=10)
    response.raise_for_status()
    API_Data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching API data: {e}")
    exit()

fields = []
for key, value in list(API_Data.items())[:10]:
    fields.append({
        "name": key.replace('_', ' ').title(),
        "value": str(value) if value else "N/A",
        "inline": True
    })


data = {
    "username": "IfConfig Reporter",
    "embeds": [
        {
            "title": "Public Network Information 🌐",
            "description": "Details fetched from ifconfig.me/all.json",
            "color": 3447003,
            "fields": fields,
            "footer": {
                "text": f"Report generated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
        }
    ]
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        print("Message sent successfully!")
    elif response.status_code == 400:
        print("Error 400: Bad Request. The payload is likely too large or improperly formatted.")
        print("Discord Error Response:", response.text)
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")