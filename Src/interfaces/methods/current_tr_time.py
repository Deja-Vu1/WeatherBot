import datetime
from datetime import datetime
import pytz
from pytz import timezone

def get():
    utc_now = datetime.utcnow()
    utc = pytz.timezone('UTC')
    aware_date = utc.localize(utc_now)
    turkey = timezone('Europe/Istanbul')
    now_turkey = aware_date.astimezone(turkey)
    return now_turkey