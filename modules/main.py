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

bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)


@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("**Welcome to the download bot! Send a .txt file containing the links to download.**")


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Bot stopped.**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["Robin"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('**Please send the text file containing the links to download:**')
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
    
    await editable.edit(f"**Total links found: {len(links)}**\n\n**Send a message with the desired resolution (144, 240, 360, 480, 720, 1080).**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter a batch name:**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    
    await editable.edit("**Enter the desired resolution (144, 240, 360, 480, 720, 1080):**")
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
    
    await editable.edit("**Enter a caption to add or send 'Robin' for default caption:**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == 'Robin':
        MR = "Default Caption"
    else:
        MR = raw_text3
   
    await editable.edit("**Now send the thumb url or 'no' if you don't want to set a thumbnail:**")
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

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "playlist.m3u8" in url:
                await handle_m3u8_link(bot, m, url, count, raw_text0, res, MR, thumb)
            elif "psitoffers.store" in url:
                await handle_drm_content(bot, m, url, count, raw_text0, res, MR, thumb)
            else:
                await handle_regular_link(bot, m, url, count, raw_text0, res, MR, thumb)

            count += 1

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("**Downloads completed successfully!**")


async def handle_regular_link(bot, m, url, count, raw_text0, res, MR, thumb):
    # Your code to handle regular links goes here
    pass


async def handle_m3u8_link(bot, m, url, count, raw_text0, res, MR, thumb):
    # Your code to handle m3u8 playlist links goes here
    pass


async def handle_drm_content(bot, m, url, count, raw_text0, res, MR, thumb):
    # Your code to handle DRM-protected content goes here
    pass


bot.run()
