import os
import html
import logging
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from config import BOT_USERNAME, CHANNEL_ID
from keyboards.inline import get_back_button, get_media_footer_menu
from services.downloader import sync_download_music, fetch_thumbnail_bytes
from .states import BotStates

router = Router()
RLM = "\u200f"

@router.callback_query(F.data == "music_search")
async def ask_music_query(call: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.waiting_for_music_query)
    text = (
        f"{RLM}🎵 <b>جستجو و دانلود مستقیم موزیک (YouTube Music)</b>\n\n"
        f"{RLM}نام آهنگ یا خواننده مورد نظرت رو بنویس و بفرست:\n"
        f"{RLM}<i>(مثلاً: شادمهر عقیلی تماشا یا Believer Imagine Dragons)</i>\n\n"
        f"{RLM}🔄 برای بازگشت: /start"
    )
    try:
        await call.message.edit_text(text, reply_markup=get_back_button(), parse_mode="HTML")
    except Exception:
        await call.message.answer(text, reply_markup=get_back_button(), parse_mode="HTML")
    await call.answer()

@router.message(Command("music"))
async def music_cmd(message: Message, state: FSMContext):
    await state.set_state(BotStates.waiting_for_music_query)
    text = (
        f"{RLM}🎵 نام آهنگ یا خواننده مورد نظرت رو بفرست:\n"
        f"{RLM}🔄 لغو و منوی اصلی: /start"
    )
    await message.answer(text, reply_markup=get_back_button(), parse_mode="HTML")

@router.message(BotStates.waiting_for_music_query)
async def process_music_download(message: Message, state: FSMContext):
    query = message.text.strip()
    status_msg = await message.reply(
        f"{RLM}🎧 <b>ربات لوپ</b> در حال جستجو در یوتیوب و دریافت بالاترین کیفیت صوتی... ⏳", 
        parse_mode="HTML"
    )
    
    try:
        filename, title, artist, duration, thumb_url = await asyncio.to_thread(sync_download_music, query)
        if not filename or not os.path.exists(filename):
            raise FileNotFoundError("فایل صوتی یافت نشد.")

        mins, secs = divmod(duration, 60)
        duration_str = f"{mins:02d}:{secs:02d}" if duration else "نامشخص"

        await status_msg.edit_text(f"{RLM}📤 در حال ارسال موزیک به تلگرام...")
        audio_file = FSInputFile(filename)
        thumb_file = await fetch_thumbnail_bytes(thumb_url)

        bot_sign = BOT_USERNAME if BOT_USERNAME else CHANNEL_ID
        caption = (
            f"{RLM}🎵 <b>نام موزیک:</b> {html.escape(title)}\n"
            f"{RLM}🎤 <b>آرتیست:</b> {html.escape(artist)}\n"
            f"{RLM}⏱ <b>مدت زمان:</b> {duration_str}\n"
            f"{RLM}🔊 <b>کیفیت:</b> اورجینال (YouTube 320)\n"
            f"{RLM}───────────────────\n"
            f"{RLM}🔄 شروع مجدد: /start | 🎵 آهنگ بعدی: /music\n\n"
            f"{RLM}🤖 <b>دانلود شده از ربات لوپ | {bot_sign}</b>\n"
            f"{RLM}📢 <b>کانال رسمی لوپ:</b> {CHANNEL_ID}"
        )

        await message.reply_audio(
            audio=audio_file,
            title=title,
            performer=artist,
            duration=duration if duration > 0 else None,
            thumbnail=thumb_file,
            caption=caption,
            parse_mode="HTML",
            reply_markup=get_media_footer_menu()
        )
        await status_msg.delete()
        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        logging.error(f"Music error handled: {e}")
        await status_msg.edit_text(
            f"{RLM}⚠️ متأسفانه آهنگ در یوتیوب پیدا نشد یا سرور فیلترشکن دچار قطعی شد.\n"
            f"{RLM}💡 لطفاً نام آهنگ را دقیق‌تر بفرستید.\n\n"
            f"{RLM}🔄 منوی اصلی: /start",
            reply_markup=get_back_button(),
            parse_mode="HTML"
        )
    
    await state.clear()