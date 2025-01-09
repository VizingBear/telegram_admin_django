import asyncio
import logging
import os
import time

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from crud import (set_new_news, set_new_images, get_entrypoint_data, get_sendnews_data, get_asqquestion_data,
                  get_aboutproject_content, get_contact_data, get_justsend_data, get_aboutproject_button)

from crud import post_user

router = Router()
MEDIA_PATH = '../media'
MEDIA_PATH_TO_SAVE_IMAGE = '/media'

class SendNews(StatesGroup):
    news_id = 0
    check_quantity = 0
    check_text = 0
    state_check = 0
    sending_news = State()
    sending_image = State()


def replace_html_tag(text):
    return text.replace("<p>","").replace("</p>","").replace("&nbsp;","").replace("<br>","").replace("</br>","")


@router.message(Command(commands=["start"]))
async def entry_function(message: types.Message):
    try:
        await post_user(message.chat.id, message.from_user.id, message.from_user.username, message.from_user.first_name,message.from_user.last_name)
    except:
        logging.log(level=logging.INFO, msg=f'User {message.from_user.username} chat id {message.chat.id} tries to log into the bot again')
    data = await get_entrypoint_data()
    await message.answer_photo(photo=FSInputFile(f'{MEDIA_PATH}/{data.path}'), caption = replace_html_tag(data.content))


@router.message(Command(commands=["send_news"]))
async def sending_news(message: types.Message, state: FSMContext):
    await state.clear()
    data = await get_sendnews_data()
    await message.answer(replace_html_tag(data.content))
    await state.set_state(SendNews.sending_news)


@router.message(SendNews.sending_news)
async def sending_news_state(message: types.Message, state: FSMContext):
    data = await get_sendnews_data()
    SendNews.check_quantity = 0
    SendNews.news_id = 0
    if message.caption:
        news = await set_new_news(message.chat.id, message.from_user.username, message.caption)
        await asyncio.sleep(0.2)
        SendNews.news_id = news
        SendNews.check_text += 1
        await asyncio.sleep(0.2)

    if message.photo:
        file_name = await download_image(message, [message.photo[-1].file_id])
        try:
            await set_new_images(SendNews.news_id, file_name)
        except:
            SendNews.check_text = 0
        SendNews.check_quantity += 1

    elif message.text:
        if message.text in ['/ask_question', '/about_projects', '/contacts', '/just_send']:
            await message.answer(
                'Вы выбрали команду нашего бота. Мы завершаем заполнение новости.'
                '\nЕсли вы хотите предложить новость: еще раз нажмите /send_news '
                f'\nЕсли вы хотите выполнить альтернитивную команду - нажмите {message.text}'
            )
            await state.clear()
            return None
        SendNews.check_text+=1
        await set_new_news(message.chat.id, message.from_user.username, message.text)
    else:
        await message.answer(replace_html_tag(data.content_failed_data))
        return await state.set_state(SendNews.sending_news)

    if SendNews.check_quantity < 2 and SendNews.check_text == 0:
        await message.answer(replace_html_tag(data.content_failed_news))
        SendNews.state_check = 1
    elif SendNews.check_quantity < 2:
        await message.answer(replace_html_tag(data.content_accept_news))
        SendNews.state_check = 0

    await state.set_state(SendNews.sending_news) if SendNews.state_check == 1 else await state.clear()


async def download_image(message,file_id_list):
    for file_id in file_id_list:
        file_name = f'{message.from_user.id}+{message.from_user.username}+{file_id[15:30]}.jpg'
        file_path = f'{MEDIA_PATH_TO_SAVE_IMAGE}/news_image'
        os.makedirs(file_path, exist_ok=True)
        await message.bot.download(file=file_id, destination=f'{file_path}/{file_name}')
        logging.log(level=logging.INFO,msg =  f'Загружена фотография {file_name} от пользователя @{message.from_user.username}')
        return file_name


@router.message(Command(commands=["contacts"]))
async def get_contacts(message: types.Message):
    data = await get_contact_data()
    await message.answer(replace_html_tag(data.content))


@router.message(Command(commands=["just_send"]))
async def just_send(message: types.Message):
    data = await get_justsend_data()
    await message.answer_photo(photo=FSInputFile(f'{MEDIA_PATH}/{data.path}'), caption = replace_html_tag(data.content))


@router.message(Command(commands=["ask_question"]))
async def ask_question(message: types.Message):
    data = await get_asqquestion_data()
    await message.answer(
        replace_html_tag(data.content),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=data.button_name, url=data.url
                    )
                ]
            ]
        )
    )


@router.message(Command(commands=["about_projects"]))
async def get_projects_info(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = await get_aboutproject_button()
    content = await get_aboutproject_content()

    if not content or buttons == []:
        await message.answer('Данный функционал еще в разработке')
    else:
        await message.answer(
            replace_html_tag(content.content),
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text=button.button_name, url=button.url
                        )
                    ] for button in buttons
                ]
            )
        )