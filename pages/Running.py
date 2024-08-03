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



### Songs Container / Getting the Genre ###
rock_songs = ["Hotel California", "Wish You Were Here", "Stairway to Heaven", "Hurt", "You Be the Judge",
"Primrose (Dream State)", "Gimme Three Steps", "Panama (Van Halen)", "Eleanor Rigby", "Just the Way You Are",
"Smells Like Teen Spirit", "Roxanne", "Hit Me With Your Best Shot", "Fortunate Son", "Bohemian Rhapsody",
"Sweet Child O' Mine", "Come As You Are","Livin' on a Prayer", "Don't Stop Believin'", "Another Brick in the Wall, Part 2", 
"Back in Black","Highway to Hell", "Paradise City", "Paint It Black", "Sweet Home Alabama", "Welcome To the Jungle",
 "Enter Sandman", "You Give Love a Bad Name","Born to Be Wild", "Fortunate Son", "Don't Fear The Reaper", 
 "The Chain", "Born to be Wild","All Along the Watchtower", "You Really Got Me", "Bad Moon Rising", 
 "Crazy Train", "Rebel Rebel","Johnny B. Goode", "Twist and Shout", "Jailhouse Rock", "I Fought the Law", 
 "Seventeen", "Wanted Dead or Alive"]

rap_songs = ["Rap God", "Lose Yourself", "MELTDOWN", "Lovin on Me", "Holy Grail", "Hard in Da Paint",
"Lemonade (Gucci Mane)", "Dear Old Nicki", "Feel Good Inc", "Poetic Justice", "All I Have (NF)", 
"Watching Movies", "No Hands","Long Live A$AP", "Hotline Bling", "Ms. Jackson", "SICKO MODE",
"500lbs", "SAY MY GRACE", "goosebumps","Empire State of Mind", "Forgot About Dre",
"Mo Money Mo Problems", "Stronger","Power", "No Hands", "HUMBLE.", "Area Codes",
"Money Trees", "All Me", "Big Pimpin'", "XO Tour LIif3", "All I Do is Win",
 "Fight The Power", "Big Bank","Bad and Boujee", "Congratulations", "N.Y. State of Mind"]


pop_songs = ["Perfect", "Someone Like You", "Sugar", "Shake It Off", "Everybody Talks",
"Don't Start Now", "Sorry","Blinding Lights", "Into You", "Thnks fr th Mmrs", "Stitches",
"Dark Horse", "Crazy In Love","Only Girl (In The World)", "Locked Out of Heaven",
"One Kiss", "Señorita", "driver's license", "deja vu", "1 step forward, 3 steps back", 
"enough for you",  "get him back!", "Dance With You Tonight (Laufey)", "Like the Movies", "Must Be Love (Laufey)",
"Sker Boi", "Bang Bang", "Toxic", "We Didn't Start the Fire", "Locked Out of Heaven", "That's Not my Name", 
"Honey Honey", "7 rings", "American Pie", "Did it Again", "As Long as You Love Me", "Cake By the Ocean", 
"Call me Maybe", "22", "cardigan", "You Belong With Me", "Mastermind", "Red", "Speak Now", "Never Grow Up"]



def get_genre(genre): 
    if genre == "Rock":
        return rock_songs
    if genre == "Pop":
        return pop_songs
    if genre == "Rap":
        return rap_songs
    if genre == "Any":
        return rock_songs + pop_songs + rap_songs

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

# predicted heartrate/bpm of song \/
def handling_gender_heartrate(gender, average_pace):
    # Equations from the DataMotion.ipynb where we used scipy to perform linear regression on running dataset 
    male_heartrate_prediction = lambda x: -1.3879786907495584 * x + 159.88667781131127
    female_heartrate_prediction = lambda x: -1.6532179784683314 * x + 171.44424342083707
    if gender == "Male":
        return male_heartrate_prediction(average_pace)
    if gender == "Female":
        return female_heartrate_prediction(average_pace)

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

# this token is what we use for everything 
token = get_token()
### BODY ###

st.title("You've Selected Running!")

if 'runs' not in st.session_state:
    st.session_state.runs = pd.DataFrame(columns=['Miles', 'Hours', 'Minutes', 'Seconds', 'Pace (mi/min)'])

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Retrieve or initialize the genre variable in session state
if 'genre' not in st.session_state:
    st.session_state.genre = None

## Selecting Gender #
st.subheader("Gender Selection")
gender = st.radio("Select your gender:", ("Male", "Female"))
st.write(f"You selected: {gender}")

## Selecting Genre
st.subheader("Genre Selection")
# st.write(f"Before selectbox - Genre: {st.session_state.genre}")
st.session_state.genre = st.selectbox("What genre would you like to listen to?", ("Pop", "Rock", "Rap", "Any"))
# st.write(f"After selectbox - Genre: {st.session_state.genre}")   

form_submitted = False

with st.form(key='run_details_form'):
    miles = st.number_input("How many miles for the run:", value=0, max_value=59)
    hours = st.number_input("How many hours:", value=0, max_value=59)
    minutes = st.number_input("How many minutes:", value=0, max_value=59)
    seconds = st.number_input("How many seconds:", value=0, max_value=59)

    submitted = st.form_submit_button("Submit")

    if submitted:
        new_run_data = {
            'Miles': [miles],
            'Hours': [hours],
            'Minutes': [minutes],
            'Seconds': [seconds]
        }
        new_run = pd.DataFrame(new_run_data)
        if (new_run['Miles'] != 0).any(): # can't divide by 0
            new_run['Pace (mi/min)'] = ((new_run['Hours'] * 60 + new_run['Minutes'] + new_run['Seconds'] / 60.0) / new_run['Miles'])# Pace not something the user enters, calculate it here
        st.session_state.runs = pd.concat([st.session_state.runs, new_run], ignore_index=True)
        form_submitted = True
        st.success("Run details added to DataFrame!")

if form_submitted:
    st.write("Current Runs:")
    st.write(st.session_state.runs)
    average_pace = st.session_state.runs['Pace (mi/min)'].mean()
    st.markdown(f"**Average Pace:** {average_pace:.2f} minutes per mile") # markdown for bolding words and stuff
    st.markdown(f"**Some Recommendations:**")


    genre_result = get_genre(st.session_state.genre)
    # st.write(genre_result) <- just checking to see if the genres were even loaded in 
    print(genre_result) # <- same thing ^^^
    songs_dict = map_songs_to_bpm(token, genre_result)
    # the first iteration will take a while, because we have to iterate through each song and make calls to Spotify's search service in the API separately

    # finding your predicted heartrate 
    predicted_bpm = handling_gender_heartrate(gender, average_pace)
    st.write(f"your predicted heartrate is {predicted_bpm:.2f} bpm")

    # get the song closest to your predicted heartrate
    best_song = find_closest_bpm(songs_dict, predicted_bpm)
    print(f"songs dict is {songs_dict}")
    print(find_closest_bpm(songs_dict, predicted_bpm))
    st.write(f"based, on your bpm, the best song for you is: {best_song} ")

    # get the id, important for visual components
    best_song_id = get_track_id(token, best_song)
    display_song_details(token, best_song_id)

    st.session_state.form_submitted = False
