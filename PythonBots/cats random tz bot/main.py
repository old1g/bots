from aiogram import Bot, types, Dispatcher
from aiogram.types import InputFile
from aiogram.utils import executor
import os
import random
import config as c
import asyncio

bot=Bot(token=c.token)
dp=Dispatcher(bot)

@dp.message_handler(commands=['random_cats'])
async def send_photo(message: types.Message):
    files = "C:/PythonBots/cats random tz bot/photo_cats/"
    photo = InputFile(path_or_bytesio='photo_cats/' + str(random.choice(os.listdir(path=files))))
    await bot.send_photo(chat_id=message.from_user.id, photo=photo)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)