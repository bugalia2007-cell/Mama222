import subprocess
import datetime
import asyncio
import os
import requests
import time
from p_bar import progress_bar
import aiohttp
import aiofiles
import concurrent.futures
from pyrogram.types import Message
from pyrogram import Client

def duration(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    try:
        return float(result.stdout)
    except:
        return 0

def exec_cmd(cmd):
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.stdout.decode()

def pull_run(work, cmds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=work) as executor:
        executor.map(exec_cmd, cmds)

async def aio(url, name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(k, mode='wb') as f:
                    await f.write(await resp.read())
    return k

async def download(url, name):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(ka, mode='wb') as f:
                    await f.write(await resp.read())
    return ka

def parse_vid_info(info):
    info = info.strip().split("\n")
    new_info = []
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i = i.split("|")[0].split(" ", 2)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info

def vid_info(info):
    info = info.strip().split("\n")
    new_info = dict()
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i = i.split("|")[0].split(" ", 3)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.update({f'{i[2]}': f'{i[0]}'})
            except:
                pass
    return new_info

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'

def old_download(url, file_name, chunk_size=1024 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"

async def download_video(url, cmd, name):
    # ✅ Fixed: os.system() → asyncio subprocess (async safe)
    download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
    proc = await asyncio.create_subprocess_shell(download_cmd)
    await proc.wait()
    for ext in ["", ".webm", ".mp4", ".mkv", ".mp4.webm"]:
        check = name if not ext else (os.path.splitext(name)[0] + ext)
        if os.path.isfile(check):
            return check
    # ✅ Fixed: os.path.isfile.splitext[0] → os.path.splitext(name)[0]
    return os.path.splitext(name)[0] + ".mp4"

async def send_doc(bot: Client, m: Message, cc, ka, cc1, prog, count, name):
    reply = await m.reply_text(f"Uploading - `{name}`")
    # ✅ Fixed: time.sleep() → await asyncio.sleep()
    await asyncio.sleep(1)
    start_time = time.time()
    await m.reply_document(ka, caption=cc1)
    count += 1
    await reply.delete(True)
    await asyncio.sleep(1)
    if os.path.exists(ka):
        os.remove(ka)
    await asyncio.sleep(3)

async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog):
    subprocess.run(
        f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg" -y',
        shell=True, stderr=subprocess.DEVNULL
    )
    await prog.delete(True)
    reply = await m.reply_text(f"**Uploading ...** - `{name}`")

    # ✅ Fixed: thumb == "no" comparison bug
    if thumb and thumb != "no" and os.path.exists(thumb):
        thumbnail = thumb
    elif os.path.exists(f"{filename}.jpg"):
        thumbnail = f"{filename}.jpg"
    else:
        thumbnail = None

    dur = int(duration(filename))
    start_time = time.time()

    try:
        await m.reply_video(
            filename, caption=cc, supports_streaming=True,
            height=720, width=1280, thumb=thumbnail, duration=dur,
            progress=progress_bar, progress_args=(reply, start_time)
        )
    except Exception:
        await m.reply_document(filename, caption=cc, progress=progress_bar, progress_args=(reply, start_time))

    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(f"{filename}.jpg"):
        os.remove(f"{filename}.jpg")
    await reply.delete(True)
