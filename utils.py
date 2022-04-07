from datetime import datetime


def compare_str_date_to_now(str_date):
    datetime_object = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    return datetime_object < datetime.now()
