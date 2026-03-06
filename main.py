import os
from config import Config
from pyrogram import Client, idle
import asyncio
import logging
import tgcrypto
from logging.handlers import RotatingFileHandler
from aiohttp import web
import threading

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

AUTH_USERS = [int(chat) for chat in Config.AUTH_USERS.split(",") if chat.strip() != '']
prefixes = ["/", "~", "?", "!"]
plugins = dict(root="plugins")

def run_web():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = web.Application()
    async def health(request):
        return web.Response(text="Bot is running!")
    app.router.add_get("/", health)
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port, loop=loop)

if __name__ == "__main__":
    t = threading.Thread(target=run_web, daemon=True)
    t.start()

    bot = Client(
        "StarkBot_new",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=20,
        plugins=plugins,
        workers=50,
        in_memory=True,
        takeout=False
    )

    async def main():
        await bot.start()
        bot_info = await bot.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started (c) STARKBOT --->")
        await idle()

    asyncio.run(main())
