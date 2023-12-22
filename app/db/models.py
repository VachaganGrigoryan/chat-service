from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4
from .database import Base, engine


# chat_user_association = Table(
#     'chat_user_association',
#     Base.metadata,
#     Column('chat_id', UUID(as_uuid=True), ForeignKey('chat.guid')),
#     Column('user_id', UUID(as_uuid=True), ForeignKey('account_user.guid'))
# )

# chat_user_association = Table(
#     'chat_user_association',
#     Base.metadata,
#     Column('chat_id', UUID(as_uuid=True), ForeignKey('chat.guid')),
#     Column('user_id', UUID(as_uuid=True), ForeignKey('account_user.guid'))
# )



# user_game_association = Table('user_game_association', Base.metadata,
#     Column('user_id', UUID(as_uuid=True), ForeignKey('account_user.guid')),
#     Column('game_id', UUID(as_uuid=True), ForeignKey('games.guid'))
# )

class ChatMembers(Base):
    __tablename__ = 'chat_members'

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, unique=True, nullable=False)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('chat.guid'), index=True, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('account_user.guid'), index=True, unique=True, nullable=False)


class Chat(Base):
    __tablename__ = 'chat'

    guid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, unique=True, nullable=False)
    game = Column(UUID(as_uuid=True), ForeignKey('games.guid'), index=True, unique=True, nullable=False)
    messages = Column(UUID(as_uuid=True), ForeignKey('message.guid'), index=True, unique=True, nullable=False)
    members = Column(UUID(as_uuid=True), ForeignKey('chat_members.id'), index=True, unique=True, nullable=False)


class Message(Base):
    __tablename__ = 'message'

    guid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, unique=True, nullable=False)
    chat = Column(UUID(as_uuid=True), ForeignKey('chat.guid'), index=True, unique=True, nullable=False)
    sender = Column(UUID(as_uuid=True), ForeignKey('account_user.guid'), index=True, unique=True, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())



class User(Base):
    __tablename__ = 'account_user'

    guid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    date_joined = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    games = Column(UUID(as_uuid=True), ForeignKey('games.guid'), index=True, unique=True, nullable=False)
    chat = Column(UUID(as_uuid=True), ForeignKey('chat.guid'), index=True, unique=True, nullable=False)




# class Game(Base):
#     __tablename__ = 'games'

#     guid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, unique=True, nullable=False)
#     title = Column(String(255), nullable=False)
#     description = Column(Text, nullable=False)
#     image = Column(String, nullable=True)
#     configs = Column(JSON, nullable=True)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
#     users = relationship('User', secondary=user_game_association, back_populates='games')
#     chat = relationship('Chat', secondary=chat_user_association, back_populates='games',
#                     primaryjoin="Game.guid == chat_user_association.c.game_id",
#                     secondaryjoin="Chat.guid == chat_user_association.c.chat_id")



class Game(Base):
    __tablename__ = 'games'

    guid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=True)
    configs = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)

    users = Column(UUID(as_uuid=True), ForeignKey('account_user.guid'), index=True, unique=True, nullable=False)

    chat = Column(UUID(as_uuid=True), ForeignKey('chat.guid'), index=True, unique=True, nullable=False)



Base.metadata.create_all(bind=engine)