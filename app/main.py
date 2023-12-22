from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from uuid import UUID
from db.database import SessionLocal, engine, get_db
from db import crud


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/users")
def get_users(db: Session=Depends(get_db)):

    users = crud.get_users(db)

    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.get("/games")
def get_users(db: Session=Depends(get_db)):

    games = crud.get_games(db)
    
    if not games:
        raise HTTPException(status_code=404, detail="No games found")
    return games

@app.get("/chat")
def get_chat(db: Session=Depends(get_db)):

    chat = crud.get_chat(db)
    
    if not chat:
        raise HTTPException(status_code=404, detail="No chat found")
    return chat

# models -> account_user, CHAT app models, games