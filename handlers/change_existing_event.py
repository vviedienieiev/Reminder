from database.mongo import db

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.states import ChangeEvent
from keyboards import main_menu, change_event, general
import texts

router = Router()
collection_events = db["events"]

def correct_day_word(x: int):
    if x == 0:
        return "В день події;"
    elif (x >= 2) & (x <= 4):
        return f"За {x} дні до події"
    elif (x >= 5) & (x <= 20):
        return f"За {x} днів до події"
    elif x%10 in [0,5,6,7,8,9]:
        return f"За {x} днів до події"
    elif x%10 == 1:
        return f"За {x} дні до події"
    elif (x%10 >= 2) & (x%10 <= 4):
        return f"За {x} дні до події"
    
@router.callback_query(F.data == "change_existing_event")
async def show_list_of_events(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    await state.set_state(ChangeEvent.events_list)
    user_id = clbck.message.chat.id
    events = list(collection_events.find({"user_id": user_id}))
    if len(events) == 0:
        await state.clear()
        await clbck.message.answer(f"{texts.no_available_events}", reply_markup=main_menu.iexit_kb)
    else:
        sorted_events = sorted(events, key=lambda x: x["event_date"])
        await state.update_data(events_list = sorted_events)
        text = "Виберіть подію з списку нижче: \n\n"
        for num, val in enumerate(sorted_events):
            text += f"{num+1} - {val['event_name']} - {val['event_date'].strftime('%Y-%m-%d')}\n"
        await clbck.message.answer(text, reply_markup=main_menu.iexit_kb)
        
    

@router.message(ChangeEvent.events_list)
async def show_edit_options(message: Message, state: FSMContext):
    await state.set_state(ChangeEvent.selected_event)
    try:
        data = await state.get_data()
        choice = int(message.text)-1
        # await message.answer(f"{choice} \n {data}")
        selected_event = data["events_list"][choice]
        await state.update_data(selected_event=selected_event)
        await message.answer(f"{texts.change_events_available_options}", reply_markup=change_event.change_options)
    except:
        await state.clear()
        await message.answer(f"{texts.change_event_select_incorrect_number}", reply_markup=main_menu.iexit_kb)

@router.callback_query(ChangeEvent.selected_event, F.data == "add_reminder")
async def show_reminders(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    await state.set_state(ChangeEvent.get_current_reminders)
    data = await state.get_data()
    selected_event = data["selected_event"]
    reminders = selected_event["reminders"]
    reminders_sorted = sorted([abs(x) for x in reminders])  
    text = "На цю подію вже існують наступні нагадувалки: \n\n"
    for num, val in enumerate(reminders_sorted):
        text += f"{num+1} - {correct_day_word(val)};\n"
    await clbck.message.answer(f"{text}")
    await clbck.message.answer(f"{texts.change_event_add_reminder_value}", reply_markup=main_menu.iexit_kb)    

@router.message(ChangeEvent.get_current_reminders)
async def add_reminders(message: Message, state: FSMContext):
    try:
        await state.set_state(ChangeEvent.add_new_reminder)
        data = await state.get_data()
        reminders = data["selected_event"]["reminders"]
        choice = int(message.text)
        if (choice < 0) | (choice > 28):
            await message.answer(f"{texts.change_event_incorrect_days_value}", reply_markup=main_menu.iexit_kb)
        elif -choice in reminders:
            await message.answer(f"{texts.change_event_existing_days_value}", reply_markup=main_menu.iexit_kb)
        else:
            reminders.append(-choice)
            data["selected_event"]["reminders"] = sorted(reminders)
            filter = {"_id":  data["selected_event"]["_id"]}
            new_value = {"$set": {"reminders": data["selected_event"]["reminders"]}}
            collection_events.update_one(filter, new_value)
            await message.answer(f"{texts.change_event_reminder_added_succesfully.format(days_value=correct_day_word(choice).lower())}", reply_markup=main_menu.iexit_kb)
    except:
         await message.answer(f"{texts.change_event_incorrect_days_value}", reply_markup=main_menu.iexit_kb)
    finally:
        await state.clear()


@router.callback_query(ChangeEvent.selected_event, F.data == "delete event")
async def show_reminders(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    await state.set_state(ChangeEvent.delete_approve)
    data = await state.get_data()
    selected_event = data["selected_event"]
    await clbck.message.answer(f"{texts.change_event_delete_approve.format(selected_event['event_name'])}", reply_markup=general.yes_no)

@router.callback_query(ChangeEvent.delete_approve, F.data == "yes")
async def show_reminders(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    await state.set_state(ChangeEvent.delete_approve)
    data = await state.get_data()
    selected_event = data["selected_event"]
    collection_events.delete_one({"_id": selected_event["_id"]})
    await state.clear()
    await clbck.message.answer(f"{texts.change_event_delete_success}", reply_markup=main_menu.iexit_kb)