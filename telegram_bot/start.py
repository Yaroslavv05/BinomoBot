import asyncio

from handlers import user
# from callbacks.user import register_handlers_callback
from aiogram import executor
from create_bot import dp

if __name__ == "__main__":
    user.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)
