from datetime import datetime


def convert_datetime_to_str(dt) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")
