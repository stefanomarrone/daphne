from datetime import datetime

from dateutil.parser import parser


def date_to_date_hour(date):
    data_ora = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    data_part = data_ora.date()
    hour_part = data_ora.time().strftime("%H")
    return data_part, hour_part


def is_date_format_without_hour(date_string):
    format = '%Y-%m-%d %H:%M:%S'
    if bool(datetime.strptime(date_string, format)):
        return False
    else:
        return True


def change_date_format(date_string):
    if is_date_format_without_hour(date_string):
        str_d = date_string
        str_h = '-'
    else:
        str_d, str_h = date_to_date_hour(date_string)
    return str_d, str_h


# function to define a rectangle given lat-lon and region_size
# xMin, yMin, xMax, yMax
def get_region_string(coords, region_size):
    left = coords[0] - region_size / 2
    right = coords[0] + region_size / 2
    top = coords[1] + region_size / 2
    bottom = coords[1] - region_size / 2
    return [left, bottom, right, top]
