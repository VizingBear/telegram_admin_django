from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, engine


class EntryPoint(Base):
    __tablename__ = 'telegram_entrypoint'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    path: Mapped[str]


class SendNews(Base):
    __tablename__ = 'telegram_sendnews'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    content_failed_news: Mapped[str]
    content_accept_news: Mapped[str]
    content_failed_data: Mapped[str]


class AsqQuestion(Base):
    __tablename__ = 'telegram_asqquestion'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    button_name: Mapped[str]
    url: Mapped[str]


class AboutProjectContent(Base):
    __tablename__ = 'telegram_aboutprojectcontent'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]


class AboutProjectButton(Base):
    __tablename__ = 'telegram_aboutprojectbutton'

    id: Mapped[int] = mapped_column(primary_key=True)
    button_name: Mapped[str]
    url: Mapped[str]


class Contact(Base):
    __tablename__ = 'telegram_contact'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]


class JustSend(Base):
    __tablename__ = 'telegram_justsend'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    path: Mapped[str]



class News(Base):
    __tablename__ = "telegram_news"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    user_name: Mapped[str | None] = mapped_column(unique=False)
    content: Mapped[str | None]
    send_date: Mapped[datetime] = mapped_column(default=datetime.now())

    images: Mapped["Image"] = relationship(back_populates="news", lazy="selectin")


class Image(Base):
    __tablename__ = "telegram_image"

    id: Mapped[int] = mapped_column(primary_key=True)
    news_id : Mapped[int] = mapped_column(ForeignKey("telegram_news.id"))
    path: Mapped[str | None]

    news: Mapped["News"] = relationship(back_populates="images", lazy="selectin")


class User(Base):
    __tablename__ = 'telegram_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(default='password_1234')
    is_superuser: Mapped[bool] = mapped_column(default=False)
    chat_id: Mapped[int]
    user_id: Mapped[int]
    username: Mapped[str] = mapped_column(default='Отсутствует')
    first_name: Mapped[str] = mapped_column(default='Отсутствует')
    last_name: Mapped[str] = mapped_column(default='Отсутствует')
    date_joined: Mapped[datetime] = mapped_column(default=datetime.now())
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)


