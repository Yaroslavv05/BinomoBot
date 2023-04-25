import asyncio
import logging
import json

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta

from BinomoBot.telegram_bot.create_bot import bot, dp

async def welcome(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'hello!')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['start', 'help'])
