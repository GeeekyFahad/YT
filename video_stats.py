import requests
import os
from dotenv import load_dotenv
load_dotenv()
CHANNEL_HANDLE = "MrBeast"
API_KEY = os.getenv("API_KEY")
MAX_RESULTS = 50

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

def get_video_id(playlist_id):
    
    video_ids = []
    page_token = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULTS}&playlistId={playlist_id}&key={API_KEY}"

    try:
        while True:
            url = base_url
            if page_token:
                url += f"&pageToken={page_token}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for values in data.get("items", []):
                video_id = values["contentDetails"]["videoId"]
                video_ids.append(video_id)
            
            page_token = data.get("nextPageToken")
            
            if not page_token:
                break
            
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_id(playlist_id)
    print(video_ids)
