# APPLEHEALTH App Instructions 

## File Structure/Things to Know

###### * .py hyperlinks lead nowhere!
APPLEHEALTH.py is the landing page, where you can access all of the features of the webapp. If you want to be able to use all of the programs featured in the app, **you have to run APPLEHEALTH.py**. 

 In a folder, titled **pages**,  in the same directory as APPLEHEALTH is where any auxillary .py flies can be found. In this app those py files include MatchFootsteps.py, Running.py, Weightlifting.py, and Yoga.py. You **can** run these individually, but you will **not** be able to access the others. 



Follow this link to learn more about multipage apps in streamlit: 
https://docs.streamlit.io/library/get-started/multipage-apps/create-a-multipage-app

### User Interface
The user interface is entirely handled by a package called streamlit. We used buttons, sliders, textboxes, etc... from the package. To run a python script and have it show up in your browser you must run the following command in your command prompt:

**streamlit run** *your_file_path.py*

### Datasets 
We used two csvs in this project -> *raw-kaggle-csv* and *megaGymDataset.csv*
*raw-data-kaggle.csv* is found in the Data folder, and *megaGymDataset.csv* is found in the pages folder, with the four scripts used to make the different pages of the app. 

Both can also be found at these respective kaggle links:

* https://www.kaggle.com/datasets/olegoaer/running-races-strava

* https://www.kaggle.com/code/niharika41298/ultimate-gym-exploratory-data-analysis/input

### required packages
visit the requirements.txt here: [Download requirements.txt](requirements.txt)

all you have to do is run **pip install - r requirements.txt**

### Data Analysis
To view the scatterplots/linear regression model(s) we used to predict heartrate - simply open up the DataMotion.ipynb notebook located in the Data folder, alongside the corresponding raw-data-kaggle.csv. 

## What each Program Does

### MatchFootsteps
User inputs a song that they like, the program spits out the album cover art, a song preview(if available), the bpm of the song - and what pace the user should be moving at (Speed Walk, Jog, or Run). 

### Running
Using what's known as an st.form - this application takes user data and puts it into a dataframe. The data it takes includes how many miles the user is going to run and the time predicted to run in hours, minutes, and seconds. The program calculates the users average pace and then factors in both the gender and the user's preferred genre of music and gives the user a song that best matches their heartbeat. 
_*sometimes using the keyboard to input numbers is finicky, so for the best results, use the + and - buttons._

### Weightlifting
This is a simple application that just takes a dataframe and turns it into a basic reccomendation system. The user selects the body part they want to work and the level of difficulty they want their exercise to be (Beginner, or Intermediate) - and then the program spits out 1 out of N reccomendations, which the user can iterate through. 

### Yoga
This app has 5 songs in its rotation, and when the meditation button is clicked, it just plays them, from slowest to fastest - then it goes down, from fastest to slowest. The user can choose the intervals at which the song changes/ how long the meditation session lasts. 