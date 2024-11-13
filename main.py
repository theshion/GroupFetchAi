from handlers import bot
import logging

# Logging setup for better debugging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        print("Bot is starting...")  # Print when the bot starts
        bot.run()  # Use run() method instead of polling
        print("Bot is running...")  # Print once the bot starts running
    except Exception as e:
        print(f"An error occurred: {e}")  # Print if an error occurs
