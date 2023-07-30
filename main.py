import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth  
from spotipy import Spotify 
from pytube import YouTube
from googleapiclient.discovery import build

def get_track_names():
    track_names = []
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        artist = track['track']['artists'][0]['name']
        #Track name
        track_name = track["track"]["name"]
        track_names.append((track_name, artist))
    return track_names


def YoutubeAudioDownload(video_url,destination_path):
    AUDIO_DOWNLOAD_DIR = os.path.join(destination_path)
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio = True).first()

    try:
        audio.download(AUDIO_DOWNLOAD_DIR)
    except:
        print("Failed to download audio")

    print("audio was downloaded successfully")

def youtube_search(title):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified query term:
    search_response = youtube.search().list(
    q=title,
    part='id,snippet',
    maxResults=1
    ).execute()

    videoIDs = []
    playlistIDs = []
    
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videoIDs.append(search_result['id']['videoId'])
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlistIDs.append(search_result['id']['playlistId'])
    
   
    return videoIDs

def get_urls(track_names):
    urls = []
    for song in track_names:
        ' '.join(song)
        video_id = youtube_search(song)
        video_id = ''.join(video_id)
        urls.append(video_id)
    
    return urls

def download_audios(urls,destination_path):
    for url in urls:
        DOWNLOAD_LINK = f'https://www.youtube.com/watch?v={url}'
        print(DOWNLOAD_LINK)
        YoutubeAudioDownload(DOWNLOAD_LINK,destination_path)


# your spotify credentials which you can obtain from developer spotify
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://localhost:3000'

SCOPE = "playlist-read-private"
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)  
sp = Spotify(auth_manager=sp_oauth)

# google yt developer key (you can get it from google console by enabling youtube API)
DEVELOPER_KEY = 'YOUR-DEVELOPER-KEY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

#link to your spotify playlist
playlist_link = "https://open.spotify.com/playlist/4IGzIuIXnIBrXbkYTCHMJa?si=2d0d70c1349649e2"

#path to store downloads
destination_path = os.path.join('PATH/TO/DESTINATION/FOLDER')

track_names = get_track_names()
urls = get_urls(track_names)
download_audios(urls, destination_path)
