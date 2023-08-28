from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
event_frequency_type =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Одноразова подія", callback_data="one_time_event")],
    [InlineKeyboardButton(text="Повторювана подія", callback_data="recurring_event")],
])


event_frequency_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Кожен місяць", callback_data="1"), InlineKeyboardButton(text="Кожні 3 місяці", callback_data="3")],
    [InlineKeyboardButton(text="Кожні 6 місяців", callback_data="6"), InlineKeyboardButton(text="Кожен рік", callback_data="12")],
])

