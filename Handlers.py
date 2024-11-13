from pyrogram import Client, enums, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, UserDeactivated
from pyrogram.types import Chat, Message
from datetime import datetime
import asyncio
import config

# Pyrogram client setup
bot = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

sessions = {}
check_with_sessions = {}

# Create buttons for bot
def create_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_check = types.KeyboardButton("Start Check")
    add_session = types.KeyboardButton("Add Session")
    show_sessions = types.KeyboardButton("Show Sessions")
    show_time = types.KeyboardButton("Current Time")
    programmer = types.KeyboardButton("Programmer")
    programmer_channel = types.KeyboardButton("Programmer's Channel")
    bot_info = types.KeyboardButton("Bot Info")
    markup.add(start_check)
    markup.add(add_session, show_sessions, show_time)
    markup.add(bot_info)
    markup.add(programmer, programmer_channel)
    return markup

# Start command handler
@bot.on_message(filters.command("start"))
def start_message(client, message):
    bot.send_video(
        message.chat.id,
        "https://t.me/yyyyyy3w/31",
        caption="""
Welcome to the bot for retrieving *your deleted groups*. Send commands now.
Bot programmer: [Sofi](t.me/M02MM)
        """,
        parse_mode="Markdown",
        reply_markup=create_buttons()
    )

# Handle all other messages
@bot.on_message(filters.text)
def handle_all_messages(client, message):
    text = message.text
    user_id = message.from_user.id

    if text == "Start Check":
        bot.send_message(message.chat.id, "Checking groups...")
        asyncio.run(check_groups(message))
    elif text == "Programmer":
        bot.send_message(message.chat.id, "- Bot Programmer: [Sofi](t.me/M02MM)", parse_mode="Markdown", disable_web_page_preview=True)
    elif text == "Programmer's Channel":
        bot.send_message(message.chat.id, "- Programmer's Channel: [Python Tools](t.me/uiujq)", parse_mode="Markdown", disable_web_page_preview=True)
    elif text == "Bot Info":
        bot.send_message(message.chat.id, "The bot is simple, no extra info needed. Enjoy!")
    elif text == "Add Session":
        bot.send_message(message.chat.id, "Send the *Pyrogram* session now", parse_mode="Markdown")
        sessions[user_id] = "add"
    elif text == "Show Sessions":
        saved_session = data.get(f"session_{user_id}")
        if saved_session:
            bot.send_message(message.chat.id, saved_session)
        else:
            bot.send_message(message.chat.id, "No session added!")
    elif user_id in sessions and sessions[user_id] == "add":
        session_data = message.text
        try:
            asyncio.run(check_session(message, user_id, session_data))
        except Exception:
            bot.send_message(message.chat.id, "Session expired ❌")
        del sessions[user_id]
    elif text == "Current Time":
        current_time = datetime.now().strftime("%I:%M:%S")
        bot.send_message(message.chat.id, f"*- Current time is:* `{current_time}`", parse_mode="Markdown")

# Session verification and storage function
async def check_session(message, user_id, session_data):
    try:
        # Creating Pyrogram client
        async with bot:
            client = Client("session", session_string=session_data, api_id=config.API_ID, api_hash=config.API_HASH)
            await client.connect()

            # Check if user is authorized
            if not await client.is_user_authorized():
                raise Exception("Session expired ❌")
            
            # Store session if valid
            data.set(f"session_{user_id}", session_data)
            bot.send_message(message.chat.id, "Session saved ✅")
            check_with_sessions[user_id] = session_data
            await client.disconnect()

    except (SessionPasswordNeeded, PhoneCodeInvalid, UserDeactivated):
        bot.send_message(message.chat.id, "Session expired ❌")
    except Exception as e:
        bot.send_message(message.chat.id, f"Session expired ❌. Error: {str(e)}")

# Group checking function
async def check_groups(message):
    user_id = message.from_user.id
    try:
        session_data = check_with_sessions[user_id]
    except KeyError:
        bot.send_message(message.chat.id, "No session added!")
        return

    if session_data:
        bot.send_message(message.chat.id, "Checking...")
        try:
            # Using the stored session
            async with bot:
                client = Client("session", session_string=session_data, api_id=config.API_ID, api_hash=config.API_HASH)
                await client.connect()

                if not await client.is_user_authorized():
                    raise Exception("Session expired ❌")
        except (SessionPasswordNeeded, PhoneCodeInvalid, UserDeactivated):
            bot.send_message(message.chat.id, "Session expired ❌")
        except Exception:
            bot.send_message(message.chat.id, "Session expired ❌")
    else:
        bot.send_message(message.chat.id, "No session added!")
        return

    # Checking for groups and extracting details
    async for dialog in client.get_dialogs():
        try:
            if isinstance(dialog.chat, Chat) and dialog.chat.type == "supergroup":  # Checking for groups
                group_id = dialog.chat.id
                group_name = dialog.chat.title
                group_username = dialog.chat.username or "None"  # Handling if username is None
                group_creation_date = dialog.chat.date
                formatted_date = group_creation_date.strftime('%Y/%m/%d')  # Formatting creation date

                # Fetching member count
                members_count = await client.get_chat_members_count(group_id)

                # Sending group details
                bot.send_message(
                    message.chat.id, 
                    f"""
                    - Group Name: {group_name}
                    - Group Username: @{group_username}
                    - Group ID: {group_id}
                    - Member Count: {members_count}
                    - Creation Date: {formatted_date}
                    """,
                    disable_web_page_preview=True
                )
        except Exception as e:
            print(f"Error while processing group: {e}")

