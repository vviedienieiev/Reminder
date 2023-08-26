from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

change_options =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Додати нагадувалку ⏰", callback_data="add_reminder"), InlineKeyboardButton(text="Видалити подію ❌", callback_data="delete event")],
    [InlineKeyboardButton(text="◀️ Вийти в меню", callback_data="menu")],
])

add_reminder =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Додати ще 1 нагадувалку ⏰", callback_data="add_new_reminder"), InlineKeyboardButton(text="◀️ Вийти в меню", callback_data="menu")],
])
