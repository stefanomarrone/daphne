import os

import requests
import json

url = "http://127.0.0.1:4416/items/"
file_path = os.path.join('inputs', 'input.json')

with open(file_path, 'r') as file:
    data = json.load(file)


response = requests.post(url, json=data)

# Stampa la risposta del server
print(response.json())



