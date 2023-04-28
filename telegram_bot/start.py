import asyncio

from handlers import user
# from callbacks.user import register_handlers_callback
from aiogram import executor
from create_bot import dp
from BinomoBot.telegram_bot.handlers import user


async def send_messages(dp):
    asyncio.create_task(user.send_every_10_minutes())


if __name__ == "__main__":
    user.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=send_messages)
