import estimacionRadio, codecs
import netsnmp, socket,binascii,codecs
import os, sys
from datetime import datetime
import pandas as pd 
import numpy as np
import csv
import json
import pickle
import warnings
import requests

today = datetime.today()

def get_cisco_table(comuity, ip):
    """Returns [(mac_addr, ip_addr), ...]."""
    macsAP = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.4.1.4',
                            Version = 2,
                            Community = comuity ,
                            DestHost = ip)
    ipsUser = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.4.1.2',
                           Version = 2,
                           Community = comuity,
                           DestHost = ip)
    userName = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.4.1.3',
                           Version = 2,
                           Community = comuity,
                           DestHost = ip)
    ssid = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.4.1.7',
                           Version = 2,
                           Community = comuity,
                           DestHost = ip)
    vlan = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.4.1.27',
                           Version = 2,
                           Community = comuity,
                           DestHost = ip)

    nusers = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.2.2.1.15',
                           Version = 2,
                           Community = comuity,
                           DestHost = ip)

    rssi = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.6.1',
                            Version=2,
                            Community=comuity,
                            DestHost=ip)
    stationSnr = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.6.4',
                                  Version=2,
                                  Community=comuity,
                                  DestHost=ip)
    numberChanel = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.2.2.1.4',
                                    Version=2,
                                    Community=comuity,
                                    DestHost=ip)
    bytesReceived = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.6.2',
                            Version=2,
                            Community=comuity,
                            DestHost=ip)
    bytesSent = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.6.3',
                                     Version=2,
                                     Community=comuity,
                                     DestHost=ip)
    policyErrors = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.6.4',
                                 Version=2,
                                 Community=comuity,
                                 DestHost=ip)
    packetsReceived = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.6.4',
                                    Version=2,
                                    Community=comuity,
                                    DestHost=ip)
    packetsSent = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.6.4',
                                       Version=2,
                                       Community=comuity,
                                       DestHost=ip)

    RSS1= netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.2.19',
                                       Version=2,
                                       Community=comuity,
                                       DestHost=ip)  
   
    RSS2 = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.2.19.1.1',
                                       Version=2,
                                       Community=comuity,
                                       DestHost=ip) 
    RSS3 = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.2.13.1.24',
                                       Version=2,
                                       Community=comuity,
                                       DestHost=ip)   
    RSS4 = netsnmp.snmpwalk('.1.3.6.1.4.1.14179.2.1.8.1.27',
                                       Version=2,
                                       Community=comuity,
                                       DestHost=ip)                                       



    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    cantidaDate = len(macsAP)*[date_time]
    cantidaMac  = len(macsAP)*[len(macsAP)]
    cantidaIpUsa = len(ipsUser)*[len(ipsUser)]

    return zip(map(codecs.decode,[binascii.hexlify(x, ':') for x in macsAP]),map(int, cantidaMac),map(codecs.decode, ipsUser),map(int, cantidaIpUsa),map(codecs.decode, userName),map(codecs.decode, ssid),map(int, nusers),map(codecs.decode, vlan),map(int, rssi), cantidaDate,RSS1,RSS2,RSS3,RSS4)


communityName = 'Tesis'
ipAddress = '192.168.246.1'
lines= (list (get_cisco_table(communityName,ipAddress)))
lista= []
for x in lines:
    if len(x) != 0:
        d_est, d_min, d_max = estimacionRadio.estimate_distance(x[0][8])
        json = {
            "mac_ap": x[0][0],
            "ip_user_dchp": x[0][2],
            "user_name": x[0][4],
            "ssid": x[0][5],
            "vlan": x[0][7],
            "nuser_ap": x[0][6],
            "rssi": x[0][8],
            "radio_min": d_max,
            "snr": x[0][0] if len(x[0]) == 14 else "",
            "fecha_captura": x[0][9],
            "cantidad_registros": x[0][1]
        }
        lista.append(json)

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
host='44.204.82.115'
ruta='/snmp'
port='9200'



def send_data(body, host, ruta, port):
    url = "https://" + host + ":" + str(port) + str(ruta)
    r = requests.post(url, json=body, verify=False)
    return r.json()


send_data(lista, host, ruta, port)

