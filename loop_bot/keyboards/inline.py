from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_URL

def get_main_menu():
    buttons = [
        [
            InlineKeyboardButton(text="🎵 سرچ و دانلود موزیک", callback_data="music_search"),
            InlineKeyboardButton(text="📥 دانلودر ویدیو و ریلز", callback_data="video_download")
        ],
        [
            InlineKeyboardButton(text="💰 تابلوی طلا، سکه و ارز", callback_data="prices"),
            InlineKeyboardButton(text="🔤 فونت و زیبانویسی", callback_data="fonts")
        ],
        [
            InlineKeyboardButton(text="📅 تقویم و زمان", callback_data="date_time"),
            InlineKeyboardButton(text="👤 اطلاعات کاربری من", callback_data="user_info")
        ],
        [
            InlineKeyboardButton(text="📢 کانال رسمی لوپ (Loop)", url=CHANNEL_URL)
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 بازگشت به منوی اصلی", callback_data="back_home")]
    ])

# کیبورد زیر فایل‌های موزیک و ویدیو (فوق‌العاده مرتب و ۲ ردیفه)
def get_media_footer_menu():
    buttons = [
        [
            InlineKeyboardButton(text="🎵 دانلود آهنگ بعدی", callback_data="music_search"),
            InlineKeyboardButton(text="📥 دانلود ویدیوی بعدی", callback_data="video_download")
        ],
        [
            InlineKeyboardButton(text="📢 کانال لوپ", url=CHANNEL_URL),
            InlineKeyboardButton(text="🔄 منوی اصلی", callback_data="restart_bot")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# کیبورد زیر تابلوی زنده قیمت‌ها
def get_prices_menu():
    buttons = [
        [
            InlineKeyboardButton(text="🔄 به‌روزرسانی زنده نرخ‌ها", callback_data="prices")
        ],
        [
            InlineKeyboardButton(text="📢 عضویت در کانال", url=CHANNEL_URL),
            InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="back_home")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)