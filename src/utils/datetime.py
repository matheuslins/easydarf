import pytz
from datetime import datetime


def now_datetime():
    now = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    now_str = now.isoformat()
    return now, now_str


def convert_str_datetime(date: str):
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    date_str = date_time_obj.isoformat()
    return date_str
