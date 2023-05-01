import asyncio
import logging
import json

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta

from telegram_bot.create_bot import bot
from telegram_bot.utils.database import UsersDatabase
from soft.signal_generation import work
from soft.db.InfoToSignalDB import DataInfoToSignal
from soft.Verirfy import get_now_price

users = UsersDatabase()
datainfotosignal = DataInfoToSignal()


async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, 'hello!')
    if not users.if_user_exists(message.from_user.id):
        users.create_new_user(message.from_user.id)
        await send_every_10_minutes()


async def send_every_10_minutes():
    while True:
        if work():
            data = datainfotosignal.get_last_forcast()
            await bot.send_photo(-1001878714474, photo=open('screenshot.png', 'rb'),
                                 caption=f'{data[0]}\n\nИспользуя свой набор индикаторов я вижу силу движения цены в {"нижнюю" if data[1] == "SHORT" else "верхнюю"} зону флета.'
                                         f'\nОткрываем сделку в {"низ" if data[1] == "SHORT" else "вверх"} по заданной валютной паре.\n\nВремя прогноза {data[3]}'
                                 )
            await asyncio.sleep(300)
            now_price = float(get_now_price())
            if now_price > float(data[4]) and data[1] == 'LONG':
                await bot.send_message(-1001878714474, f'Ставка зашла, текущая цена - {now_price}')
            elif now_price < float(data[4]) and data[1] == 'SHORT':
                await bot.send_message(-1001878714474, f'Ставка зашла, текущая цена - {now_price}')
            else:
                await bot.send_message(-1001878714474, f'Ставка не зашла, текущая цена - {now_price}')
            await asyncio.sleep(120)



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['start', 'help'])
