import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
CHANNEL_HANDLE = "MrBeast"
API_KEY = os.getenv("API_KEY")

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        print("DEBUG JSON:", data)

        channel_items = data["items"][0]
        channel_playlistid = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        return channel_playlistid

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    get_playlist_id()
