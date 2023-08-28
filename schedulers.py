import datetime
from aiogram import Bot
from dateutil.relativedelta import relativedelta


from functions import calculate_next_occurence
from database.mongo import db

collection_events = db["events"]

async def bot_is_working(bot:Bot):
    await bot.send_message(text="Бот ще працює!", chat_id=420205733)

async def notify_users(bot: Bot):
    month_ahead =  (datetime.datetime.today() + relativedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    filter = {"next_date": {"$lt": month_ahead}, "status": "active"}
    events = collection_events.find(filter)
    for event in events:
        user_id = event["user_id"]
        event_name = event["event_name"]
        event_date = event["event_date"]
        next_date = event["next_date"]
        for reminder in event["reminders"]:
            reminder_date = next_date + relativedelta(days=reminder)
            if today == reminder_date:
                print(f"Нагадую про {event_name}, що відбудеться {event_date}!")
                await bot.send_message(text=f"Нагадую про {event_name}, що відбудеться {next_date.strftime('%Y-%m-%d')}!", chat_id=user_id)

async def update_event_status_and_date():
    yesterday = (datetime.datetime.today()+ relativedelta(days=-1)).replace(hour=0, minute=0, second=0, microsecond=0)  
    filter = {"next_date": yesterday, "status": "active"}
    events = collection_events.find(filter)
    for event in events:
        if event["event_recurring_type"] == "one_time":
            filter = {"_id": event["_id"]}
            new_value = {"status": "inactive", "next_date": None}
        else:
            next_date = calculate_next_occurence(event["event_date"], int(event["event_freq"]))
            filter = {"_id": event["_id"]}
            new_value = {"next_date": next_date}
        collection_events.update_one(filter, {"$set": new_value})


