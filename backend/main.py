import os
import datetime
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client: Optional[AsyncIOMotorClient] = None
mongo_db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global mongo_client, mongo_db
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongo_db_name = os.getenv("MONGODB_DB", "gamerank")
    mongo_client = AsyncIOMotorClient(mongo_uri)
    mongo_db = mongo_client[mongo_db_name]
    existing_collections = await mongo_db.list_collection_names()
    if "users" not in existing_collections:
        await mongo_db.create_collection("users")
    if "games" not in existing_collections:
        await mongo_db.create_collection("games")
    try:
        yield
    finally:
        mongo_client.close()

app = FastAPI(title="GameRank API", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


def serialize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    if document is None:
        return {}
    cloned = dict(document)
    if "_id" in cloned:
        cloned["id"] = str(cloned["_id"])  # ObjectId -> str
        del cloned["_id"]
    return cloned


class UserCreate(BaseModel):
    username: str
    email: str


class GameCreate(BaseModel):
    title: str
    genre: str
    release_year: int
    rating: Optional[float] = None


@app.get("/users")
async def list_users() -> List[Dict[str, Any]]:
    users_cursor = mongo_db["users"].find()
    users: List[Dict[str, Any]] = []
    async for user in users_cursor:
        users.append(serialize_document(user))
    return users


@app.post("/users")
async def create_user(user: UserCreate) -> Dict[str, Any]:
    new_user: Dict[str, Any] = {
        "username": user.username,
        "email": user.email,
        "createdAt": datetime.datetime.utcnow().isoformat() + "Z",
    }
    insert_result = await mongo_db["users"].insert_one(new_user)
    created = await mongo_db["users"].find_one({"_id": insert_result.inserted_id})
    return serialize_document(created)


@app.get("/games")
async def list_games() -> List[Dict[str, Any]]:
    games_cursor = mongo_db["games"].find()
    games: List[Dict[str, Any]] = []
    async for game in games_cursor:
        games.append(serialize_document(game))
    return games


@app.post("/games")
async def create_game(game: GameCreate) -> Dict[str, Any]:
    new_game: Dict[str, Any] = {
        "title": game.title,
        "genre": game.genre,
        "release_year": game.release_year,
        "rating": game.rating,
        "createdAt": datetime.datetime.utcnow().isoformat() + "Z",
    }
    insert_result = await mongo_db["games"].insert_one(new_game)
    created = await mongo_db["games"].find_one({"_id": insert_result.inserted_id})
    return serialize_document(created)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


