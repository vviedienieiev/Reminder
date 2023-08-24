import datetime
import texts

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from database.mongo import db
from keyboards import main_menu

router = Router()
collection_users = db["users"]

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    
    user_id = message.chat.id

    mongodb_id = collection_users.find_one({"id": user_id})
    
    if mongodb_id:
        filter = {"id": user_id}
        new_values = {"$set": 
            {"personal_data":
                {
                    "username": message.chat.username,
                    "first_name": message.chat.first_name,
                    "last_name": message.chat.last_name,
                    "updated_time": datetime.datetime.now()
                }
            }
        }

        collection_users.update_one(filter, new_values)
    else:
        collection_users.insert_one(
            {
                "id": user_id,
                "created_time": datetime.datetime.now(),
                "personal_data":
                {
                    "username": message.chat.username,
                    "first_name": message.chat.first_name,
                    "last_name": message.chat.last_name,
                    "updated_time": datetime.datetime.now()
                }
            }
        )
    # await message.answer(f"user successfully added")
    await message.answer(texts.greetings.format(username=message.chat.full_name), reply_markup=main_menu.main_menu)
    
@router.message(F.text.lower() == "меню")
@router.message(F.text == "Вийти в меню")
@router.message(F.text == "◀️ Вийти в меню")
async def menu(msg: Message):
    await msg.answer("Головне меню ☰", reply_markup=main_menu.main_menu)

@router.callback_query(F.data == "menu")
async def menu(clbck: CallbackQuery):
    await clbck.message.answer("Головне меню ☰", reply_markup=main_menu.main_menu)