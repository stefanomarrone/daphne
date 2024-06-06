import requests
class MongoWriter:
    def __init__(self, iip, pport):
        self.ip = iip
        self.port = pport

    def write(self, name, image):
        mongourl = 'http://' + self.ip + ':' + str(self.port) + '/matforpat?configuration_name=' + name
        handler = open(image, 'rb')
        files = {"file": (handler.name, handler, "multipart/form-data")}
        resp = requests.post(url=mongourl, files=files)
        #todo improve the return message
        return resp.json()['success']
