import streamlit as st
import pandas as pd

# so basically I have this Runner's Dataset that keeps track of things like M or F - elapsed time - distance - and BPM (hard to find an easy dataset with bpm)
# I'm thinking about merging the dfs using pandas, then doing some analysis?
# What I'm thinking is doing two models (M and F) of linear (or other type of regression) and trying to correlate average pace (distance / elapsed time) and finding the bpm -> and then using 
# that bpm as the bpm to a song (or a song with a musical bpm in the general range/ tolerance of the running bpm)
# obviously - use the scipy library to do this

# we may have to take into account whether the user is Male or Female and do reccomendations based off that 
# Maybe we could add a Heart Rate suggester for the type of exercise 

# Maybe something similar for strength training and yoga? 
# or we could get rid of those and flesh out the running? 
# who knows 

# BODY ----------------------

st.set_page_config(
    page_title= "APPLEHEALTH", 
    page_icon=":apple:"
)


st.sidebar.success("Select a Workout")  

# Set page title and header
st.title("Workout Buddy")
st.write("🏃‍♂️ 🏋️‍♀️ Welcome to the Workout Buddy tool! 🏋️‍♂️ 🏃‍♀️")

st.write("Select your workout 👈")
    


# Old attempt at implementation, really finnicky -> broke if more than like 2 runs
# workout_options = ["Select an Option", "Running", "Strength Training", "Yoga"]
# selected_workouts = st.selectbox("Select your workout(s):", workout_options) # display workout options

# if "Running" in selected_workouts:
#     st.write("You selected running!")
#     pass
# if "Strength Training" in selected_workouts: 
#     st.write("You selected strength!")
#     pass
# if "Yoga" in selected_workouts:
#     st.write("You selected yoga!")
#     pass
