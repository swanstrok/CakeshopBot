from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from storage_db import *
from Cakeshop_Euphoria_Bot import config

logging.basicConfig(level=logging.INFO,
                    # filename='Euphoria.log',
                    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-5s TIME:%(asctime)s %(message)s')

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)
db = DatabaseManager('Euphoria_database.db')

# async def on_startup(_):

#
#     db_connect()
#     print("Создание таблиц БД завершено.")


if __name__ == '__main__':
    from Cakeshop_Euphoria_Bot.handlers import dp

    executor.start_polling(dp, skip_updates=True)
