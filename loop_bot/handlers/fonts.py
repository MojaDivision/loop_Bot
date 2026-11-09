import html
import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from config import CHANNEL_ID
from keyboards.inline import get_main_menu, get_back_button
from services.font_engine import ASCII_LETTERS, FONT_STYLES_EN, get_persian_styles
from .states import BotStates

router = Router()

@router.message(Command("fonts"))
async def fonts_cmd(message: Message, state: FSMContext):
    await state.set_state(BotStates.waiting_for_font_text)
    text = (
        "🔤 <b>استودیو زیبانویسی و فونت (فارسی و انگلیسی)</b>\n\n"
        "متن، کلمه یا اسم مورد نظرت رو بفرست:\n"
        "<i>(می‌تونی فارسی بنویسی مثل: لوپ یا انگلیسی مثل: Loop)</i>\n\n"
        "🔄 بازگشت: /start"
    )
    await message.answer(text, reply_markup=get_back_button(), parse_mode="HTML")

@router.callback_query(F.data == "fonts")
async def ask_font_text(call: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.waiting_for_font_text)
    text = (
        "🔤 <b>استودیو زیبانویسی و فونت (فارسی و انگلیسی)</b>\n\n"
        "متن، کلمه یا اسم مورد نظرت رو بفرست:\n"
        "<i>(می‌تونی فارسی بنویسی مثل: لوپ یا انگلیسی مثل: Loop)</i>\n\n"
        "🔄 بازگشت: /start"
    )
    await call.message.edit_text(text, reply_markup=get_back_button(), parse_mode="HTML")
    await call.answer()

@router.message(BotStates.waiting_for_font_text)
async def process_font(message: Message, state: FSMContext):
    user_text = message.text.strip()
    has_persian = bool(re.search(r'[\u0600-\u06FF]', user_text))
    has_english = bool(re.search(r'[a-zA-Z]', user_text))

    result = f"✨ <b>استایل‌های آماده برای متن شما:</b>\n<i>(روی هر متن ضربه بزنید تا کپی شود)</i>\n\n"

    if has_persian or not has_english:
        result += "🇮🇷 <b>استایل‌های فونت فارسی:</b>\n\n"
        for label, styled in get_persian_styles(user_text):
            result += f"🔹 {label}:\n<code>{html.escape(styled)}</code>\n\n"

    if has_english:
        result += "🇬🇧 <b>استایل‌های فونت انگلیسی:</b>\n\n"
        for style_name, styled in FONT_STYLES_EN.items():
            trans_table = str.maketrans(ASCII_LETTERS, styled)
            converted = user_text.translate(trans_table)
            result += f"🔹 {style_name}:\n<code>{html.escape(converted)}</code>\n\n"

        underline_txt = "".join(c + '\u0332' for c in user_text)
        strike_txt = "".join(c + '\u0336' for c in user_text)
        result += f"🔹 𝗨̲𝗻̲𝗱̲𝗲̲𝗿̲𝗹̲𝗶̲𝗻̲𝗲̲ (خط زیر):\n<code>{html.escape(underline_txt)}</code>\n\n"
        result += f"🔹 S̶t̶r̶i̶k̶e̶t̶h̶r̶o̶u̶g̶h̶ (خط خورده):\n<code>{html.escape(strike_txt)}</code>\n\n"

    result += f"🤖 <b>ربات لوپ | {CHANNEL_ID}</b>\n🔄 منوی اصلی: /start"
    await state.clear()
    await message.reply(result, parse_mode="HTML", reply_markup=get_main_menu())