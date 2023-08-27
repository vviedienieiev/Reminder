
import datetime
from dateutil.relativedelta import relativedelta

from database.mongo import db

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.states import NewEvent
from keyboards import main_menu
import texts

router = Router()
collection_events = db["events"]

def get_one_time_events(user_id):
    one_time_events = list(collection_events.find({"user_id": user_id, 
                                 "event_recuring_type": "one_time", 
                                 "event_date": {"$gte": datetime.datetime.today()}},
                                 {"event_name": 1, "event_date": 1}))
    one_time_events = [[val['event_name'], val['event_date'].date()] for val in one_time_events]
    return one_time_events

def get_recurring_events(user_id):
    recurring_events = list(collection_events.find({"user_id": user_id, 
                                 "event_recuring_type": "recurring"},
                                 {"event_name": 1, "event_date": 1, "event_freq": 1}))
    ls = []
    for val in recurring_events:
        event_name = val["event_name"]
        next_event_date = None

        today = datetime.datetime.today().date()
        init_date = val["event_date"].date()
        freq = int(val["event_freq"].split(" ")[0])
        month_diff = (today.year - init_date.year) * 12 + today.month - init_date.month
        init_day = init_date.day
        if month_diff < 0: 
            next_event_date = init_date
        else:
            month_add = 0
            if ((month_diff)%freq == 0) & (today.day < init_date.day):
                month_add = 0
            elif ((month_diff)%freq == 0) & (today.day >= init_date.day) :
                month_add = freq
            else:
                month_add = freq - (month_diff)%freq
            
            next_event_date = (today + relativedelta(months=month_add)).replace(day=init_day)
        ls.append([event_name, next_event_date])
    return ls
    

@router.callback_query(F.data == "show_events")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer()
    user_id = clbck.message.chat.id
    one_time_events = get_one_time_events(user_id)
    recurring_events = get_recurring_events(user_id)

    all_events = one_time_events+recurring_events
    sorted_events = sorted(all_events, key=lambda x: x[1])
    text = ""
    for num, val in enumerate(sorted_events):
        text += f"{num+1} - {val[0]} - {val[1].strftime('%Y-%m-%d')}\n"
    if len(text) == 0:
        await clbck.message.answer(f"{texts.no_available_events}", reply_markup=main_menu.iexit_kb)
    else:
        await clbck.message.answer(f"{text}", reply_markup=main_menu.iexit_kb)