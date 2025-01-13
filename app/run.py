import sys
import asyncio
import logging

from aiogram import Dispatcher

from model import MailBot
from config import TG_TOKEN


async def main() -> None:
    dp = Dispatcher()
    mail = ...
    db = ...
    bot = MailBot(token=TG_TOKEN, mail=mail, db=db)
    # dp.include_routers
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
