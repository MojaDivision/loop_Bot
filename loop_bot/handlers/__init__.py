from aiogram import Dispatcher
from .start import router as start_router
from .music import router as music_router
from .video import router as video_router
from .prices import router as prices_router
from .fonts import router as fonts_router
from .utils import router as utils_router

def register_all_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(music_router)
    dp.include_router(video_router)
    dp.include_router(prices_router)
    dp.include_router(fonts_router)
    dp.include_router(utils_router)
