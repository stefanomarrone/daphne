#DA FARE: automatizzare i nomi dei file ini

import configparser
import json
import run #gli passo tutta la cartella per il file ini
def conf ():
    #in questa funzione fare la conversione del file ini in file json

    config_object = configparser.ConfigParser()
    file = open("run/configuration.ini", "r")
    config_object.read_file(file)
    output_dict = dict()
    sections = config_object.sections()
    for section in sections:
        items = config_object.items(section)
        output_dict[section] = dict(items)

    json_file = open("configuration.json", "w")
    json.dump(output_dict, json_file)
    json_file.close()
    file.close()


    return "configuration.json"     #ritorna il nome del file json che nel main, con il richiamo
                                    #della funzione mi apre questo file e lo legge
