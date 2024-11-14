from pyrogram import Client
import handlers  # This will register handlers without needing `bot`

# Import configuration
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize Pyrogram Client
app = Client(
    "GroupFetchAi",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("Bot is starting...")

# Start the bot
app.run()
