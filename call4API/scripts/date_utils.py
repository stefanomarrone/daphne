import datetime


def date_to_timestamp(date_str):
    # Convert the date string to a datetime object
    date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    # Get the Unix timestamp from the datetime object
    timestamp = int(date_object.timestamp())

    return timestamp


def timestamp_to_date(timestamp):
    # Convert the Unix timestamp to a datetime object
    date_object = datetime.datetime.fromtimestamp(timestamp)

    # Format the datetime object as a date string
    date_str = date_object.strftime('%Y-%m-%d %H:%M:%S')

    return date_str


