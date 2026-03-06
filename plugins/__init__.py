@stark.on_message()
async def debug_all(bot, m):
    print(f"✅ Message: {m.text} from {m.from_user.id}")from pyrogram import filters
from pyrogram import Client as stark
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from main import LOGGER, prefixes, AUTH_USERS
from config import Config
import os
import sys


@stark.on_message(filters.command(["start"]))
async def Start_msg(bot: stark, m: Message):
    await m.reply_text(
        "**Hi i am All in One Extractor Bot** 🤖\n\n"
        "Press **/pw** for **Physics Wallah**\n\n"
        "Press **/e1** for **E1 Coaching App**\n\n"
        "Press **/vidya** for **Vidya Bihar App**\n\n"
        "Press **/ocean** for **Ocean Gurukul App**\n\n"
        "Press **/winners** for **The Winners Institute**\n\n"
        "Press **/rgvikramjeet** for **Rgvikramjeet App**\n\n"
        "Press **/txt** for **Ankit With Rojgar, The Mission Institute, The Last Exam App**\n\n"
        "Press **/cp** for **Classplus App**\n\n"
        "Press **/cw** for **Careerwill App**\n\n"
        "Press **/khan** for **Khan Gs App**\n\n"
        "Press **/exampur** for **Exampur App**\n\n"
        "Press **/samyak** for **Samayak Ias**\n\n"
        "Press **/mgconcept** for **Mgconcept App**\n\n"
        "Press **/forward** for **Forward messages**\n\n"
        "**𝗕𝗼𝘁 𝗢𝘄𝗻𝗲𝗿 : YASH**"
    )


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
