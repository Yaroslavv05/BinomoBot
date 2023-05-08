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
data_verify = DataVerify()


async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, 'Вас приветствует Boss_trade_bot!\nЧтобы получить бонус от меня напиши команду /bonus')


async def bonus(message: types.Message):
    await bot.send_message(message.chat.id, 'Вводи промокод BigBoss , и получай +100% к депозиту')


async def send_every_10_minutes():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        while True:
            # -1001878714474 прод
            # -1001969551915 тест
            if users.is_work_time()[1]:
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
                    now = datetime.now()
                    today = now.strftime("%Y-%m-%d")
                    write = DataVerify()
                    if now_price >= float(data[4]) and data[1] == 'LONG':
                        write.input_data(today, data[0], '+')
                        await bot.send_message(-1001969551915, f'{data[0]}\n\n✅ Сигнал зашел')
                    elif now_price <= float(data[4]) and data[1] == 'SHORT':
                        write.input_data(today, data[0], '+')
                        await bot.send_message(-1001969551915, f'{data[0]}\n\n✅ Сигнал зашел')
                    else:
                        write.input_data(today, data[0], '-')
                        await bot.send_message(-1001969551915, f'{data[0]}\n\n❌ Сигнал не зашел')
                    await asyncio.sleep(120)
            await asyncio.sleep(1)


async def check_daily_time():
    while True:
        now = datetime.now()
        if now > datetime.combine(now.date(), time(hour=21)) or now < datetime.combine(now.date(), time(hour=9)):
            if users.is_work_time()[1]:
                minus = 0
                plus = 0

                for i in data_verify.get_all_signals():
                    if i[2] == '-':
                        minus+=1
                    elif i[2] == '+':
                        plus+=1
                await bot.send_message(-1001969551915, 'Бот заканчивает анализ и торговлю на сегодня , всем пока 👋')
                users.change_work_time(morning=False, evening=True)
        else:
            if users.is_work_time()[2]:
                await bot.send_message(-1001969551915, 'Доброе утро трейдеры ❗️\nВас приветствует Boss_trade_bot  и '
                                                       'мы начинаем нашу торговлю 📈')
                users.change_work_time(morning=True, evening=False)
        await asyncio.sleep(5)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['start', 'help'])
    dp.register_message_handler(bonus, commands=['bonus'])
