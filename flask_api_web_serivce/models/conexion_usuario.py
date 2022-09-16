from utils.db import db


class ConexionUsuario(db.Model):
    ip_dinamica = db.Column(db.String(100), primary_key=True)
    mac_ap = db.Column(db.String(100))
    ssid = db.Column(db.String(100))
    snr = db.Column(db.String(100))
    rssi = db.Column(db.String(100))
    latencia = db.Column(db.Float(precision=32, decimal_return_scale=None))
    paquetes_perdidos = db.Column(db.Integer)
    jitter = db.Column(db.Float(precision=32, decimal_return_scale=None))
    paquetes_size = db.Column(db.Float(precision=32, decimal_return_scale=None))
    protocolo = db.Column(db.String(100))
    # vlan = db.Column(db.String(100))
    radio_min = db.Column(db.Float(precision=32, decimal_return_scale=None))
    user_name = db.Column(db.String(100))
    trafico_total = db.Column(db.Float(precision=32, decimal_return_scale=None))
    fecha_captura = db.Column(db.String(100))
    
