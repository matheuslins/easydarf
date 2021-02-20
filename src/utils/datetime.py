import pytz
from datetime import datetime


def now_datetime():
    now = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    now_str = now.isoformat()
    return now, now_str
