def try_make_int(value: str) -> int | None:
    if value != None and value.isdigit():
        return int(value)
    else:
        return None