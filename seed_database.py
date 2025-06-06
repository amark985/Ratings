"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

os.system("dropdb ratings")
os.system("createdb ratings")

connect_to_db(app)
app.app_context().push()
db.create_all()

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
)
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    
    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

db.session.add_all(movies_in_db)
db.session.commit()

# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"  # A unique email!
    password = "test"
    
    user = crud.create_user(email, password)
    db.session.add(user)
    
    for i in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)
        rating = crud.create_rating(user, random_movie, score)
        db.session.add(rating)

db.session.commit()