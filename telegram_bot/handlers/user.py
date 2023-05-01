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

users = UsersDatabase()


async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, 'hello!')
    if not users.if_user_exists(message.from_user.id):
        users.create_new_user(message.from_user.id)
        await send_every_10_minutes()


async def send_every_10_minutes():
    while True:
        if work():
            await bot.send_message(-1001878714474, '+[BOT] Тут будет выводиться сигнал каждые 10 минут')
            await asyncio.sleep(300)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['start', 'help'])
