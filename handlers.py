from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import config

# Dictionary to store session data temporarily
sessions = {}

# Function to create inline buttons using Pyrogram
def create_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Start Check", callback_data="start_check")],
        [InlineKeyboardButton("Add Session", callback_data="add_session")],
        [InlineKeyboardButton("Show Sessions", callback_data="show_sessions")],
        [InlineKeyboardButton("Current Time", callback_data="current_time")],
        [InlineKeyboardButton("Programmer", callback_data="programmer")],
        [InlineKeyboardButton("Programmer's Channel", callback_data="programmer_channel")],
        [InlineKeyboardButton("Bot Info", callback_data="bot_info")]
    ])

# Start Message
@Client.on_message(filters.command("start"))
async def start_message(client, message):
    await message.reply_video(
        "https://t.me/yyyyyy3w/31",
        caption="""
Welcome to the bot for retrieving *your deleted groups*. 
Bot programmer: [Sofi](t.me/M02MM)
        """,
        parse_mode="markdown",
        reply_markup=create_buttons()
    )

# Callback Handler
@Client.on_callback_query()
async def handle_callback_query(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "start_check":
        await callback_query.message.reply("Checking groups... 🔍")
        await check_groups(callback_query)
    elif data == "add_session":
        sessions[user_id] = "add"
        await callback_query.message.reply("Send me your session data now.")
    elif data == "show_sessions":
        session_data = sessions.get(user_id)
        await callback_query.message.reply(session_data or "No session added!")
    elif data == "current_time":
        current_time = datetime.now().strftime("%I:%M:%S")
        await callback_query.message.reply(f"*- Current time:* `{current_time}`", parse_mode="markdown")
    elif data == "programmer":
        await callback_query.message.reply("Programmer: [Sofi](t.me/M02MM)", disable_web_page_preview=True)
    elif data == "programmer_channel":
        await callback_query.message.reply("Channel: [Python Tools](t.me/uiujq)", disable_web_page_preview=True)
    elif data == "bot_info":
        await callback_query.message.reply("This bot helps retrieve group data. Enjoy!")

# Function for Group Check
async def check_groups(callback_query):
    user_id = callback_query.from_user.id
    session_data = sessions.get(user_id)

    if not session_data:
        await callback_query.message.reply("No session available!")
        return

    try:
        async with TelegramClient(StringSession(session_data), config.API_ID, config.API_HASH) as client:
            async for dialog in client.iter_dialogs():
                if dialog.is_group:
                    await callback_query.message.reply(f"Group: {dialog.title}")
    except Exception as e:
        await callback_query.message.reply(f"An error occurred: {str(e)}")
