import asyncio
# from callbacks.user import register_handlers_callback
from aiogram import executor
from create_bot import dp
from telegram_bot.handlers import user
from aiogram import types, Dispatcher


async def send_messages():
    # Create tasks for the user functions, passing a message argument to each task
    task2 = asyncio.create_task(user.check_daily_time())
    task3 = asyncio.create_task(user.send_every_10_minutes())
    await asyncio.gather(task2)


async def main():
    asyncio.create_task(send_messages())
    user.register_handlers_client(dp)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
