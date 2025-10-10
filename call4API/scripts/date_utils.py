from datetime import datetime


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