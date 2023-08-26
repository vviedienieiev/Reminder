from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

yes_no = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✔️", callback_data="yes"), InlineKeyboardButton(text="❌", callback_data="no")],
])