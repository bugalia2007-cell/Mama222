import time
import asyncio
import os
from Easy_F import hrb, hrt
from pyrogram.errors import FloodWait

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

timer = Timer()

async def progress_bar(current, total, reply, start):
    if timer.can_send():
        diff = time.time() - start
        if diff < 1:
            return
        perc  = f"{current * 100 / total:.1f}%"
        speed = current / diff
        sp    = str(hrb(speed)) + "ps"
        tot   = hrb(total)
        cur   = hrb(current)
        try:
            await reply.edit(
                f'`┌ 𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨 📈 -【 {perc} 】\n'
                f'├ 𝙎𝙥𝙚𝙚𝙙 🧲 -【 {sp} 】\n'
                f'└ 𝙎𝙞𝙯𝙚 📂 -【 {cur} / {tot} 】`'
            )
        except FloodWait as e:
            # ✅ Fixed: e.x → e.value (new Pyrogram API)
            # ✅ Fixed: time.sleep → await asyncio.sleep (async safe)
            await asyncio.sleep(e.value)
        except Exception:
            pass
