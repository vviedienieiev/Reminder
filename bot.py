import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode

from handlers import add_new_event, start, show_nearest_events, change_existing_event

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

@router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(start.router)
    dp.include_router(add_new_event.router)
    dp.include_router(show_nearest_events.router)
    dp.include_router(change_existing_event.router)
    # dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(os.getenv("TG_TOKEN"), parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")