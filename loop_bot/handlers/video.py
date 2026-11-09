import os
import logging
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from config import BOT_USERNAME, CHANNEL_ID
from keyboards.inline import get_back_button, get_media_footer_menu
from services.downloader import sync_download_video
from .states import BotStates

router = Router()
RLM = "\u200f"

@router.callback_query(F.data == 'video_download')
async def ask_video_url(call: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.waiting_for_video_url)
    text = (
        f'{RLM}📥 <b>دانلودر هوشمند ویدیو و ریلز (Loop Downloader)</b>\n\n'
        f'{RLM}لینک ریلز یا پست اینستاگرام، پینترست یا یوتیوب را ارسال کنید:\n'
        f'{RLM}🔄 برای بازگشت: /start'
    )
    try:
        await call.message.edit_text(text, reply_markup=get_back_button(), parse_mode='HTML')
    except Exception:
        await call.message.answer(text, reply_markup=get_back_button(), parse_mode='HTML')
    await call.answer()

@router.message(Command('video'))
async def video_cmd(message: Message, state: FSMContext):
    await state.set_state(BotStates.waiting_for_video_url)
    await message.answer(
        f'{RLM}📥 لینک ویدیوی اینستاگرام یا پینترست را ارسال کنید:\n{RLM}🔄 لغو: /start',
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )

async def handle_video_download(message: Message, url: str):
    status_msg = await message.reply(f'{RLM}⏳ <b>ربات لوپ</b> در حال دریافت و دانلود ویدیو است... شکیبا باشید.', parse_mode='HTML')
    try:
        filename, title = await asyncio.to_thread(sync_download_video, url)
        if not filename or not os.path.exists(filename):
            raise FileNotFoundError("فایل ویدیو یافت نشد.")

        await status_msg.edit_text(f'{RLM}📤 در حال آپلود ویدیو به چت...')
        video_file = FSInputFile(filename)
        bot_sign = BOT_USERNAME if BOT_USERNAME else CHANNEL_ID
        caption = (
            f'{RLM}🎬 <b>ویدیوی شما با بالاترین کیفیت دانلود شد!</b>\n'
            f'{RLM}───────────────────\n'
            f'{RLM}🔄 شروع مجدد: /start | 📥 دانلود بعدی: /video\n\n'
            f'{RLM}🤖 <b>دانلود شده از ربات لوپ | {bot_sign}</b>\n'
            f'{RLM}📢 <b>کانال رسمی لوپ:</b> {CHANNEL_ID}'
        )
        await message.reply_video(
            video=video_file,
            caption=caption,
            parse_mode='HTML',
            reply_markup=get_media_footer_menu()
        )
        await status_msg.delete()
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        logging.error(f'Video download error: {e}')
        await status_msg.edit_text(
            f'{RLM}⚠️ متأسفانه ویدیو دانلود نشد!\n'
            f'{RLM}(احتمالاً پیج خصوصی است یا لینک نامعتبر است).\n\n'
            f'{RLM}🔄 شروع مجدد: /start',
            reply_markup=get_back_button(),
            parse_mode='HTML'
        )

@router.message(BotStates.waiting_for_video_url)
async def process_video_state(message: Message, state: FSMContext):
    await state.clear()
    await handle_video_download(message, message.text.strip())

# قابلیت تشخیص خودکار لینک بدون نیاز به زدن دکمه!
@router.message(F.text.regexp(r'https?://(?:www\.)?(?:instagram\.com|pin\.it|pinterest\.com|tiktok\.com|youtu\.be|youtube\.com)/\S+'))
async def auto_link_detector(message: Message, state: FSMContext):
    await state.clear()
    await handle_video_download(message, message.text.strip())