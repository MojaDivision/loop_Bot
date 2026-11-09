import html
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from config import CHANNEL_ID
from keyboards.inline import get_main_menu

router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        f'سلام <b>{html.escape(message.from_user.first_name)}</b> عزیز! 🌸\n'
        f'به <b>ربات هوشمند لوپ (Loop Bot)</b> خوش اومدی ✨\n\n'
        f'📢 کانال رسمی ما: {CHANNEL_ID}\n'
        '👇 لطفاً یکی از قابلیت‌های زیر رو انتخاب کن:'
    )
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode='HTML')

@router.callback_query(F.data == 'restart_bot')
async def restart_bot_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    welcome_text = (
        f'🏠 <b>منوی اصلی ربات لوپ (Loop Bot)</b>\n'
        f'📢 کانال ما: {CHANNEL_ID}\n\n'
        'یکی از گزینه‌های زیر را انتخاب کنید:'
    )
    await call.message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode='HTML')
    await call.answer()

@router.callback_query(F.data == 'back_home')
async def back_to_home(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        f'🏠 <b>منوی اصلی ربات لوپ</b>\n📢 کانال: {CHANNEL_ID}\n\nیک بخش را انتخاب کنید:',
        reply_markup=get_main_menu(),
        parse_mode='HTML'
    )
    await call.answer()
