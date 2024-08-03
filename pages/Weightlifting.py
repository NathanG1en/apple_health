import streamlit as st
import pandas as pd
### FUNCTIONS ###
def filter_workouts(body_part, difficulty):
    filtered_workouts = workouts_df[(workouts_df['BodyPart'] == body_part) & (workouts_df['Level'] == difficulty)]
    return filtered_workouts

def display_workout(index, filtered_results):
    workout_index.write(f"Workout {index + 1} of {len(filtered_results)}")
    workout_title.write(filtered_results.iloc[index]['Title'])
    workout_description.write(filtered_results.iloc[index]['Desc'])

### BODY ###

st.title("The Workout Helper!")

exercise_data = "pages/megaGymDataset.csv"
workouts_df = pd.read_csv(exercise_data)
workouts_df.dropna(inplace=True)
# print(workouts_df)

options = workouts_df.BodyPart.unique()
# print(workouts_   df[workouts_df['muscle_gp']].unique()) <- wasn't working

bodypart_selected = st.selectbox("Select the bodypart you want to work:", options)
difficulty_selected = st.selectbox("What level of difficulty:", ("Beginner","Intermediate"))



# Store the previously selected values in session_state
prev_bodypart_selected = st.session_state.get('bodypart_selected')
prev_difficulty_selected = st.session_state.get('difficulty_selected')

if (bodypart_selected != prev_bodypart_selected) or (difficulty_selected != prev_difficulty_selected):
    st.session_state['current_workout_index'] = 0
    st.session_state['bodypart_selected'] = bodypart_selected
    st.session_state['difficulty_selected'] = difficulty_selected
    
filtered_results = filter_workouts(bodypart_selected, difficulty_selected)

if not filtered_results.empty:
    workout_index = st.empty()
    workout_title = st.empty()
    workout_description = st.empty()
    show_another_button = st.empty()



    current_workout_index = st.session_state.get('current_workout_index', 0)
    # workout_index.write(f"Workout {0 + 1} of {len(filtered_results)}")
    # workout_title.write(filtered_results.iloc[current_workout_index]['Title'])
    # workout_description.write(filtered_results.iloc[current_workout_index]['Desc'])

    if len(filtered_results) > 1:
        if show_another_button.button("Reveal Workout(s)"):
            st.session_state['current_workout_index'] = (current_workout_index + 1)  % len(filtered_results) # so we can do circular 5/5 -> 1/5
            print(st.session_state['current_workout_index'])
            workout_index.write(f"Workout {current_workout_index + 1} of {len(filtered_results)}")
            workout_title.write(filtered_results.iloc[current_workout_index]['Title'])
            workout_description.write(filtered_results.iloc[current_workout_index]['Desc'])
