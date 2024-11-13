from pyrogram import Client
import handlers
import config

# Initialize the bot client
bot = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Register handlers
bot.add_handler(handlers.start_message)
bot.add_handler(handlers.handle_all_messages)

# Run the bot
if __name__ == "__main__":
    bot.run()
print("Bot is starting...")
bot.run()
print("Bot has started.")
