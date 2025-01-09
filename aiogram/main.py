import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

import handlers

bot = Bot(token=os.getenv('TG_TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
dispatcher = Dispatcher()
dispatcher.include_routers(handlers.router)


async def main():
    await bot.delete_webhook()
    logging.log(level=logging.INFO,msg='Aiogram is up')
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    asyncio.run(main())
