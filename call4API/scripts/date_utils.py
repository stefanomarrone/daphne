from datetime import datetime

def date_to_date_hour(date):
    data_ora = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    data_part = data_ora.date().strftime("%Y-%m-%d")
    hour_part = data_ora.time().strftime("%H")
    return data_part, hour_part


def is_date_format_without_hour_originale(date_string):
    format = '%Y-%m-%d %H:%M:%S'
    if bool(datetime.strptime(date_string, format)):
        return False
    else:
        return True


def is_date_format_without_hour(date_string):
    format = '%Y-%m-%d %H:%M:%S'
    try:
        datetime.strptime(date_string, format)
        return False  # Se il parsing va a buon fine, restituisce False
    except ValueError:
        return True


def change_date_format(date_string):
    if is_date_format_without_hour(date_string):
        str_d = date_string
        str_h = '-'
    else:
        str_d, str_h = date_to_date_hour(date_string)
    return str_d, str_h

def date_to_timestamp(date_str):
    # Convert the date string to a datetime object
    date_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    # Get the Unix timestamp from the datetime object
    timestamp = int(date_object.timestamp())

    return timestamp


def timestamp_to_date(timestamp):
    # Convert the Unix timestamp to a datetime object
    date_object = datetime.fromtimestamp(timestamp)

    # Format the datetime object as a date string
    date_str = date_object.strftime('%Y-%m-%d %H:%M:%S')

    return date_str

def date_to_iso(date_str):
    if not date_str:
        return None
    if "T" in date_str and len(date_str.split("T")) == 2:
        return date_str
    possible_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
    ]
    for fmt in possible_formats:
        try:
            data_obj = datetime.strptime(date_str, fmt)
            return data_obj.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue

def _fmt_date(s):
    try:
        # taglia il fuso e rendi leggibile
        return date_to_iso(s.replace("Z","+00:00")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return s or "-"


def from_iso_format(s):
    dt = datetime.fromisoformat(s)
    formatted = dt.strftime("%Y-%m-%d %H:%M")
    return formatted