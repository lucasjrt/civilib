from datetime import date, datetime


def format_date(raw_date: date):
    return raw_date.strftime("%Y-%m-%d")


def format_datetime(raw_datetime: datetime):
    return raw_datetime.strftime("%Y-%m-%d %H:%M:%S")


def normalize_phone_number(phone_number):
    digits = "".join(filter(str.isdigit, phone_number))
    if len(digits) == 11 and digits.startswith("55"):
        return f"+{digits}"
    elif not digits.startswith("55") and len(digits) in {10, 11}:
        return f"+55{digits}"
    elif len(digits) == 13 and digits.startswith("55"):
        return f"+{digits}"
    else:
        raise ValueError("Invalid phone number format")
