@stark.on_message()
async def debug_all(bot, m):
    print(f"Message: {m.text} from {m.from_user.id}")
from pyrogram import filters
from pyrogram import Client as stark
from pyrogram.types import Message
from main import LOGGER, prefixes, AUTH_USERS
from config import Config
import os
import sys


@stark.on_message()
async def debug_all(bot, m):
    print(f"Message received: {m.text} from {m.from_user.id}")


@stark.on_message(filters.command(["start"]))
async def Start_msg(bot: stark, m: Message):
    await m.reply_text("**Hi i am All in One Extractor Bot** 🤖\n\n**Bot Owner: YASH**")


@stark.on_message(filters.command(["ping"]))
async def ping(bot: stark, m: Message):
    await m.reply_text("**Pong! 🏓 Bot is alive!**")


@stark.on_message(filters.command(["restart"]))
async def restart_handler(_, m):
    if m.from_user.id not in AUTH_USERS:
        return
    await m.reply_text("Restarting... ♻️")
    os.execl(sys.executable, sys.executable, *sys.argv)


@stark.on_message(filters.command(["log"]))
async def log_msg(bot: stark, m: Message):
    if m.from_user.id not in AUTH_USERS:
        return
    await bot.send_document(m.chat.id, "log.txt")
