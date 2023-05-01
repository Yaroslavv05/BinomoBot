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
            await bot.send_message(-1001878714474, f'+[BOT] Новый сигнал!\nПара - {data[0]}\nПозиция - {data[1]}\n'
                                                   f'Время входа - {data[2]} | Время выхода - {data[3]}\nЦена входа - {data[4]}')
            await asyncio.sleep(300)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['start', 'help'])
