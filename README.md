# AnimeFlix

This is a web-based anime recommendation system that uses React for the frontend and Flask for the backend. The system provides recommendations for anime based on user preferences and previously watched anime. Users can create an account and save their favorite anime to their profile. The system uses various filtering techniques to generate recommendations based on the user's preferences and watch history.

## Features

* User authentication and account creation
* Anime recommendation based based on preferred genres, type of anime and user age.
* Anime recommendation based on search query.
* Top rated recommendations.
* Recommendation based on previously watched anime.

## Technologies Used

* React for frontend
* Flask for backend
* Pytorch
* scikit-learn

## Repository Tree Structure

```
AnimeFlix

-NoteBooks
--ColdStart-UserBased CF
--Content Based Filtering
--Hybrid
NN-ItemBased CF

-backend
--models
--util

-frontend
--public
--src
---components
----Dashboard
----Login
----Register

```

## Installation

Step 1: Download the git repository.
git clone https://github.com/thermistokles/AnimeFlix

Step 2: Download the utility files and put them in AnimeFlix/backend/util
https://wpi0-my.sharepoint.com/:u:/g/personal/amore_wpi_edu/EYPmO7zVD6VLprDZO3zvNBsBFGpyi7cyWN2y8ALAwy6X0g?e=Zz9LEH
Alternatively, you can train and export these files from AnimeFlix/NoteBooks

Step 3: Start the backend server
```
cd backend
flask --app main.py --debug run
```

Step 4: Start the frontend
```
cd frontend
npm install
npm start
```

Step 5: Navigate to http://localhost:3000 in your browser to access the web application


## Credits

This project was developed by:
1. Akanksha Pawar
2. Amey More
3. Padmesh Naik
4. Vignesh Sundaram  

as a part of Information Retrieval final project at Worcester Polytechnic Institute.

