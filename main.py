from handlers import bot
from aiogram import Bot, Dispatcher, executor
import asyncio

from config import BOT_TOKEN

# Initialize Aiogram Bot
aio_bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(aio_bot)

print("Bot is starting...")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Start Pyrogram bot
    loop.create_task(bot.start())  # Use 'start()' instead of 'run()' for compatibility with asyncio

    # Start Aiogram bot
    from handlers import setup_aiogram_handlers  # Ensure your handlers are imported here
    setup_aiogram_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
