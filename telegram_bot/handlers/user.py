import asyncio
from datetime import datetime, time
from aiogram import types, Dispatcher
from soft.db.VerifyDB import DataVerify
from telegram_bot.create_bot import bot
from telegram_bot.utils.database import UsersDatabase
from soft.signal_generation import work
from soft.db.InfoToSignalDB import DataInfoToSignal
from telegram_bot.Verirfy import get_now_price
import concurrent.futures

users = UsersDatabase()
datainfotosignal = DataInfoToSignal()


async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, 'hello!')
    if not users.if_user_exists(message.from_user.id):
        users.create_new_user(message.from_user.id)
        await send_every_10_minutes()


async def send_every_10_minutes():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        while True:
            # -1001878714474 прод
            # -1001969551915 тест
            is_true = loop.run_in_executor(pool, work)
            result = await is_true
            if result:
                data = datainfotosignal.get_last_forcast()
                await bot.send_photo(-1001969551915, photo=open('screenshot.png', 'rb'),
                                     caption=f'{data[0]}\n\nИспользуя свой набор индикаторов я вижу силу движения цены в {"нижнюю" if data[1] == "SHORT" else "верхнюю"} зону флета.'
                                             f'\nОткрываем сделку в {"низ" if data[1] == "SHORT" else "вверх"} по заданной валютной паре.\n\nВремя прогноза {data[3]}'
                                     )
                await asyncio.sleep(300)
                now_price = float(get_now_price())
                today = datetime.now()
                if now_price >= float(data[4]) and data[1] == 'LONG':
                    write = DataVerify(today, data[0], '+')
                    write.input_data()
                    await bot.send_message(-1001969551915, f'{data[0]}\n\n✅ Сигнал зашел')
                elif now_price <= float(data[4]) and data[1] == 'SHORT':
                    write = DataVerify(today, data[0], '+')
                    write.input_data()
                    await bot.send_message(-1001969551915, f'{data[0]}\n\n✅ Сигнал зашел')
                else:
                    write = DataVerify(today, data[0], '-')
                    write.input_data()
                    await bot.send_message(-1001969551915, f'{data[0]}\n\n❌ Сигнал не зашел')
                await asyncio.sleep(120)


async def check_daily_time():
    while True:
        now = datetime.now()
        if now > datetime.combine(now.date(), time(hour=19)) or now < datetime.combine(now.date(), time(hour=9)):
            users.change_work_time(False)
        else:
            users.change_work_time(True)
        await asyncio.sleep(5)



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['start', 'help'])
