greetings = """Привіт {username}👋
Я бот, що покликаний врятувати тебе від великої кількості неприємностей!
Ти забуваєш про важливі події та про дні народження своїх близьких?
Я візьму цю работу на себе і нагадую заздалегіть, щоб ти нічого не забув :)
Почни працювати зі мною, використовуючи меню нижче 🔽"""

main_menu = "Головне меню ☰"

check_new_event = """
Дякую, за цю інформацію. Перевір, будь ласка, чи я все правильно запам'ятав?
Назва події: {event_name};
Повторюваність події: {event_recurring}; 
Дата події: {event_date};
Частота події: {event_freq}.
"""

no_available_events = "Поки що у вас немає жодної події."

new_event_name  = "Введіть назву події: "

new_event_frequency_type = "Це одноразова чи повторювана подія?"

new_event_one_time_date = "Коли ця подія відбудеться? (введіть у форматі рррр-мм-дд)"

new_event_recurring_date = "Коли ця подія в перший раз відбулася? (введіть у форматі рррр-мм-дд)"

new_event_other_date = "Такого варіанту немає."

new_event_one_time_incorrect_date = "Дата одноразової події має бути тільки в майбутньому"

new_event_incorrect_date = "Невірна дата"

new_event_ask_freq_value = "Як часто ця подія повторюється?"

new_event_already_existed = "Вибачте, ви вже планували цю подію. Змініть назву або дату, будь ласка."

new_event_added_succesfully = "Я запам'ятав цю подію. Нагадю про неї за тиждень, за 2 дні до неї, а також в день події."

new_event_user_reject = "Шкода, що я неправильно запам'ятав дані. Введіть їх ще раз, будь ласка."

new_event_undefined_error = "Трапилось якесь лихо і я не зміг запам'ятати цю подію. Спробуйте ще раз."

change_events_available_options = "Що ви хочете зробити з подією?"

change_event_select_incorrect_number = "Ви обрали неіснуючий номер."

change_event_add_reminder_value = "Введіть число від 0 до 28, щоб додати нагадування за стільки днів."

change_event_incorrect_days_value = "Неправильна кількість днів"

change_event_existing_days_value = "Нагадувалка за цей період вже існує"

change_event_reminder_added_succesfully = "Нагадування {days_value} успішно додане"

change_event_delete_approve = "Ви впевнені, що хочете видалити подію {event_name}?"

change_event_delete_success = "Подія успішно видалена!"