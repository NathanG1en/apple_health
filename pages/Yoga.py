import streamlit as st
import simpleaudio as sa
import time

## FUNCTIONS (and class) ## 

class AudioSong:  # just a class for handling audio because that would be annoying to do for all five 
    def __init__(self, file_path):
        self.file_path = file_path
        self.wave_obj = sa.WaveObject.from_wave_file(file_path)
        self.play_obj = None

    def play(self):
        self.play_obj = self.wave_obj.play()

    def stop(self):
        if self.play_obj:
            self.play_obj.stop()

# Downloads/AppleHealthReal/pages/megaGymDataset.csv

song_healing = 'pages/Songs/invisible_healing.wav'
song_bells = 'pages/Songs/carol_of_the_bells.wav'
song_thunder = 'pages/Songs/drew_theory_thunder.wav'
song_halo = 'pages/Songs/halo_theme.wav'
song_survive = 'pages/Songs/i_will_survive.wav'
# Originally geting an error - about it not beng in WAV (I had it in mp3)

# Create song objects
song1 = AudioSong(song_healing)
song2 = AudioSong(song_bells)
song3 = AudioSong(song_thunder)
song4 = AudioSong(song_halo)
song5 = AudioSong(song_survive)

song_list = [song1, song2, song3, song4, song5]


# iterates through for tier - 3 mintues, and then stays on the last song for 3 minutes (we think it's really calming :D)
meditation_tiers = [0.5, 4 , 8, 13, 23, 33]

st.title("Meditation Master :peace_symbol:")

duration_of_meditation = st.selectbox("Select how long you'll be meditating: ", meditation_tiers)

# stop_button = st.button("Stop Your Meditation Experience")
# if stop_button:
#     st.write("haha")
#     for song in song_list:
#         song.stop()

end_speed = 115
start_speed = 45


if st.button("Start Your Meditation Experience"):
    steps = len(song_list)

    duration_seconds = (duration_of_meditation - 3) * 60  # Convert minutes to seconds
    if duration_of_meditation  == 0.5:
        duration_seconds = 30
    speed_difference = end_speed - start_speed
    step_size = speed_difference / steps

    # Booleans
    song_playing = False
    # stop_audio = False

    for i in range(steps):
        if i != 0: # if we're playing something and we're not on the first iteration 
            if song_playing:
                song_list[i - 1].stop()
                print("previous song stopped")
                song_playing = False

        song_list[i].play()
        song_playing = True
        print(i)
        current_speed = start_speed + i * step_size
        time.sleep(duration_seconds / steps)
        st.write(f"Step {i+1}/{steps}: Song speed was about {current_speed} bpm")

        if i == steps - 1:
            song_list[i].stop()
            print("Last song stopped")
            song_playing = False


    for i in range(steps - 1, -1, -1):
        if i != steps - 1:  # If we're playing something and we're not on the last iteration, we iterate backwards 
            if song_playing:
                song_list[i + 1].stop()
                print("Previous song stopped")
                song_playing = False
        
        song_list[i].play()
        song_playing = True
        print(i)
        current_speed = start_speed + i * step_size
        time.sleep(duration_seconds / steps)
        st.write(f"Step {steps - i}/{steps}: Song speed was about {current_speed + 14} bpm")

        if duration_of_meditation == 0.5 and i == 0: 
            song_list[i].stop()
            st.write("**MEDITATION COMPLETE!**")
    


