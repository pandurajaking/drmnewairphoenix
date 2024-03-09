import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import api_id, api_hash, bot_token
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Initialize the Pyrogram client
bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Command handler for /start command
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, m: Message):
    await m.reply_text("**Welcome! Use the /Robin command to start downloading files.**")

# Command handler for /stop command
@bot.on_message(filters.command("stop"))
async def stop_command(_, m):
    await m.reply_text("**Bot stopped.**")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Command handler for /Robin command
@bot.on_message(filters.command(["Robin"]))
async def download_links(bot: Client, m: Message):
    # Ask user to send the text file containing the links
    editable = await m.reply_text('**Please send the text file containing the links to download:**')
    input_message = await bot.listen(editable.chat.id)
    x = await input_message.download()
    await input_message.delete(True)

    try:
        with open(x, "r") as f:
            content = f.read()
        links = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', content)
        os.remove(x)
    except Exception as e:
        await m.reply_text(f"Error: {str(e)}")
        os.remove(x)
        return

    await m.reply_text(f"Total links found: {len(links)}")

    for url in links:
        try:
            # Handle each link
            await handle_link(bot, m, url)
        except Exception as e:
            await m.reply_text(f"Error processing link: {url}\n{str(e)}")

    await m.reply_text("All downloads completed.")

# Function to handle each link
async def handle_link(bot: Client, m: Message, url: str):
    # Your code to handle each link goes here
    # You can implement different logic based on the type of link
    # For example:
    if "playlist.m3u8" in url:
        await handle_m3u8_link(bot, m, url)
    elif "psitoffers.store" in url:
        await handle_drm_content(bot, m, url)
    else:
        await handle_other_link(bot, m, url)

# Function to handle m3u8 playlist links
async def handle_m3u8_link(bot: Client, m: Message, url: str):
    # Your code to handle m3u8 playlist links goes here
    pass

# Function to handle PSIT Offers DRM-protected content
async def handle_drm_content(bot: Client, m: Message, url: str):
    # Your code to handle DRM-protected content goes here
    pass

# Function to handle other types of links
async def handle_other_link(bot: Client, m: Message, url: str):
    # Your code to handle other types of links goes here
    pass

# Run the bot
bot.run()
