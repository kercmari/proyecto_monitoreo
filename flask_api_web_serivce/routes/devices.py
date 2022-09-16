from email import utils
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.ssid import Ssid
from models.ap import Ap
from models.conexion_usuario import ConexionUsuario
from flask_sqlalchemy import SQLAlchemy
from utils.db import db as _db
import json

db:SQLAlchemy = _db

devices = Blueprint("devices", __name__)


@devices.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        a = json.loads(request.data).get('macAddr')
        if a:
            return a
        return 'nada'
    return 'hello world'

@devices.route('/raspberry', methods=['POST'])
def raspberry():
    data =( json.loads(request.data))
    for value in data:
        mac_ap = value.get('mac_ap')
        mac_wifi = value.get('mac_wifi')
        name = value.get('name')
        frequency = value.get('frequency')
        channel = value.get('channel')
        bandwidth = value.get('bandwidth')
        fecha_captura = value.get('fecha_captura')
        # ap
        new_ap = getAP(mac_ap)
        new_ap.fecha_captura = fecha_captura
        # ssid
        new_ssid = getSSID(mac_wifi)
        new_ssid.mac_ap = mac_ap
        new_ssid.nombre = name
        new_ssid.frecuencia = frequency
        new_ssid.channel = channel
        new_ssid.bandwidth = bandwidth
        db.session.commit()
    return 'success'

@devices.route('/snmp', methods=['POST'])
def snmp():
    data =(json.loads(request.data))
    
    for value in  data:
        mac_ap = value.get("mac_ap")
        ip_user_dchp = value.get('ip_user_dchp')
        user_name = value.get('user_name')
        ssid = value.get('ssid')
        vlan = value.get('vlan')
        nuser_ap = value.get('nuser_ap') # en ap
        rssi = value.get('rssi')
        radio_min = value.get('radio_min')
        snr = value.get('snr')
        fecha_captura = value.get('fecha_captura')
        # cantidad_registros = value.get('cantidad_registros')
        # todo esto va en conexion usuario
        # ap
        new_ap = getAP(mac_ap)
        new_ap.fecha_captura = fecha_captura
        new_ap.n_usuarios = nuser_ap
        # ssid
        new_ssid: Ssid = Ssid.query.filter_by(mac_ap=mac_ap).first()
        if new_ssid:
            new_ssid.vlan = vlan
        # conexion usuario
        new_conexion_usuario = getConexionUsuario(ip_user_dchp)
        new_conexion_usuario.mac_ap = mac_ap
        new_conexion_usuario.fecha_captura = fecha_captura
        new_conexion_usuario.ssid = ssid
        new_conexion_usuario.user_name = user_name
        # new_conexion_usuario.vlan = vlan
        new_conexion_usuario.rssi = rssi
        new_conexion_usuario.radio_min = radio_min
        new_conexion_usuario.snr = snr
        db.session.commit()
    return 'success'

@devices.route('/wireshark', methods=['POST'])
def wireshark():
    data = json.loads(request.data)
    for value in data:
        ip_user_dchp = value.get('ip_user_dchp') # conexion_usuario
        latencia = value.get('latencia')
        jitter = value.get('jitter')
        paquetes_size = value.get('paquetes_size')
        protocolo = value.get('protocolo')
        #paquetes_perdidos = value.get('paquetes_perdidos')
        #trafico_total = value.get('trafico_total')
        fecha_captura = value.get('fecha_captura')
        # en conexion de usuario
        # ap
        conexion_usuario = getConexionUsuario(ip_user_dchp)
        conexion_usuario.latencia = latencia
        conexion_usuario.jitter = jitter
        conexion_usuario.paquetes_size = paquetes_size
        conexion_usuario.protocolo = protocolo
        conexion_usuario.fecha_captura = fecha_captura
        db.session.commit()
    return 'success'


def getAP(mac_ap) -> Ap:
    ap = Ap.query.get(mac_ap)
    if ap:
        return ap
    else:
        new_ap = Ap()
        new_ap.mac_ap = mac_ap
        db.session.add(new_ap)
        db.session.commit()
        return Ap.query.get(mac_ap)

def getSSID(mac_wifi) -> Ssid:
    ssid = Ssid.query.get(mac_wifi)
    if ssid:
        return ssid
    else:
        new = Ssid()
        new.mac_wifi = mac_wifi
        db.session.add(new)
        db.session.commit()
        return Ssid.query.get(mac_wifi)

def getConexionUsuario(ip_user_dchp) -> ConexionUsuario:
    new = ConexionUsuario.query.get(ip_user_dchp)
    if new:
        return new
    else:
        new = ConexionUsuario()
        new.ip_dinamica = ip_user_dchp
        db.session.add(new)
        db.session.commit()
        return ConexionUsuario.query.get(ip_user_dchp)