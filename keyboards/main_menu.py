from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
main_menu =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Додати нову подію ✏️", callback_data="add_new_event")],
    [InlineKeyboardButton(text="Редагувати подію 🛠️", callback_data="change_existing_event")],
    [InlineKeyboardButton(text="Показати найближчі події 📅", callback_data="show_events")],
])
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Вийти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Вийти в меню", callback_data="menu")]])  