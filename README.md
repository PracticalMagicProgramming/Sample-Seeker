
# Welcome to Sample Seeker Redux!

This is my first Capstone Project for Springboards Software Engineering Bootcamp.The goal was to create a server-side application using my knowledge of Python, Flask and SQLAlchemy and my imagination!

Sample Seeker is an app where you can upload samples from your personal sample library on your harddrive and categorize them. As music producer myself often a producers sample library is chaotic on the best of days. Having an app to keep track of, store and organize samples is pretty useful! 

# How to use this app:
1. If you're new - hit up the registration page to create an account
1. If your're already a user you can use our login page 
2. The upload page is where you can upload your sounds into your user account
3. You can access your sounds through your profile page - right now you'll only be able to preview your sounds


## The Story Thus Far

I learned **a ton**  about Flask and its functionality. I really love it as a microframework for web development. I used Flask-Login for managining the current users status for the app. Flask also offers its own migration library which I utilized often for version control of my SQLAlchemy models and Database in Postgres.

The most complicated part of this application was by far managing the audio data. Firstly bc I needed to figure out how to store it in Postgres and SQLAlchemy (which is a temporary solution until I have implemented Dropbox). Secondly because I then needed to *decode* the audio so that the application could play it back. 

My solution for uploading sound was to utilize the request object to capture the data and save it as a binary data in SQLAlchemy and Postgres. Which worked fairly easily. If you look at the code you can see Im using a multi-part form to capture the form data using both WTForms and then the request object for the raw audio itself. This is then validated by the view function and saved to the db.

Getting the sound to playback was a bit more tricky. On the front-end I used an audio tag in the html. On the server side I needed to find a way to grab the audio data from the database and insert it into the *src* parameter of the the audio tag. This was not as clear cut as the upload. My solution was to have the *src* be a flask endpoint whose response was the audio data to be used for playback. If you look in the *app.py* file I created an endpoint that queried the db-decoded the binary data using bytesIO-and sent back as wave/mp3 file to the audio tag in the html.(I used Flasks send_file() to create the response, the mimetype parameter was used to establish that our resp. is an audiofile).

## The Future of Sample Seeker

Sample Seeker is still in its fledgling state so it's current functionality is labeling-uploading-preview. Albeit there are stretch goals to improve functionality and flow.

### IMMEDIATE STRETCH GOAL:

**Full dropbox API integration** - *this will improve the amount that can be stored and provide access to anything that is in your dropbox. (As long as you give us permission ofc !)*

#### Other Stretch Goals:

**Overhaul the front-end with React** - *currently the front end is done mainly with CSS and Bootstrap. However, in designing the current front-end there are tons of places I would love to re-implenment the front-end using components and hooks.*

**Creating a search filter** - *I want to create a filter that will search all of the your sounds and only display sounds based on the filtering criteria. Ideal for bigger sample libraries.* 
