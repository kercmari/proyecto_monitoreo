import json
from datetime import datetime

import requests
def send_data(body,host, ruta,port ):
    url = "http://" + host + ":" +str(port)+ "/"+str(ruta)
    r = requests.post(url, json = body, verify=False)
    return r.content
list =  ['CapFIECViejaIEEE.json', 'capFIECViejaP2.json','CapFCV.json', 'CapFICT.json','CapFCV.json', 'CapFICT.json', 'capFIMCP.json']
# Opening JSON file
lista = []
f = open(list[6])

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data["wifi-aps"]:
    json_list = {
        "mac_ap": i["macAddr"][:-1]+"0",
        "mac_wifi": i["macAddr"],
        "name": i["ssid"],
        "frequency": i["frequency"],
        "channel": i["channel"],
        "bandwidth": i["bandwidth"],
        "fecha_captura": i["firstseen"]

    }
    lista.append(json_list)

# Closing file
f.close()

host='127.0.0.1'
ruta='raspberry'
port='4000'
list_data = json.dumps(lista)
send_data(lista,host, ruta, port)
