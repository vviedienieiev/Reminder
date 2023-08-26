import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.states import NewEvent
from keyboards import main_menu, new_event, general
import texts

from database.mongo import db

router = Router()
collection_events = db["events"]

@router.callback_query(F.data == "add_new_event")
async def new_event_callback(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    await state.set_state(NewEvent.event_name)
    await clbck.message.answer("Введіть назву події: ")

@router.message(NewEvent.event_name)
async def get_event_name(message: Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await state.set_state(NewEvent.event_recuring_type)
    await message.answer(f"Це одноразова чи повторювана подія", reply_markup=new_event.event_frequency_type)

@router.callback_query(NewEvent.event_recuring_type, F.data == "one_time_event")
async def handle_one_time_events(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    await state.update_data(event_recuring_type="one_time")
    await state.set_state(NewEvent.event_date)
    await clbck.message.answer(f"Коли ця подія відбудеться? (введіть у форматі рррр-мм-дд)")

@router.callback_query(NewEvent.event_recuring_type, F.data == "recurring_event")
async def handle_recurring_events(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    await state.update_data(event_recuring_type="recurring")
    await state.set_state(NewEvent.event_date)
    await clbck.message.answer(f"Коли ця подія в перший раз відбулася? (введіть у форматі рррр-мм-дд)")

@router.message(NewEvent.event_recuring_type)
async def handle_another_choices(message: Message, state: FSMContext) -> None:   
    await state.clear()
    await message.answer(f"Такого варіанту немає", reply_markup=main_menu.iexit_kb)

@router.message(NewEvent.event_date)
async def get_event_date(message: Message, state: FSMContext):
    data = await state.get_data()
    try: 
        dt = datetime.datetime.strptime(message.text, "%Y-%m-%d")
        if (data["event_recuring_type"] == "one_time") & (dt <= datetime.datetime.today()):
            await message.answer(f"Дата одноразової події має бути тільки в майбутньому", reply_markup=main_menu.iexit_kb)
        elif data["event_recuring_type"] == "one_time":
            await state.update_data(event_date=dt)
            await state.update_data(event_freq=None)
            await state.set_state(NewEvent.upload_event)
            await message.answer(texts.check_new_event.format(event_name = data["event_name"], 
                                                              event_recurring = "Одноразова подія", 
                                                              event_date = dt.strftime("%Y-%m-%d"), 
                                                              event_freq = "Не повторюється"), reply_markup=general.yes_no)
        elif data["event_recuring_type"] == "recurring":
            await state.update_data(event_date=dt)
            await state.set_state(NewEvent.event_freq)
            await message.answer(f"Як часто ця подія повторюється?", reply_markup=new_event.event_frequency_options)
    except:
        await message.answer("Невірна дата", reply_markup=main_menu.iexit_kb)
    
@router.callback_query(NewEvent.event_freq)
async def check_correct_event(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    await state.update_data(event_freq=clbck.data)
    data = await state.get_data()
    freq = None
    if data["event_freq"] == "1 month":
        freq = "Кожен місяць"
    elif data["event_freq"] == "3 months":
        freq = "Кожні 3 місяці"
    elif data["event_freq"] == "6 months":
        freq = "Кожні 6 місяців"
    elif data["event_freq"] == "12 months":
        freq = "Кожен рік" 
    await state.set_state(NewEvent.upload_event)
    await clbck.message.answer(texts.check_new_event.format(event_name = data["event_name"], 
                                                              event_recurring = "Повторювана подія", 
                                                              event_date = data["event_date"].strftime("%Y-%m-%d"), 
                                                              event_freq = freq), reply_markup=general.yes_no)

@router.callback_query(NewEvent.upload_event, F.data == "yes")
async def insert_event(clbck: CallbackQuery, state: FSMContext): 
    await clbck.answer()
    data = await state.get_data()
    data["user_id"] = clbck.message.chat.id
    data["reminders"] = [-7, -2, 0]
    event_id_from_mongo = collection_events.find_one({"event_name": data["event_name"],
                                                     "event_date": data["event_date"]})
    if event_id_from_mongo:
        await clbck.message.answer("Вибачте, ви вже планували цю подію. Змініть назву або дату, будь ласка.", reply_markup=main_menu.iexit_kb)
    else:
        try:
            event_id = collection_events.insert_one(data).inserted_id
            await clbck.message.answer(f"Я запам'ятав цю подію. Нагадю про неї за 7,2 дні до неї, а також в день події.", reply_markup=main_menu.iexit_kb)
        except:
            await clbck.message.answer("Трапилось якесь лихо і я не зміг запам'ятати цю подію. Спробуйте ще раз.", reply_markup=main_menu.iexit_kb)
        finally:
            await state.clear()

@router.callback_query(NewEvent.upload_event, F.data == "no")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer() 
    await state.clear()
    await clbck.message.answer("Шкода, що я неправильно запам'ятав дані. Введіть їх ще раз, будь ласка.", reply_markup=main_menu.iexit_kb)