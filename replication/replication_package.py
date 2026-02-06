import os
import sys
import time
import requests
import json

if __name__ == '__main__':
    time.sleep(5)
    daphne_host = sys.argv[1]
    daphne_port = int(sys.argv[2])
    input_file_name = sys.argv[3]
    url = f'http://{daphne_host}:{daphne_port}/execute'
    file_path = os.path.join('replication', input_file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    response = requests.post(url, json=data)
    print(response.json())



