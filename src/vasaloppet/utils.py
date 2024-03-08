import datetime as dt

def try_make_int(value: str) -> int | None:
    if value != None and value.isdigit():
        return int(value)
    else:
        return None

def try_make_timedelta(value: str) -> dt.timedelta | None:
    try:
        datetime = dt.datetime.strptime(value, "%H:%M:%S")
        return datetime - dt.datetime(1900, 1, 1)
    except:
        return None