<h1 align="center"> SHIPTRACKER 💯 </h1>

> Sistema Unificado de Monitoreo de Calidad de Servicio y Calidad de Experiencia en Redes Wi-Fi
<h3> Members </h3>

<div align="center">
 <table>
  <tr>
    <td align="center"><a href="https://github.com/kercmari"><img src="https://avatars.githubusercontent.com/u/62037369?v=4" width="100px;" alt=""/><br /><sub><b>Kerly Cervantes</b></sub></a><br/><a>🌹</a></td>
<td align="center"><a href="https://github.com/YiamRodriguezDelgado"><img src="https://avatars.githubusercontent.com/u/44529630?v=4" width="100px;" alt=""/><br /><sub><b>Yiam Rodriguez</b></sub></a><br/><a>😎</a></td>
  
## Descripción del Proyecto
    
El proyecto consta de tres agentes de reacoleccion de datos, cada uno trabaja con un script diferente.
Existen 3 script que limpian y filtran la data para enviarla al EC2, el cual se encargado de sincronizar 
los datos y almacenarlos en MySQL. Una vez llenado las tablas se enviaran cada minuto a Elasticsearch. 
Aqui esta el repositoro de web service flask https://github.com/kercmari/proyecto_monitoreo.git, este debe 
estar instalado en el EC2 esperar los request de los agentes de monitoreo.
