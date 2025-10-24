# gamerank
A website with online games catalogue with advanced ranking system.

must have:

- games catalogue

- filters

- authorization / log in / registration

- comments

- game link

- ratings

should have

- likes/dislikes 

- follow

- admin panel

could have
  
- trailer

- screenshots preview 

wont have
  
- friends system 

 wish

- add custom game

## Backend setup

Prerequisites:
- Python 3.10+
- MongoDB running locally at `mongodb://localhost:27017`

Steps (Windows PowerShell):
1. `cd D:\w\gamerank\backend`
2. `py -m venv .venv`
3. `.\.venv\Scripts\Activate.ps1`
4. `python -m pip install --upgrade pip`
5. `pip install -r requirements.txt`
6. `setx MONGODB_URI "mongodb://localhost:27017"`
7. `setx MONGODB_DB "gamerank"`
8. Start server: `uvicorn main:app --reload`

Endpoints:
- `GET /` hello world
- `GET /health` health check
- `GET /users` list users
- `POST /users` create user `{ "username": "alice", "email": "alice@example.com" }`
- `GET /games` list games
- `POST /games` create game `{ "title": "Hades", "genre": "Roguelike", "release_year": 2020, "rating": 9.0 }`

## Database initialization

On app startup, the API connects to MongoDB and ensures the `users` and `games` collections exist. No manual step is required beyond running MongoDB.