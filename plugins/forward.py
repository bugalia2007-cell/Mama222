import requests
import json
import subprocess
import helper
from pyromod import listen
from pyrogram.types import Message
import tgcrypto
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import time
import os
import sys
from pyrogram import Client as bot
from main import LOGGER, prefixes, AUTH_USERS
from config import Config


@bot.on_message(
    filters.private &
    filters.incoming &
    filters.command("forward", prefixes=prefixes)
)
async def forward(bot: Client, m: Message):
    if m.from_user.id not in AUTH_USERS:
        return

    msg = await bot.listen(m.chat.id)
    if not msg.forward_from_chat:
        await m.reply_text("❌ Pehle kisi channel ka message forward karo!")
        return
    t_chat = msg.forward_from_chat.id

    msg1 = await bot.listen(m.chat.id)
    if not msg1.forward_from_chat:
        await m.reply_text("❌ Starting message forward karo!")
        return

    msg2 = await bot.listen(m.chat.id)
    if not msg2.forward_from_chat:
        await m.reply_text("❌ Ending message forward karo!")
        return

    i_chat = msg1.forward_from_chat.id
    s_msg = int(msg1.forward_from_message_id)
    f_msg = int(msg2.forward_from_message_id) + 1

    await m.reply_text('**Forwarding Started...**')
    try:
        for i in range(s_msg, f_msg):
            try:
                await bot.copy_message(
                    chat_id=t_chat,
                    from_chat_id=i_chat,
                    message_id=i
                )
            except Exception:
                continue
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done Forwarding ✅")
