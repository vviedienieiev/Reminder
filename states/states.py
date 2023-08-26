from aiogram.fsm.state import StatesGroup, State

class NewEvent(StatesGroup):
    event_name = State()
    event_recuring_type = State()
    event_date = State()
    event_freq = State()
    check_info = State()
    upload_event = State()

class ChangeEvent(StatesGroup):
    events_list = State()
    selected_event = State()

    get_current_reminders = State()
    add_new_reminder = State()

    delete_approve = State()
