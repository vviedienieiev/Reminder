import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.states import NewEvent
from keyboards import main_menu

from database.mongo import db

router = Router()
collection_users = db["events"]

@router.callback_query(F.data == "add_new_event")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(NewEvent.event_name)
    await clbck.message.answer("Введіть назву події: ")

@router.message(NewEvent.event_name)
async def generate_text(message: Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await state.set_state(NewEvent.event_date)
    await message.answer(f"Коли ця подія станеться? (введіть у форматі рррр-мм-дд)")

@router.message(NewEvent.event_date)
async def generate_text(message: Message, state: FSMContext):
    try: 
        dt = datetime.datetime.strptime(message.text, "%Y-%m-%d")
        if dt >= datetime.datetime.today():
            await state.update_data(event_date=dt)
            await state.set_state(NewEvent.event_period)
            await message.answer(f"Як часто ця подія повторюється?")
        else:
            await message.answer("Обрана дата має бути в майбутньому", reply_markup=main_menu.iexit_kb)
    except:
        await message.answer("Невірна дата", reply_markup=main_menu.iexit_kb)
    

@router.message(NewEvent.event_period)
async def generate_text(message: Message, state: FSMContext):
    await state.update_data(event_period=message.text)
    data = await state.get_data()
    data["event_date"] = data["event_date"].strftime("%Y-%m-%d")
    await message.answer(f"{data}")

