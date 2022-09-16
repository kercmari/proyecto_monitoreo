from cmath import pi
from flask import Flask
from routes.devices import devices
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, not_, func
from config import DATABASE_CONNECTION_URI
from models.ssid import Ssid
from models.ap import Ap
from models.conexion_usuario import ConexionUsuario
from utils.db import db as _db
import time
import requests
app = Flask(__name__)

# settings
app.secret_key = 'mysecret'
print(DATABASE_CONNECTION_URI)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# no cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

SQLAlchemy(app)


app.register_blueprint(devices)
db:SQLAlchemy = _db
def serialize(row):
    return {
    'mac_wifi': row.mac_wifi,
    'ssid': row.nombre,
    'bandwidth': row.bandwidth,
    'frecuencia': row.frecuencia,  
    'channel': row.channel,
    }
def serialize_mapa(row):
    return {
    'rssi': row.rssi,
    'radio_min': row.radio_min
    }
def send_data(body,host, ruta,port ):
    url = "http://" + host + ":" +str(port)+ "/"+str(ruta)
    r = requests.put(url, json = body, verify=False)
    return (r.content)
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name)) if  column.name!= 'n_usuarios' else (int(getattr(row, column.name)) if isinstance(getattr(row, column.name),int) else 0)
      
        if (column.name=='mac_ap'):
            
            d_qos= {}
            d_latencia= {}
            d_jitter= {}
            d_packets_loss= {}
            
            mac_id = str(getattr(row, column.name))
            result_ssid = [serialize(u) for u in Ssid.query.filter_by(mac_ap=mac_id)]
            result_mapa = [serialize_mapa(u) for u in ConexionUsuario.query.filter_by(mac_ap=mac_id).limit(5).all()]
            #Latencia
            count_filter_latencia_R= ConexionUsuario.query.filter_by(mac_ap=mac_id).count()
            count_filter_latencia_R2= ConexionUsuario.query.filter_by(mac_ap=mac_id,).filter(ConexionUsuario.latencia.between( 0,100) ).count()
            count_filter_latencia_R3= ConexionUsuario.query.filter_by(mac_ap=mac_id,).filter(ConexionUsuario.latencia.between( 101,150) ).count()
            count_filter_latencia_R4= ConexionUsuario.query.filter_by(mac_ap=mac_id,).filter(ConexionUsuario.latencia> 150 ).count()
            porcentaje_r1 = count_filter_latencia_R2/count_filter_latencia_R if count_filter_latencia_R!= 0 else 0
            porcentaje_r2 = count_filter_latencia_R3/count_filter_latencia_R if count_filter_latencia_R!= 0 else  0
            porcentaje_r3 = count_filter_latencia_R4/count_filter_latencia_R if count_filter_latencia_R!= 0 else  0
            d_latencia["0_100"] = round(porcentaje_r1*100,2)
            d_latencia["101_150"] = round(porcentaje_r2*100,2)
            d_latencia["150_250"] = round(porcentaje_r3*100,2)
            #Jitter
            count_filter_jitter_R2= ConexionUsuario.query.filter_by(mac_ap=mac_id,).filter(ConexionUsuario.jitter.between( 0,30) ).count()
            count_filter_jitter_R3= ConexionUsuario.query.filter_by(mac_ap=mac_id,).filter(ConexionUsuario.jitter.between( 31,50) ).count()
            count_filter_jitter_R4= ConexionUsuario.query.filter_by(mac_ap=mac_id,).filter(ConexionUsuario.jitter > 51 ).count()
            porcentaje_j1 = count_filter_jitter_R2/count_filter_latencia_R if count_filter_latencia_R!= 0 else 0
            porcentaje_j2 = count_filter_jitter_R3/count_filter_latencia_R if count_filter_latencia_R!= 0 else  0
            porcentaje_j3 = count_filter_jitter_R4/count_filter_latencia_R if count_filter_latencia_R!= 0 else  0
            d_jitter["0_30"] = round(porcentaje_j1*100,2)
            d_jitter["31_50"] = round(porcentaje_j2*100,2)
            d_jitter["51_90"] = round(porcentaje_j3*100,2)
       
            #Paquetes perdidos
            # count_filter_pk_R2= ConexionUsuario.query.filter_by(mac_ap=mac_id).filter(ConexionUsuario.jitter.between( 0,3) ).count()
            # count_filter_pk_R3= ConexionUsuario.query.filter_by(mac_ap=mac_id).filter(ConexionUsuario.jitter.between( 3,6) ).count()
            # count_filter_pk_R4= ConexionUsuario.query.filter_by(mac_ap=mac_id).filter(ConexionUsuario.jitter > 6 ).count()
            # porcentaje_pk1 = count_filter_pk_R2/count_filter_latencia_R if count_filter_latencia_R!= 0 else 0
            # porcentaje_pk2 = count_filter_pk_R3/count_filter_latencia_R if count_filter_latencia_R!= 0 else  0
            # porcentaje_pk3 = count_filter_pk_R4/count_filter_latencia_R if count_filter_latencia_R!= 0 else  0
            # d_packets_loss["0_3"] = round(porcentaje_pk1*100,2)
            # d_packets_loss["3_6"] = round(porcentaje_pk2*100,2)
            # d_packets_loss["6_10"] = round(porcentaje_pk3*100,2)
       

            total_traffic= db.session.query(func.sum(ConexionUsuario.paquetes_size)).filter_by(mac_ap=mac_id).group_by(ConexionUsuario.mac_ap).all()
            rssi_aveg= db.session.query(func.avg(ConexionUsuario.rssi)).filter_by(mac_ap=mac_id).group_by(ConexionUsuario.mac_ap).all()
            protocolo= db.session.query(ConexionUsuario.protocolo).filter_by(mac_ap=mac_id).first()
          
 
            #Grabar datos
            d_qos["latencia"] = d_latencia
            d_qos["jitter"] = d_jitter
            d_qos["protocolo"] = protocolo[0] if (protocolo) =='None' else "-"
            d_qos["trafico_total_tcp"] = total_traffic[0][0] if len(total_traffic)>=1 else 0
            d['rssi'] = rssi_aveg[0][0] if len(rssi_aveg)>=1 else 0
            d['ssid'] = result_ssid
            d['mapa_heat'] = result_mapa
            d['qos_parameters'] = d_qos
           
           
            host='44.204.82.115'
            ruta='aps/_doc/'+mac_id
            port='9200'
            #print(d)
        print(send_data(d,host, ruta, port))
        #print(d)

@app.cli.command()
def scheduled():
    """Run scheduled job."""
    print('Creando Modelo Elastic...')
    time.sleep(5)
    for row in Ap.query.all():
        row2dict(row)
    #print('Users:', str(Ap.query.all()))
    print('Done!')