import requests

def get_public_ip():
    try:
        # Use a service like ifconfig.me to get the public IP address
        response = requests.get('https://ifconfig.me/ip')
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error getting IP address: {e}")
        return None

def send_ip_to_discord_webhook(webhook_url, ip_address):
    try:
        # Create JSON payload with the IP address
        payload = {'content': ip_address}

        # Make POST request to Discord webhook
        response = requests.post(webhook_url, json=payload)

        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        print("IP address sent to Discord webhook successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending IP address to Discord webhook: {e}")

if __name__ == "__main__":
    # Replace "YOUR_DISCORD_WEBHOOK_URL" with your actual Discord webhook URL
    webhook_url = "https://discord.com/api/webhooks/1186667780615975113/UUy48ocvN51uMhfvaRyq5Q9mJiIIFeWd1qMTvLyUixa_iZW9JGVgmsm6RbI4KoVPq4jm"

    # Get the public IP address of the machine
    ip_address = get_public_ip()

    if ip_address is not None:
        # Send IP address to Discord webhook
        send_ip_to_discord_webhook(webhook_url, ip_address)
