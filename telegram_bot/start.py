import asyncio
# from callbacks.user import register_handlers_callback
from aiogram import executor
from create_bot import dp
from telegram_bot.handlers import user


async def send_messages(dp):
    # Сделать вторую асинхронную функцию которая скорее всего будет работать в другом потоке которая будет проверять
    # когда писать доброе утро мы начинаем работу..
    asyncio.create_task(user.send_every_10_minutes())


if __name__ == "__main__":
    user.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=send_messages)
