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

# Initialize the bot client
bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Function to handle different types of links
async def handle_other_link(bot: Client, m: Message, url: str):
    if "playlist.m3u8" in url:
        # Handle m3u8 playlist links
        await handle_m3u8_link(bot, m, url)
    elif "cpvod.testbook.com" in url:
        # Handle Testbook CPVOD links
        await handle_testbook_cpvod_link(bot, m, url)
    elif "streaming-cdn.rjlive.in" in url:
        # Handle RJ Live streaming links
        await handle_rjlive_link(bot, m, url)
    elif "psitoffers.store" in url:
        # Handle PSIT Offers DRM-protected links
        await handle_psitoffers_link(bot, m, url)
    else:
        # Handle other types of links
        await handle_generic_link(bot, m, url)

# Function to handle Testbook CPVOD links
async def handle_testbook_cpvod_link(bot: Client, m: Message, url: str):
    # Your code to handle Testbook CPVOD links goes here
    pass

# Function to handle RJ Live streaming links
async def handle_rjlive_link(bot: Client, m: Message, url: str):
    # Your code to handle RJ Live streaming links goes here
    pass

# Function to handle PSIT Offers DRM-protected links
async def handle_psitoffers_link(bot: Client, m: Message, url: str):
    # Your code to handle PSIT Offers DRM-protected links goes here
    pass

# Function to handle other types of links
async def handle_generic_link(bot: Client, m: Message, url: str):
    # Your code to handle other types of links goes here
    pass

# Start command handler
@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("**Welcome to your bot!**")

# Stop command handler
@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Bot stopped**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

# Robin command handler
@bot.on_message(filters.command(["Robin"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('**Send a text file containing the links you want to download**')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
       with open(x, "r") as f:
           content = f.read()
       content = content.split("\n")
       links = []
       for i in content:
           links.append(i.split("://", 1))
       os.remove(x)
    except:
           await m.reply_text("**Invalid file input.**")
           os.remove(x)
           return
    
    await editable.edit(f"**Total links found: {len(links)}**\n\nSend the initial link from where you want to download.")

    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter a name for the batch**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("**Enter the resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"

    await editable.edit("**Enter a caption to add or send 'Robin'**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Robin':
        MR = highlighter 
    else:
        MR = raw_text3

    await editable.edit("**Now send the Thumb URL or send 'no'**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            url = links[i][1]

            await handle_other_link(bot, m, url)

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("**Downloads complete**")

# Run the bot
bot.run()
