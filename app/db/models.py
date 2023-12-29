import datetime
import uuid
from typing import List, Dict

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from uuid import uuid4

from app.db.database import Base


class ChatMembers(Base):
    __tablename__ = 'chat_members'

    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('chat.guid'), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('account_user.id'), primary_key=True)

    chat: Mapped["Chat"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="chats")


class Chat(Base):
    __tablename__ = 'chat'

    guid: Mapped[uuid.UUID] = mapped_column(default=uuid4, primary_key=True, unique=True, nullable=False)
    game: Mapped[uuid.UUID] = mapped_column(ForeignKey('games.guid'), index=True)
    game_guid: Mapped[uuid.UUID] = mapped_column(index=True, unique=True)

    messages: Mapped[List["Message"]] = relationship(back_populates="chat", lazy='selectin')
    members: Mapped[List["ChatMembers"]] = relationship(back_populates="chat", lazy='selectin')

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.UTC_TIMESTAMP())


class Message(Base):
    __tablename__ = 'message'

    guid: Mapped[uuid.UUID] = mapped_column(default=uuid4, primary_key=True, unique=True, nullable=False)
    chat_guid: Mapped[uuid.UUID] = mapped_column(ForeignKey('chat.guid'), index=True)
    chat: Mapped["Chat"] = relationship(back_populates="messages")

    sender_id: Mapped[int] = mapped_column(ForeignKey('account_user.id'), index=True, unique=True)
    sender: Mapped['User'] = relationship()

    message: Mapped[str]
    sent_at: Mapped[datetime.datetime] = mapped_column(server_default=func.UTC_TIMESTAMP())


class User(Base):
    __tablename__ = 'account_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    guid: Mapped[uuid.UUID] = mapped_column(default=uuid4, unique=True, nullable=False)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    date_joined: Mapped[datetime.datetime] = mapped_column(server_default=func.UTC_TIMESTAMP())

    chats: Mapped[List["ChatMembers"]] = relationship(back_populates="user", lazy='selectin')


class Game(Base):
    __tablename__ = 'games'

    guid: Mapped[uuid.UUID] = mapped_column(default=uuid4, primary_key=True, unique=True, nullable=False)
    title: Mapped[str]
    description: Mapped[str]
    image: Mapped[str] = mapped_column(nullable=True)
    configs: Mapped[Dict | List] = mapped_column(type_=JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.UTC_TIMESTAMP())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.UTC_TIMESTAMP)

    users: Mapped[uuid.UUID] = mapped_column(ForeignKey('account_user.guid'), index=True, unique=True, nullable=False)

    chat: Mapped[uuid.UUID] = mapped_column(ForeignKey('chat.guid'), index=True, unique=True, nullable=False)
