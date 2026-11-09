import os
import glob
import logging
import aiohttp
import yt_dlp
from aiogram.types import BufferedInputFile
from config import DOWNLOAD_DIR

def get_ffmpeg_path():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None

def sync_download_music(query):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    out_tmpl = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    ffmpeg_exe = get_ffmpeg_path()

    # تنظیمات استاندارد و اصلی یوتیوب (دقیقاً مثل نسخه اول بدون دستکاری‌های اضافی)
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': out_tmpl,
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 25,
        'max_filesize': 49 * 1024 * 1024
    }
    if ffmpeg_exe:
        ydl_opts['ffmpeg_location'] = ffmpeg_exe

    # ۱. تلاش مستقیم از یوتیوب (مثل نسخه اولیه)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info and info['entries']:
                info = info['entries'][0]

            filename = ydl.prepare_filename(info)
            if not os.path.exists(filename):
                base_name = os.path.splitext(filename)[0]
                matches = glob.glob(f"{base_name}.*")
                if matches and os.path.getsize(matches[0]) > 0:
                    filename = matches[0]

            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                title = info.get('track') or info.get('title') or 'Music'
                artist = info.get('artist') or info.get('uploader') or 'Loop Music'
                duration = int(info.get('duration') or 0)
                thumb_url = info.get('thumbnail')
                return filename, title, artist, duration, thumb_url
    except Exception as e:
        err_msg = str(e)
        logging.warning(f"YouTube direct failed: {err_msg}")

        # اگر یوتیوب به آی‌پی فیلترشکن گیر داد، استفاده خودکار از سشن مرورگر ویندوز برای باز کردن قفل
        if "confirm you’re not a bot" in err_msg or "Sign in" in err_msg or "403" in err_msg:
            for browser in ['edge', 'chrome', 'firefox']:
                try:
                    cookie_opts = ydl_opts.copy()
                    cookie_opts['cookiesfrombrowser'] = (browser,)
                    with yt_dlp.YoutubeDL(cookie_opts) as ydl_c:
                        info = ydl_c.extract_info(query, download=True)
                        if 'entries' in info and info['entries']:
                            info = info['entries'][0]

                        filename = ydl_c.prepare_filename(info)
                        if not os.path.exists(filename):
                            base_name = os.path.splitext(filename)[0]
                            matches = glob.glob(f"{base_name}.*")
                            if matches and os.path.getsize(matches[0]) > 0:
                                filename = matches[0]

                        if os.path.exists(filename) and os.path.getsize(filename) > 0:
                            title = info.get('track') or info.get('title') or 'Music'
                            artist = info.get('artist') or info.get('uploader') or 'Loop Music'
                            duration = int(info.get('duration') or 0)
                            thumb_url = info.get('thumbnail')
                            return filename, title, artist, duration, thumb_url
                except Exception:
                    continue

    # ۲. پشتیبان ساندکلاد در صورتی که آی‌پی یوتیوب کاملاً بلاک باشد
    sc_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_tmpl,
        'default_search': 'scsearch1',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 20,
        'max_filesize': 49 * 1024 * 1024
    }
    if ffmpeg_exe:
        sc_opts['ffmpeg_location'] = ffmpeg_exe

    try:
        with yt_dlp.YoutubeDL(sc_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info and info['entries']:
                info = info['entries'][0]

            filename = ydl.prepare_filename(info)
            if not os.path.exists(filename):
                base_name = os.path.splitext(filename)[0]
                matches = glob.glob(f"{base_name}.*")
                if matches and os.path.getsize(matches[0]) > 0:
                    filename = matches[0]

            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                title = info.get('title') or 'Music'
                artist = info.get('uploader') or 'Loop Music'
                duration = int(info.get('duration') or 0)
                thumb_url = info.get('thumbnail')
                return filename, title, artist, duration, thumb_url
    except Exception as e:
        logging.error(f"SoundCloud fallback failed: {e}")

    raise FileNotFoundError("متأسفانه این آهنگ در یوتیوب دانلود نشد.")

def sync_download_video(url):
    out_tmpl = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    ffmpeg_exe = get_ffmpeg_path()
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': out_tmpl,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 25,
        'max_filesize': 49 * 1024 * 1024
    }
    if ffmpeg_exe:
        ydl_opts['ffmpeg_location'] = ffmpeg_exe

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if not os.path.exists(filename):
            base_name = os.path.splitext(filename)[0]
            matches = glob.glob(f"{base_name}.*")
            if matches:
                filename = matches[0]
        title = info.get('title') or 'ویدیو'
        return filename, title

async def fetch_thumbnail_bytes(url):
    if not url:
        return None
    try:
        timeout = aiohttp.ClientTimeout(total=4)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    return BufferedInputFile(data, filename="cover.jpg")
    except Exception:
        pass
    return None