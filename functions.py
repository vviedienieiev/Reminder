import datetime
from dateutil.relativedelta import relativedelta


def calculate_next_occurence(init_date: datetime.datetime, freq_month: int, incl_today: bool = False) -> datetime.date:
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    month_diff = (today.year - init_date.year) * 12 + today.month - init_date.month
    if incl_today & (today.date() == init_date.date()):
        return init_date
    elif month_diff < 0: 
        return init_date
    else:
        month_add = 0
        if ((month_diff)%freq_month == 0) & (today.day < init_date.day):
            month_add = 0
        elif ((month_diff)%freq_month == 0) & (today.day >= init_date.day) :
            month_add = freq_month
        else:
            month_add = freq_month - (month_diff)%freq_month
        return (today + relativedelta(months=month_add)).replace(day=init_date.day)