from aiogram.fsm.state import StatesGroup, State

class NewEvent(StatesGroup):
    event_name = State()
    event_date = State()
    event_period = State()

class MainMenu(StatesGroup):
    user_id = State()