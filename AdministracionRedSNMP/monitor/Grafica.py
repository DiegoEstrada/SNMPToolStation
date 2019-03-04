import sys
import rrdtool
import time
from . import SnmpGet 


def iniciarGrafica1(hostname,versionSNMP,puerto,comunidad,nombreBase):
    ret = rrdtool.create('assets/'+nombreBase+'red.rrd',
                         "--start", 'N',  # N de now.
                         "--step", '1',
                         "DS:inoctets:COUNTER:600:U:U",
                         "RRA:AVERAGE:0.5:1:600")
    contadorDeGraficación = 5
    tiempoInicial = int(time.time())
    while 1:
        if (contadorDeGraficación < 1):
            ret = rrdtool.graph('assets/'+nombreBase + "red.png",
                                "--start", str(tiempoInicial),  # Abrir XML y checar un valor válido y existente
                                #                "--end", "N",
                                "--vertical-label=Equipo2TICMP",
                                "DEF:inoctets=" +'assets/'+ nombreBase + "red.rrd:inoctets:AVERAGE",
                                "AREA:inoctets#00FF00:InTrafico")
            contadorDeGraficación = 5
            tiempoInicial = int(time.time())
        else:
            total_input_traffic = int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.2.2.1.10.1'))# el 3 es de grupo de interfaz y checar si funciona la inalambrica en la interfaz 3
            valor = "N:" + str(total_input_traffic)
            print(valor)
            rrdtool.update('assets/'+nombreBase + "red.rrd", valor)
            #rrdtool.dump(nombreBase + 'red.rrd', nombreBase + 'red.xml')
            time.sleep(1)
            contadorDeGraficación -= 1
    return



def iniciarGrafica2(hostname,versionSNMP,puerto,comunidad,nombreBase):
    ret = rrdtool.create('assets/'+nombreBase+'icmp.rrd',
                         "--start", 'N',  # N de now.
                         "--step", '1',
                         "DS:inconexiones:GAUGE:600:U:U",
                         "DS:outconexiones:GAUGE:600:U:U",  # DS: "String" nombre de la variable
                         "RRA:AVERAGE:0.5:1:600",
                         "RRA:AVERAGE:0.5:1:600")
    contadorDeGraficación = 3
    tiempoInicial = int(time.time())
    while 1:
        if (contadorDeGraficación < 1):
            ret = rrdtool.graph('assets/'+nombreBase + "icmp.png",
                                "--start", str(tiempoInicial),  # Abrir XML y checar un valor válido y existente
                                #                "--end", "N",
                                "--vertical-label=Conexiones/s",
                                "DEF:inconexiones=" + 'assets/'+ nombreBase + "icmp.rrd:inconexiones:AVERAGE",
                                "DEF:outconexiones=" + 'assets/'+ nombreBase + "icmp.rrd:outconexiones:AVERAGE",
                                "AREA:inconexiones#00FF00:In icmp",
                                "LINE1:outconexiones#0000FF:Out icmp")
            contadorDeGraficación = 3
            tiempoInicial = int(time.time())
        else:
            input_icmp = int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.5.1.0 '))# el 3 es de grupo de interfaz y checar si funciona la inalambrica en la interfaz 3
            output_icmp= int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.5.14.0'))
            valor = "N:" + str(input_icmp) + ':' + str(output_icmp)
            print(valor)
            rrdtool.update('assets/'+nombreBase + "icmp.rrd", valor)
            #rrdtool.dump(nombreBase + 'icmp.rrd', nombreBase + 'icmp.xml')
            time.sleep(1)
            contadorDeGraficación -= 1
    return


def iniciarGrafica3(hostname,versionSNMP,puerto,comunidad,nombreBase):
    ret = rrdtool.create('assets/'+nombreBase+'tcp.rrd',
                         "--start", 'N',  # N de now.
                         "--step", '1',
                         "DS:inconexiones:COUNTER:600:U:U",
                         "DS:outconexiones:COUNTER:600:U:U",  # DS: "String" nombre de la variable
                         "RRA:AVERAGE:0.5:1:600",
                         "RRA:AVERAGE:0.5:1:600")
    contadorDeGraficación = 5
    tiempoInicial = int(time.time())
    while 1:
        if (contadorDeGraficación < 1):
            ret = rrdtool.graph('assets/'+nombreBase + "tcp.png",
                                "--start", str(tiempoInicial),  # Abrir XML y checar un valor válido y existente
                                #                "--end", "N",
                                "--vertical-label=Bytes/s",
                                "DEF:inconexiones=" + 'assets/' + nombreBase + "tcp.rrd:inconexiones:AVERAGE",
                                "DEF:outconexiones=" + 'assets/' + nombreBase + "tcp.rrd:outconexiones:AVERAGE",
                                "AREA:inconexiones#00FF00:InTCP",
                                "LINE1:outconexiones#0000FF:OutTCP")
            contadorDeGraficación = 5
            tiempoInicial = int(time.time())
        else:
            input_tcp = int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.6.10.0'))# el 3 es de grupo de interfaz y checar si funciona la inalambrica en la interfaz 3
            output_tcp= int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.6.11.0'))
            valor = "N:" + str(input_tcp) + ':' + str(output_tcp)
            print(valor)
            rrdtool.update('assets/'+nombreBase + "tcp.rrd", valor)
            #rrdtool.dump(nombreBase + 'tcp.rrd', nombreBase + 'tcp.xml')
            time.sleep(1)
            contadorDeGraficación -= 1
    return


def iniciarGrafica4(hostname,versionSNMP,puerto,comunidad,nombreBase):
    ret = rrdtool.create('assets/'+nombreBase+'udp.rrd',
                         "--start", 'N',  # N de now.
                         "--step", '1',
                         "DS:inconexiones:COUNTER:600:U:U",
                         "DS:outconexiones:COUNTER:600:U:U",  # DS: "String" nombre de la variable
                         "RRA:AVERAGE:0.5:1:600",
                         "RRA:AVERAGE:0.5:1:600")
    contadorDeGraficación = 5
    tiempoInicial = int(time.time())
    while 1:
        if (contadorDeGraficación < 1):
            ret = rrdtool.graph('assets/'+nombreBase + "udp.png",
                                "--start", str(tiempoInicial),  # Abrir XML y checar un valor válido y existente
                                #                "--end", "N",
                                "--vertical-label=Bytes/s",
                                "DEF:inconexiones=" + 'assets/'+nombreBase + "udp.rrd:inconexiones:AVERAGE",
                                "DEF:outconexiones=" + 'assets/'+nombreBase + "udp.rrd:outconexiones:AVERAGE",
                                "AREA:inconexiones#00FF00:InUDP",
                                "LINE1:outconexiones#0000FF:OutUDP")
            contadorDeGraficación = 5
            tiempoInicial = int(time.time())
        else:
            input_udp = int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.7.1.0'))
            output_udp= int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.7.4.0'))
            valor = "N:" + str(input_udp) + ':' + str(output_udp)
            print(valor)
            rrdtool.update('assets/'+nombreBase + "udp.rrd", valor)
            #rrdtool.dump(nombreBase + 'udp.rrd', nombreBase + 'udp.xml')
            time.sleep(1)
            contadorDeGraficación -= 1
    return


def iniciarGrafica5(hostname,versionSNMP,puerto,comunidad,nombreBase):
    ret = rrdtool.create('assets/'+nombreBase+'ping.rrd',
                         "--start", 'N',  # N de now.
                         "--step", '1',
                         "DS:inconexiones:GAUGE:600:U:U",
                         "DS:outconexiones:GAUGE:600:U:U",  # DS: "String" nombre de la variable
                         "RRA:AVERAGE:0.5:1:600",
                         "RRA:AVERAGE:0.5:1:600")
    contadorDeGraficación = 3
    tiempoInicial = int(time.time())
    while 1:
        if (contadorDeGraficación < 1):
            ret = rrdtool.graph('assets/'+nombreBase + "ping.png",
                                "--start", str(tiempoInicial),  # Abrir XML y checar un valor válido y existente
                                #                "--end", "N",
                                "--vertical-label=Conexiones/s",
                                "DEF:inconexiones=" + 'assets/'+nombreBase + "ping.rrd:inconexiones:AVERAGE",
                                "DEF:outconexiones=" + 'assets/'+nombreBase + "ping.rrd:outconexiones:AVERAGE",
                                "AREA:inconexiones#00FF00:In ping",
                                "LINE1:outconexiones#0000FF:Out ping")
            contadorDeGraficación = 3
            tiempoInicial = int(time.time())
        else:
            input_ping = int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.5.9.0'))# el 3 es de grupo de interfaz y checar si funciona la inalambrica en la interfaz 3
            output_ping= int(SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.5.20.0'))
            valor = "N:" + str(input_ping) + ':' + str(output_ping)
            print(valor)
            rrdtool.update('assets/'+nombreBase + "ping.rrd", valor)
            #rrdtool.dump(nombreBase + 'ping.rrd', nombreBase + 'ping.xml')
            time.sleep(1)
            contadorDeGraficación -= 1
    return

