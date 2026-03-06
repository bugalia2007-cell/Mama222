import os
from config import Config
from pyrogram import Client, idle
import asyncio
import logging
import tgcrypto
from logging.handlers import RotatingFileHandler
from aiohttp import web

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# Auth Users
AUTH_USERS = [int(chat) for chat in Config.AUTH_USERS.split(",") if chat.strip() != '']

# Prefixes
prefixes = ["/", "~", "?", "!"]

plugins = dict(root="plugins")

# Simple web server — Render ka "No open ports" error fix
async def health(request):
    return web.Response(text="Bot is running!")

async def start_web():
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    LOGGER.info(f"Web server started on port {port}")

if __name__ == "__main__":
    bot = Client(
        "StarkBot_new",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=20,
        plugins=plugins,
        workers=50
    )

    async def main():
        await start_web()
        await bot.start()
        bot_info = await bot.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started (c) STARKBOT --->")
        await idle()

    asyncio.run(main())
    LOGGER.info(f"<---Bot Stopped-->")
