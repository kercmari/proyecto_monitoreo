<h1 align="center"> Sistema Unificado de Monitoreo de Calidad de Servicio y Calidad de Experiencia en Redes Wi-Fi </h1>

<h3> Miembros </h3>

<div align="center">
 <table>
  <tr>
    <td align="center"><a href="https://github.com/kercmari"><img src="https://avatars.githubusercontent.com/u/62037369?v=4" width="100px;" alt=""/><br /><sub><b>Kerly Cervantes</b></sub></a><br/><a>🌹</a></td>
<td align="center"><a href="https://github.com/YiamRodriguezDelgado"><img src="https://avatars.githubusercontent.com/u/44529630?v=4" width="100px;" alt=""/><br /><sub><b>Yiam Rodriguez</b></sub></a><br/><a>😎</a></td>
</table> 
</div>
 
  
<h3> Descripción del Proyecto </h3>
<p css="text-align: justify;">El proyecto consta de tres agentes de reacoleccion de datos, cada uno trabaja con un script diferente.
Existen 3 script que limpian y filtran la data para enviarla al EC2, el cual se encargado de sincronizar 
los datos y almacenarlos en MySQL. Una vez llenadas las tablas se enviaran cada minuto a Elasticsearch. 
El repositoro que utiliza el web service Flask, debe 
estar instalado en el EC2 y esperar los request de los agentes de monitoreo.</p>    


## Despliegue de Proyecto

### El Deploy estara habilitado hasta 30/09/2022
### Proyecto levantado en http://44.204.82.115:9200/aps/_search

### Portal de Kibana   
Para ingresar dirigirse a [http://44.204.82.115/]
### Para iniciar sesion solicitar credenciales a los siguientes correos:
- kercmari@espol.edu.ec
- yorodrig@espol.edu.ec

### Dashboard
Dirigirse al menu (=) en la parte superior izquierda y luego Analytics


### Fases para levantamiento del Proyecto
- 1. Recopilación de datos
    - 1.1 Agente SNMP
### Se utiliza el script de Python alojado en el directorio: 
[/snmp/script/get_and_post_snpm_script.py ]
para obtener los datos de la controladora

1.2 Agente Wireshark
Aqui se capturaron datos y muestras de paquestes 

tshark -b filesize:6000 -a files:10 -w traffic.pcapng
1.3 Agente Rasberry Pi

2. Levantamiento del Servidor EC2
Se instalo una instancia en AWS EC2 instancia  EC2  Ubuntu t4g.xlarge
con 2GB de RAM y 30 GB de almacenamiento. Para efectos de prueba 
se utilizó la configuración de seguridad de forma general, que 
permita todo el tráfico 0.0.0.0/0 

3. Levantar Kibana y ElastichSearch

sh -i <path to .pem file> ubuntu@<dns name>

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install default-jre

java -version

sudo apt-get install nginx

sudo systemctl start nginx

sudo systemctl status nginx

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list

sudo apt-get update

sudo apt-get install elasticsearch

sudo nano /etc/elasticsearch/elasticsearch.yml
xpack.security.enabled: false
network.host: 0.0.0.0
http.cors.enabled: true
http.cors.allow-origin: "*"

sudo nano /etc/elasticsearch/jvm.options

-Xms128m
-Xmx128m

sudo systemctl start elasticsearch

sudo systemctl enable elasticsearch

sudo systemctl status elasticsearch

sudo curl -XGET http://localhost:9200

sudo apt-get install kibana

sudo systemctl start kibana

sudo systemctl enable kibana

sudo systemctl status kibana

echo "kibanaadmin:`openssl passwd -apr1`" | sudo tee -a /etc/nginx/htpasswd.users
kibanaadmin
holaker
sudo nano /etc/nginx/sites-available/44.204.82.115

server {
    listen 80;

    server_name 44.204.82.115;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

sudo ln -s /etc/nginx/sites-available/44.204.82.115 /etc/nginx/sites-enabled/44.204.82.115

sudo nginx -t

sudo systemctl restart nginx

sudo ufw allow 'Nginx Full'

4. Levantamiento del Web Services Flask 
4.0 Instalar servicios 
python3 -m venv entorno
sudo apt install python3-virtualenv
4.1 Crear el environment
En este caso no es necesario crearlo porque ya existe, solo se debe desacargr el repo del api
que se encuentra en el siguiente directorio proyecto_monitoreo/flask_api_web_serivce/
4.2 Correr el servicio
Una vez inslado pytohn y virtualenv
instalar los requerimientos
pip install -r requirements.txt
Por ultimo 
$ python3 -m venv venv
$ source venv/bin/activate 
ejecuta estos comandos para activar el environmet
y correrlo con python index.py
