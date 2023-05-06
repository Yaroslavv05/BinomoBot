import asyncio
# from callbacks.user import register_handlers_callback
from aiogram import executor
from create_bot import dp
from telegram_bot.handlers import user
from aiogram import types, Dispatcher


async def send_messages(dp):
    # Create tasks for the user functions, passing a message argument to each task
    task0 = asyncio.create_task(user.welcome())
    task1 = asyncio.create_task(user.bonus())
    task2 = asyncio.create_task(user.check_daily_time())
    task3 = asyncio.create_task(user.send_every_10_minutes())

    await asyncio.gather(task0, task1, task2, task3)


if __name__ == "__main__":
    user.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=send_messages)
