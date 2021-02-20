import pytz
from datetime import datetime


def now_datetime():
    now = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    now_string = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return now, now_string
