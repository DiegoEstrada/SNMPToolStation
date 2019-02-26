import sys
import rrdtool
import time
from . import SnmpGet
total_input_traffic = 0
total_output_traffic = 0

def iniciarGrafica1(hostname,versionSNMP,puerto,comunidad,nombreBase):
    ret = rrdtool.create(nombreBase+'.rrd',
                         "--start", 'N',  # N de now.
                         "--step", '1',
                         "DS:inoctets:COUNTER:600:U:U",
                         "DS:outoctets:COUNTER:600:U:U",  # DS: "String" nombre de la variable
                         "RRA:AVERAGE:0.5:1:600",
                         "RRA:AVERAGE:0.5:1:600")
    contadorDeGraficación = 3
    tiempoInicial = int(time.time())
    while 1:
        if (contadorDeGraficación < 1):
            ret = rrdtool.graph(nombreBase + ".png",
                                "--start", str(tiempoInicial),  # Abrir XML y checar un valor válido y existente
                                #                "--end", "N",
                                "--vertical-label=Bytes/s",
                                "DEF:inoctets=" + nombreBase + ".rrd:inoctets:AVERAGE",
                                "DEF:outoctets=" + nombreBase + ".rrd:outoctets:AVERAGE",
                                "AREA:inoctets#00FF00:In traffic",
                                "LINE1:outoctets#0000FF:Outtraff")
            contadorDeGraficación = 3
            tiempoInicial = int(time.time())
        else:
            total_input_traffic = int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.2.2.1.10.3'))# el 3 es de grupo de interfaz y checar si funciona la inalambrica en la interfaz 3
            total_output_traffic = int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.2.2.1.16.3'))
            valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
            print(valor)
            rrdtool.update(nombreBase + ".rrd", valor)
            rrdtool.dump(nombreBase + '.rrd', nombreBase + '.xml')
            time.sleep(1)
            contadorDeGraficación -= 1
    return


