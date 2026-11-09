import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import TOKEN
from handlers import register_all_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def setup_bot_commands():
    commands = [
        BotCommand(command="start", description="🔄 منوی اصلی ربات"),
        BotCommand(command="prices", description="💰 تابلوی زنده طلا، سکه و ارز"),
        BotCommand(command="music", description="🎵 جستجو و دانلود آهنگ"),
        BotCommand(command="video", description="📥 دانلود ویدیو و اینستاگرام"),
        BotCommand(command="fonts", description="🔤 استودیو زیبانویسی و فونت"),
        BotCommand(command="date", description="📅 تاریخ و ساعت رسمی"),
        BotCommand(command="me", description="👤 مشخصات حساب کاربری"),
    ]
    await bot.set_my_commands(commands)

async def main():
    register_all_handlers(dp)
    await setup_bot_commands()
    print("🚀 ربات ماژولار لوپ با منوی دستورات کامل روشن شد...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())