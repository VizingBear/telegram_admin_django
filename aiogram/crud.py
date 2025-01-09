import logging

from sqlalchemy import select, delete, update

from models import News, Image, EntryPoint, SendNews, AsqQuestion, AboutProjectContent, Contact, JustSend, User, AboutProjectButton
from database import async_session


async def post_user(chat_id, user_id, username, first_name, last_name):
    async with async_session() as session:
        new_user = User(chat_id=chat_id, user_id=user_id, username=username,first_name=first_name, last_name=last_name )
        session.add(new_user)
        await session.commit()


async def get_entrypoint_data():
    async with async_session() as session:
        statement = select(EntryPoint)
        return (await session.execute(statement)).scalar()


async def get_sendnews_data():
    async with async_session() as session:
        statement = select(SendNews)
        return (await session.execute(statement)).scalar()


async def get_asqquestion_data():
    async with async_session() as session:
        statement = select(AsqQuestion)
        return (await session.execute(statement)).scalar()


async def get_aboutproject_content():
    async with async_session() as session:
        statement = select(AboutProjectContent)
        return (await session.execute(statement)).scalar()


async def get_aboutproject_button():
    async with async_session() as session:
        statement = select(AboutProjectButton)
        return (await session.execute(statement)).scalars().all()


async def get_contact_data():
    async with async_session() as session:
        statement = select(Contact)
        return (await session.execute(statement)).scalar()


async def get_justsend_data():
    async with async_session() as session:
        statement = select(JustSend)
        return (await session.execute(statement)).scalar()


async def set_new_news(chat_id, user_name, content):
    async with async_session() as session:
        new_news = News(chat_id=chat_id,user_name=user_name ,content=content)
        session.add(new_news)
        await session.commit()
        await session.flush()
        await session.refresh(new_news)
        return new_news.id


async def set_new_images(news_id, file_name):
    async with async_session() as session:
        new_image = Image(news_id=news_id, path=f'media/news_image/{file_name}')
        session.add(new_image)
        await session.flush()
        await session.commit()