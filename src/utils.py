def messagemaker(image_flag, data_flag):
    responses = {
        (True, True): 'no error',
        (True, False): 'error in data retrival',
        (False, True): 'error in image retrival',
        (False, False): 'error in both retrivals'
    }
    message = responses((image_flag, data_flag))
    return message