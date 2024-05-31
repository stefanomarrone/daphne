import requests

mongoport = 1812
mongoip = '127.0.0.1'

def addingDDM():
    mongourl = 'http://' + mongoip + ':' + str(mongoport) + '/ddmodels?identifier=' + str(1) + '&version=' + str(1)
    handler = open('modelfitted.keras', 'rb')
    files = {"file": (handler.name, handler, "multipart/form-data")}
    resp = requests.post(url=mongourl, files=files)
    return resp.json()['success']


def gettingDDM():
    mongourl = 'http://' + mongoip + ':' + str(mongoport) + '/ddmodels?identifier=' + str(1) + '&version=' + str(1)
    resp = requests.get(url=mongourl)
    handler = open('test.keras','wb')
    handler.write(resp.content)
    handler.close()
    return True


def cleaning():
    mongourl = 'http://' + mongoip + ':' + str(mongoport) + '/clean'
    resp = requests.get(url=mongourl)
    return resp.json()['success']

def addingMBM():
    mongourl = 'http://' + mongoip + ':' + str(mongoport) + '/mbmodels?identifier=' + str(1) + '&version=' + str(1)
    handler = open('example.ftml', 'r')
    files = {"file": (handler.name, handler, "multipart/form-data")}
    resp = requests.post(url=mongourl, files=files)
    return resp.json()['success']


def gettingMBM():
    mongoport = 1812
    mongourl = 'http://127.0.0.1:' + str(mongoport) + '/mbmodels?identifier=' + str(1) + '&version=' + str(1)
    resp = requests.get(url=mongourl)
    handler = open('test.ftml','w')
    handler.write(resp.json()['content'])
    handler.close()
    return resp.json()['success']


if __name__ == '__main__':
    print("Cleaning the database")
    result = cleaning()
    print(result)
    print("Adding the Model Based Model")
    result = addingMBM()
    print(result)
    print("Getting the Model Based Model")
    result = gettingMBM()
    print(result)
    print("Adding the Data Driven Model")
    result = addingDDM()
    print(result)
    print("Getting the Data Driven Model")
    result = gettingDDM()
    print(result)