from pyrogram import Client, enums, filters
from pyrogram.types import ReplyKeyboardMarkup, Message
from pyrogram.errors import SessionPasswordNeeded, AuthKeyUnregistered, ChatAdminRequired
from kvsqlite.sync import Client as Database
from datetime import datetime
from config import API_ID, API_HASH, BOT_TOKEN  # Import from config

# Initialize bot
bot = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Database to store sessions
data = Database("session_data.bot")

# In-memory session management
sessions = {}
check_with_sessions = {}

# Configurable video link
INTRO_VIDEO = "https://t.me/yyyyyy3w/31"

# Create bot reply buttons
def create_buttons():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["Start Check", "Add Session", "Show Sessions"],
            ["Current Time", "Bot Info", "Programmer"],
            ["Programmer's Channel"]
        ],
        resize_keyboard=True
    )

# Start command handler
@bot.on_message(filters.command("start"))
async def start_message(client, message: Message):
    await message.reply_video(
        INTRO_VIDEO,
        caption="""Welcome to the bot for retrieving *your deleted groups*. Send commands now.
Bot programmer: [Sofi](t.me/M02MM)""",
        parse_mode="Markdown",
        reply_markup=create_buttons()
    )

# General message handler
@bot.on_message(filters.text & ~filters.command())
async def handle_all_messages(client, message: Message):
    if message.text.startswith("/"):
        return  # Ignore commands entirely if you add filters
    # Proceed other cases, all the main business here

    if text == "Start Check":
        await message.reply("Initiating group check...")
        await check_left_groups(client, message)
    elif text == "Programmer":
        await message.reply("- Bot Programmer: [Sofi](t.me/M02MM)", parse_mode="Markdown")
    elif text == "Programmer's Channel":
        await message.reply("- Programmer's Channel: [Python Tools](t.me/uiujq)", parse_mode="Markdown")
    elif text == "Bot Info":
        await message.reply("This bot retrieves your group data and simplifies access.")
    elif text == "Add Session":
        await message.reply("Send the *Pyrogram* session string now.", parse_mode="Markdown")
        sessions[user_id] = "add"
    elif text == "Show Sessions":
        saved_session = data.get(f"session_{user_id}")
        if saved_session:
            await message.reply(f"Your session:\n{saved_session}")
        else:
            await message.reply("No session found!")
    elif user_id in sessions and sessions[user_id] == "add":
        session_data = message.text.strip()
        await message.reply("Verifying session...")
        await check_session(client, message, user_id, session_data)
        del sessions[user_id]
    elif text == "Current Time":
        current_time = datetime.now().strftime("%I:%M:%S %p")
        await message.reply(f"*- Current time is:* `{current_time}`", parse_mode="Markdown")

# Session verification and saving
async def check_session(client, message, user_id, session_data):
    try:
        user_client = Client("user_session", session_string=session_data, api_id=API_ID, api_hash=API_HASH)
        await user_client.start()

        me = await user_client.get_me()
        data.set(f"session_{user_id}", session_data)
        check_with_sessions[user_id] = session_data
        await message.reply(f"Session saved ✅\nWelcome, {me.first_name}!")
        await user_client.stop()
    except (AuthKeyUnregistered, SessionPasswordNeeded):
        await message.reply("Session expired or invalid ❌")
    except Exception as e:
        await message.reply(f"An unexpected error occurred: {str(e)}")

# Check left groups owned by user
async def check_left_groups(client, message: Message):
    user_id = message.from_user.id
    session_data = check_with_sessions.get(user_id) or data.get(f"session_{user_id}")

    if not session_data:
        await message.reply("No session added!")
        return

    try:
        user_client = Client("group_checker", session_string=session_data, api_id=API_ID, api_hash=API_HASH)
        await user_client.start()

        groups_found = False

        async for dialog in user_client.get_dialogs():
            c = dialog.chat
            if c.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP] and c.is_creator:
                groups_found = True
                try:
                    link = f"https://t.me/{c.username}" if c.username else (await user_client.get_chat(c.id)).invite_link
                    await message.reply(f"**Group Name:** {c.title}\n**Group Link:** {link}", parse_mode="Markdown")
                except ChatAdminRequired:
                    await message.reply(f"Error in {c.title}: Bot needs admin privileges to export invite link.")
                except Exception as e:
                    await message.reply(f"Error in {c.title}: {str(e)}")

        if not groups_found:
            await message.reply("User does not own any group.")
        
        await user_client.stop()
    except Exception as e:
        await message.reply(f"Failed checking groups: {str(e)}")

# Run the bot
bot.run()
