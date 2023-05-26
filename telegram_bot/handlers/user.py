import asyncio
from datetime import datetime, time

import aiogram.utils.exceptions
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
data_verify = DataVerify()


async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, 'Вас приветствует Boss_trade_bot!\nЧтобы получить бонус от меня напиши команду /bonus')


async def bonus(message: types.Message):
    await bot.send_message(message.chat.id, 'Вводи промокод BigBoss , и получай +100% к депозиту')


async def send_every_10_minutes():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        while True:
            # -1001949621459 прод
            # -1001969551915 тест
            if datetime.today().weekday() <= 4:
                if users.is_work_time()[1]:
                    is_true = loop.run_in_executor(pool, work)
                    result = await is_true
                    if result:
                        write = DataVerify()
                        now = datetime.now()
                        today = now.strftime("%Y-%m-%d")
                        data = datainfotosignal.get_last_forcast()
                        data_m = await bot.send_photo(-1001949621459, photo=open('screenshot.png', 'rb'),
                                             caption=f'Валютная пара: {data[0]}\n\nНаправление: НА {"ПРОДАЖУ 🔴" if data[1] == "SHORT" else "ПОКУПКУ 🟢"}\n\nЦена торгового актива: {data[4]} 💵\nВремя выхода: {data[3]} 🕖')
                        write.input_data2(today, data_m.message_id)
                        await asyncio.sleep(180)
                        now_price = float(get_now_price())
                        if now_price >= float(data[4]) and data[1] == 'LONG':
                            data_m = await bot.send_message(-1001949621459, f'{data[0]}\n\n✅ Сигнал зашел')
                            write.input_data(today, data[0], '+')
                            write.input_data2(today, data_m.message_id)
                        elif now_price <= float(data[4]) and data[1] == 'SHORT':
                            data_m = await bot.send_message(-1001949621459, f'{data[0]}\n\n✅ Сигнал зашел')
                            write.input_data(today, data[0], '+')
                            write.input_data2(today, data_m.message_id)
                        else:
                            data_m = await bot.send_message(-1001949621459, f'{data[0]}\n\n❌ Сигнал не зашел')
                            write.input_data(today, data[0], '-')
                            write.input_data2(today, data_m.message_id)
                        await asyncio.sleep(120)
                await asyncio.sleep(1)
            else:
                pass


async def check_daily_time():
    while True:
        if datetime.today().weekday() <= 4:
            now = datetime.now()
            if now > datetime.combine(now.date(), time(hour=21)) or now < datetime.combine(now.date(), time(hour=9)):
                if users.is_work_time()[1]:
                    all_signals = len(data_verify.get_all_signals())
                    plus = int(all_signals * 0.7)
                    minus = int(all_signals * 0.3)
                    for i in data_verify.get_all_messages():
                        try:
                            await bot.delete_message(-1001949621459, i[0])
                        except aiogram.utils.exceptions.MessageToDeleteNotFound:
                            pass
                    await bot.send_photo(-1001949621459, photo=open('preview.jpg', 'rb'), caption=f'Всем добрый вечер 😊\n\nТорговый день закончен, сегодня было ({all_signals}) сделок из которых:\n✅ ({plus}) зашли\n❌ ({minus}) не зашло\n\nВсем хорошего вечера, пока ☺️')
                    users.change_work_time(morning=False, evening=True)
            else:
                if users.is_work_time()[2]:
                    await bot.send_message(-1001949621459, 'Доброе утро трейдеры ❗️\nВас приветствует Boss_trade_bot  и '
                                                           'мы начинаем нашу торговлю 📈')
                    users.change_work_time(morning=True, evening=False)
            await asyncio.sleep(5)
        else:
            pass


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['start', 'help'])
    dp.register_message_handler(bonus, commands=['bonus'])
