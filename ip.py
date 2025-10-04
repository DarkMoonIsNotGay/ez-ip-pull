import requests
import json
import datetime

# Your actual webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1422989185588920391/hMxTIPMFiP_MOCBn5mS4X9DSAJijurEJ2sS5N-6XSaBQcZOS9NhAOSGCWQLTKrpwyjqR"

# 1. Get the data
try:
    response = requests.get('https://ifconfig.me/all.json', timeout=10)
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
    API_Data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching API data: {e}")
    exit()

# 2. Build the Embed Payload
# Create a list of fields from the API_Data for a clean presentation
fields = []
# We'll take the first 10 items to keep the embed clean and prevent errors
for key, value in list(API_Data.items())[:10]:
    # Ensure value is a string for the embed field
    fields.append({
        "name": key.replace('_', ' ').title(),  # Title case and remove underscores
        "value": str(value) if value else "N/A",
        "inline": True  # Arrange fields side-by-side
    })


data = {
    "username": "IfConfig Reporter",
    "embeds": [
        {
            "title": "Public Network Information 🌐",
            "description": "Details fetched from ifconfig.me/all.json",
            "color": 3447003, # Blue color
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

# 3. Send the POST request
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