import csv
lista = []
from datetime import datetime
import requests
import json
with open('QoS-Analizado.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    for x in reader:

             json_data = {

                 "ip_user_dchp": x['Source'],
                 "latencia": (float(x['Delay'] )if x['Delay'] != '' else 0)*1000,
                 "jitter": (float(x['Jitter'])if x['Jitter'] != '' else 0)*1000,
                 "paquetes_size": float(x['Length']),
                 "protocolo":  x['Protocol'],
                 "fecha_captura": date_time,
             }
             lista.append(json_data)
def send_data(body,host, ruta,port ):
    url = "http://" + host + ":" +str(port)+ "/"+str(ruta)
    r = requests.post(url, json = body, verify=False)
    return r

#host='44.204.82.115'
host='127.0.0.1'
ruta='wireshark'
port='4000'
list_data = json.dumps(lista)
#print(list_data)
send_data(lista,host, ruta, port)
