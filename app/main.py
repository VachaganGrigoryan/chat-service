from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from database import engine, get_db, SessionLocal



# models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='postgres',
                                user='postgres',
                                password='postgres',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was succesful")
        break
    except Exception as error:
        print("COnnecting fail!")
        print("ERROR Was", error)
        time.sleep(2)