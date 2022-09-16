from utils.db import db


class Ssid(db.Model):
    mac_wifi = db.Column(db.String(100), primary_key=True)
    mac_ap = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    frecuencia = db.Column(db.Integer)
    channel = db.Column(db.Integer)
    bandwidth = db.Column(db.Integer)
    vlan = db.Column(db.String(100))
    
