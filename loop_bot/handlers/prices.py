import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline import get_prices_menu
from services.market import fetch_market_prices

router = Router()

@router.message(Command("prices"))
async def prices_cmd(message: Message):
    status_msg = await message.answer("در حال دریافت آخرین نرخ‌های زنده بازار... ⏳")
    text = await fetch_market_prices()
    await status_msg.edit_text(text, reply_markup=get_prices_menu(), parse_mode="HTML")

@router.callback_query(F.data == "prices")
async def show_prices(call: CallbackQuery):
    await call.answer("در حال بارگذاری تابلوی زنده قیمت‌ها...")
    text = await fetch_market_prices()
    try:
        await call.message.edit_text(text, reply_markup=get_prices_menu(), parse_mode="HTML")
    except Exception as e:
        if "message is not modified" not in str(e):
            await call.message.answer(text, reply_markup=get_prices_menu(), parse_mode="HTML")