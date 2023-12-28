from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID

from . import models, schemas


def get_users(db: Session):  #, user_id: UUID
    return db.query(models.User).all() # .filter(models.User.guid == user_id)

def get_games(db: Session):
    return db.query(models.Game).all()

# def get_chat(db: Session): #, chat_id: UUID
#     return db.query(models.Chat).all() #.filter(models.Chat.id == chat_id).first()
