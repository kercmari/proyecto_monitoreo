El proyecto consta de tres agentes de reacoleccion de datos, cada uno trabaja con un script diferente.
Esta planteado 3 script que limpian y filtran la data para enviarla al EC2 el cual se encargado de sincronizar 
los datos y almacenarlos en mysql. Una vez llenado las tablas se enviaran cada minuto a elasticsearch. 
Aqui esta el repositoro de web service flask https://github.com/kercmari/proyecto_final.git, este debe 
estar instalado en el EC2 para estar esperando los request de los agentes de monitoreo.
