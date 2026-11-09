import html
import logging
from datetime import datetime
import jdatetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from config import CHANNEL_ID
from keyboards.inline import get_back_button

router = Router()

def get_datetime_text():
    now = datetime.now()
    j_now = jdatetime.datetime.now()
    return (
        "📅 <b>زمان و تاریخ دقیق امروز:</b>\n\n"
        f"🇮🇷 <b>شمسی:</b> {j_now.strftime('%Y/%m/%d - %A')}\n"
        f"🌍 <b>میلادی:</b> {now.strftime('%Y-%m-%d')}\n"
        f"⏰ <b>ساعت رسمی:</b> {now.strftime('%H:%M:%S')}\n\n"
        f"🤖 <b>ربات لوپ | {CHANNEL_ID}</b>"
    )

def get_user_info_text(u):
    name = html.escape(u.full_name)
    username = f"@{html.escape(u.username)}" if u.username else "ندارد"
    premium = "بله ⭐" if u.is_premium else "خیر"
    return (
        "👤 <b>پروفایل کاربری شما:</b>\n\n"
        f"▫️ <b>نام:</b> {name}\n"
        f"▫️ <b>آیدی عددی:</b> <code>{u.id}</code>\n"
        f"▫️ <b>نام کاربری:</b> {username}\n"
        f"▫️ <b>پریمیوم:</b> {premium}\n\n"
        f"🤖 <b>ربات لوپ | {CHANNEL_ID}</b>"
    )

@router.message(Command("date"))
async def date_cmd(message: Message):
    await message.answer(get_datetime_text(), reply_markup=get_back_button(), parse_mode="HTML")

@router.callback_query(F.data == "date_time")
async def show_date_time(call: CallbackQuery):
    await call.message.edit_text(get_datetime_text(), reply_markup=get_back_button(), parse_mode="HTML")
    await call.answer()

@router.message(Command("me"))
async def me_cmd(message: Message):
    await message.answer(get_user_info_text(message.from_user), reply_markup=get_back_button(), parse_mode="HTML")

@router.callback_query(F.data == "user_info")
async def show_user_info(call: CallbackQuery):
    try:
        await call.message.edit_text(get_user_info_text(call.from_user), reply_markup=get_back_button(), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error in user_info: {e}")
    await call.answer()