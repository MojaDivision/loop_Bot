from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    waiting_for_font_text = State()
    waiting_for_music_query = State()
    waiting_for_video_url = State()
