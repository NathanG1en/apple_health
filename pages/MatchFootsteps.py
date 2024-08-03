import streamlit as st
import pandas as pd
import base64
from requests import post, get 
import requests
import json
import webbrowser
# from HelperFunctionsSpotify import * 

# https://www.youtube.com/watch?v=WAmEZBEeNmg
# video by Tim from @TechWithTim that We used to understand API calls and how to 

client_id = '4905bbd8cf0f47f6bbc36b2f5fec965a'
client_secret = '5f6ed5391e6144b9a733d0f384332384'

### FUNCTIONS ###
def get_token(): 
    auth_string = f"{client_id}:{client_secret}" # These three lines are to get authentification information
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    result = requests.post(url, headers=headers, data=data) 
    result.raise_for_status()  # Check for request errors
    json_result = result.json()
    token = json_result["access_token"]
    return token


def get_auth_header(token): 
    return {"Authorization": "Bearer " + token} # need this a lot, basically saying we have permission to use the API 

def search_for_artist(token, artist_name): 
    url = "https://api.spotify.com/v1/search" # after the /v1, you put it in what service you want - and then what you want to do with that service
    headers = get_auth_header(token) 
    query = f"q={artist_name}&type=artist&limit=1" # for example, /v1/search?q=ACDC&type=artist&limit=1

    query_url = url + "?" + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"] # we get a json from this query, but we only want the artist information
    if len(json_result) == 0: 
        print("No artist with this name exists")
        return None
    else: 
        return json_result[0]


def get_songs_by_artist(token, artist_id): # title is a good descriptor
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        headers = get_auth_header(token)
        result = requests.get(url, headers = headers)
        json_result = json.loads(result.content)["tracks"] # important part, indexes through the json
        return json_result


def get_track_bpm(token, track_id): # good descriptor 
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        audio_features = response.json()
        bpm = audio_features['tempo']  # BPM information is under 'tempo' key
        return bpm
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None  # Handle the error as needed


def get_track_id(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={song_name}&type=track&limit=1"

    query_url = f"{url}?{query}"
    result = requests.get(query_url, headers = headers)

    if result.status_code == 200: # this is the status code for a successful http request attempt :D
        json_result = json.loads(result.content)
        tracks = json_result.get("tracks", {}).get("items", [])
        if tracks:
            track_id = tracks[0]["id"]
            return track_id
        else:
            print("No tracks found :()")



def get_track_info(token, track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        track_info = response.json()
        return track_info
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None



def find_closest_bpm(songs_dict, target_bpm):
    closest_song = None
    # https://stackoverflow.com/questions/68198688/whats-a-good-starting-value-for-a-min-or-max-variable
    min_difference = float('inf')

    for song, bpm in songs_dict.items():
        difference = abs(bpm - target_bpm)
        if difference < min_difference:
            min_difference = difference
            closest_song = song

    return closest_song


def display_song_image(token, song_id):
    track_info = get_track_info(token, song_id)
    if track_info:
        # Accessing album artwork URLs
        album_artwork_urls = [image['url'] for image in track_info['album']['images']]
        
        # Displaying the album artwork URLs
        print("Album Artwork URLs:")
        for url in album_artwork_urls:
            print(url)
            
        # Opening the first image URL in a web browser
        if album_artwork_urls:
            webbrowser.open(album_artwork_urls[0])
        else:
            print("No album artwork available for this track.")
    else:
        print("Failed to retrieve track information.")

def display_song_details(token, song_id):
    st.title("Song Details")

    # Retrieve track information
    track_info = get_track_info(token, song_id)
    if track_info:
        # Display album artwork
        st.markdown("### Album Artwork")
        album_artwork_urls = [image['url'] for image in track_info['album']['images']]
        st.image(album_artwork_urls[0], width=300)
        
        # Display audio player for song snippet
        preview_url = track_info.get('preview_url')
        if preview_url:
            st.markdown("### Song Preview")
            st.audio(preview_url)
        else:
            st.warning("No preview available for this track.")

# songs_dict = {} # lowkey global -> don't really know how to handle this otherwise
def map_songs_to_bpm(token, songs):
    songs_id_dict = {}
    songs_dict = {}
    for song in songs: 
        song_id = get_track_id(token, song)
        song_bpm = get_track_bpm(token, song_id)
        songs_dict[song] = song_bpm
        # print(f"{song}: {song_bpm}") # <- had this before I returned anything, made sure the songs & bpms were accurately mapped
        # songs_id_dict[song] = song_id
    return songs_dict
        
def bpm_handler(bpm):
    if bpm < 120:
        st.write("You should be **Speed Walking**!")
    if bpm >= 120 and bpm <= 140:
        st.write("You should be **Jogging**!")
    if bpm > 140:
        st.write("You should be **Running**!")



# this token is what we use for everything 
token = get_token()

## BODY ##

st.title("Match Your Steps to the Beat! :notes:")

Users_song = st.text_input("Enter your song!" )

if len(Users_song) != 0:
    Users_song_id = get_track_id(token, Users_song)
    display_song_details(token, Users_song_id)

    st.subheader("TAP YOUR FEET AT THIS RATE:")
    st.write(f"{get_track_bpm(token, Users_song_id):.2f} Beats Per Minute")
    bpm_handler(get_track_bpm(token, Users_song_id))

