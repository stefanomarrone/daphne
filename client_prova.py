import os
import requests
import json

mongoport = 1812
mongoip = '127.0.0.1'

file_path = os.path.join('inputs', 'input.json')

# with open(file_path, 'r') as file:
#     data = json.load(file)
#
#
# x = data['configurations']
# y = x[0]['name']


image_path = os.path.join('output', 'Untitled.jpeg')
image_path2 = os.path.join('output2', 'Untitled.jpeg')


def addingDDM():
    mongourl = 'http://' + mongoip + ':' + str(mongoport) + '/matforpat?identifier=' + 'configuration.ini'
    handler = open("./output/Untitled.jpeg", 'rb')
    files = {"file":( handler.name, handler, "multipart/form-data")}
    resp = requests.post(url=mongourl,files=files)

    return resp.json()['success']



if __name__ == '__main__':

    print("Adding the Data Driven Model")
    result = addingDDM()
    print(result)
