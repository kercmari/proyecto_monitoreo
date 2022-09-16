from utils.db import db


class Ap(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    mac_ap = db.Column(db.String(100), primary_key=True)
    n_usuarios = db.Column(db.Integer)
    fecha_captura = db.Column(db.String(100))
    latitud = db.Column(db.Float(precision=32, decimal_return_scale=None))
    longitud = db.Column(db.Float(precision=32, decimal_return_scale=None))
    ap_model = db.Column(db.String(100))
    max_num_usuarios = db.Column(db.String(100))
    
