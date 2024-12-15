from src.catalog.coordinateextractor import CoordinateExtractor

def messagemaker(image_flag, data_flag):
    responses = {
        (True, True): 'no error',
        (True, False): 'error in data retrival',
        (False, True): 'error in image retrival',
        (False, False): 'error in both retrivals'
    }
    message = responses[(image_flag, data_flag)]
    return message

def get_content(file_name):
    handle = open(file_name, 'r')
    retval = handle.readlines()
    retval = ''.join(retval)
    handle.close()
    return retval

def define_coordinates(lat, lon, country_name):
    if lat != '' and lon != '':
        return lat, lon
    elif country_name is not None:
        coordinates = CoordinateExtractor().get_coordinates(country_name)
        return list(coordinates.values())
