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
<p class="text-align-justify">El proyecto consta de tres agentes de reacoleccion de datos, cada uno trabaja con un script diferente.
Existen 3 script que limpian y filtran la data para enviarla al EC2, el cual se encargado de sincronizar 
los datos y almacenarlos en MySQL. Una vez llenado las tablas se enviaran cada minuto a Elasticsearch. 
El repositoro que utiliza el web service Flask debe 
estar instalado en el EC2 y esperar los request de los agentes de monitoreo.</p>    

