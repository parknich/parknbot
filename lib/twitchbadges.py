import requests
import config
# Twitch API endpoint URLs
TWITCH_API_URL = "https://api.twitch.tv/helix"
BADGES_ENDPOINT = "/chat/badges"

# Twitch API credentials
CLIENT_ID = config.clientid
CLIENT_SECRET = config.clientsecret

# OAuth token
OAUTH_TOKEN = config.parknich_access_token

# Channel username for which you want to fetch badges
channel_username = "hubalubalu"



# Function to fetch badges for a specific channel
# Function to get channel ID using username
def __get_channel_id(username):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {OAUTH_TOKEN}"
    }
    params = {
        "login": username
    }
    response = requests.get(TWITCH_API_URL + "/users", headers=headers, params=params)
    # print(response.url)  # Debugging: Print the URL being requested
    # print(response.text)  # Debugging: Print the response text
    
    if response.status_code == 200:
        data = response.json().get("data", [])
        if data:
            return data[0]["id"]
        else:
            print("No user data found.")
            return None
    else:
        print(f"Failed to fetch channel ID: {response.text}")
        return None

# Fetch badges for the specified channel
def __get_channel_badges(channel_username):
    channel_id = __get_channel_id(channel_username)
    if channel_id:
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {OAUTH_TOKEN}"
        }
        params = {
            "broadcaster_id": channel_id
        }
        response = requests.get(TWITCH_API_URL + BADGES_ENDPOINT, headers=headers, params=params)
        #print(response.url)  # Debugging: Print the URL being requested
        #print(response.text)  # Debugging: Print the response text

        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch badges: {response.text}")
            return None
    else:
        print("Failed to fetch channel ID.")
        return None


def get_badge_json():
    # Fetch badges for the specified channel
    badges_data = __get_channel_badges(channel_username)
    if badges_data:
        print(badges_data)  # Debugging: Print the retrieved badges data
    else:
        print("Failed to fetch badges.")

print(__get_channel_id('parknbot'))