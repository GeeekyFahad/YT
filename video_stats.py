import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

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
          
def extract_video_data(video_ids):
    extracted_data = []
    def batch_list(video_id_lst, batch_size):
        for video_id in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[video_id : video_id + batch_size]
    try:
        for batch in batch_list(video_ids, MAX_RESULTS):
            video_ids_str = ','.join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get("items", []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]
                video_data = {
                    "video_id": video_id,
                    "title": snippet.get("title"),
                    "publishedAt": snippet.get("publishedAt"),
                    "duration": contentDetails.get("duration"),
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None),
                }
                extracted_data.append(video_data)
        return extracted_data
    except requests.exceptions.RequestException as e:
        raise e
    
def save_to_json(extracted_data):
    file_path = f"./data/video_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(file_path, 'w') as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    if not API_KEY:
        raise ValueError("API_KEY not found. Check your .env file or environment variables.")
    playlist_id = get_playlist_id()
    video_ids = get_video_id(playlist_id)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)
