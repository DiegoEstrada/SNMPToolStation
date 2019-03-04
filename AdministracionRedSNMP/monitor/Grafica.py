import sys
import rrdtool
import time
from . import SnmpGet 


class Grafica:
    def __init__(self,hostname,versionSNMP,puerto,comunidad,archivordd):
        print("CONSTRUCTOR")
        self.hostname = hostname
        self.versionSNMP = versionSNMP
        self.puerto = puerto
        self.comunidad = comunidad
        self.archivordd = archivordd


    def getTraficoRed(self):
        ret = rrdtool.create('assets/'+self.archivordd+'TraficoRed.rrd',
                         "--start", 'N',  
                         "--step", '1',
                         "DS:inoctets:COUNTER:600:U:U",
                         "DS:outoctets:COUNTER:600:U:U",
                         "RRA:AVERAGE:0.5:1:600",
                         "RRA:AVERAGE:0.5:1:600")
        cont = 5
        tiempoInicial = int(time.time())
        while 1:
            if (cont < 1):
                ret = rrdtool.graph('assets/'+self.archivordd + "TraficoRed.png",
                                    "--start", str(tiempoInicial),  
                                    "--vertical-label=Equipo2Bytes/s",
                                    "DEF:inoctets=" +'assets/'+ self.archivordd + "TraficoRed.rrd:inoctets:AVERAGE",
                                    "DEF:outoctets=" +'assets/'+ self.archivordd + "TraficoRed.rrd:outoctets:AVERAGE",
                                    "LINE1:inoctets#00FF00:InTrafico",
                                    "LINE1:inoctets#FF0000:OutTrafico")
                cont = 5
                tiempoInicial = int(time.time())
            else:
                inputTr = int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.2.2.1.10.1'))
                outputTr = int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.2.2.1.16.1'))
                valor = "N:" + str(inputTr) + ":" + str(outputTr)
                print(valor)
                rrdtool.update('assets/'+self.archivordd + "TraficoRed.rrd", valor)
                time.sleep(1)
                cont -= 1
        
        return

    def getICMP(self):
        ret = rrdtool.create('assets/'+self.archivordd+'EstadisticaICMP.rrd',
                            "--start", 'N',  
                            "--step", '1',
                            "DS:inconexiones:GAUGE:600:U:U",
                            "DS:outconexiones:GAUGE:600:U:U",  
                            "RRA:AVERAGE:0.5:1:600",
                            "RRA:AVERAGE:0.5:1:600")
        cont = 3
        tiempoInicial = int(time.time())
        while 1:
            if (cont < 1):
                ret = rrdtool.graph('assets/'+self.archivordd + "EstadisticaICMP.png",
                                    "--start", str(tiempoInicial), 
                                    "--vertical-label=Equipo2PaquetesICMP/s",
                                    "DEF:inconexiones=" + 'assets/'+ self.archivordd + "EstadisticaICMP.rrd:inconexiones:AVERAGE",
                                    "DEF:outconexiones=" + 'assets/'+ self.archivordd + "EstadisticaICMP.rrd:outconexiones:AVERAGE",
                                    "LINE1:inconexiones#00FF00:In icmp",
                                    "LINE1:outconexiones#FF0000:Out icmp")
                cont = 3
                tiempoInicial = int(time.time())
            else:
                input_icmp = int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.5.1.0 '))
                output_icmp= int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.5.14.0'))
                valor = "N:" + str(input_icmp) + ':' + str(output_icmp)
                print(valor)
                rrdtool.update('assets/'+self.archivordd + "EstadisticaICMP.rrd", valor)
                time.sleep(1)
                cont -= 1
        return

    def getSegmentosTCP(self):
        ret = rrdtool.create('assets/'+self.archivordd+'SegmentosTCP.rrd',
                            "--start", 'N',  
                            "--step", '1',
                            "DS:inconexiones:COUNTER:600:U:U",
                            "DS:outconexiones:COUNTER:600:U:U",
                            "RRA:AVERAGE:0.5:1:600",
                            "RRA:AVERAGE:0.5:1:600")
        cont = 5
        tiempoInicial = int(time.time())
        while 1:
            if (cont < 1):
                ret = rrdtool.graph('assets/'+self.archivordd + "SegmentosTCP.png",
                                    "--start", str(tiempoInicial), 
                                    "--vertical-label=Equipo2Segmentos/s",
                                    "DEF:inconexiones=" + 'assets/' + self.archivordd + "SegmentosTCP.rrd:inconexiones:AVERAGE",
                                    "DEF:outconexiones=" + 'assets/' + self.archivordd + "SegmentosTCP.rrd:outconexiones:AVERAGE",
                                    "LINE1:inconexiones#00FF00:InTCP",
                                    "LINE1:outconexiones#FF0000:OutTCP")
                tiempoInicial = int(time.time())
                cont = 5
            else:
                input_tcp = int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.6.10.0'))
                output_tcp= int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.6.11.0'))
                valor = "N:" + str(input_tcp) + ':' + str(output_tcp)
                print(valor)
                rrdtool.update('assets/'+self.archivordd + "SegmentosTCP.rrd", valor)
                time.sleep(1)
                cont -= 1
        return

    def getDatagramasIP(self):
        ret = rrdtool.create('assets/'+self.archivordd+'DatagramasIP.rrd',
                            "--start", 'N',  
                            "--step", '1',
                            "DS:inconexiones:COUNTER:600:U:U",
                            "DS:outconexiones:COUNTER:600:U:U",  
                            "RRA:AVERAGE:0.5:1:600",
                            "RRA:AVERAGE:0.5:1:600")
        cont = 5
        tiempoInicial = int(time.time())
        while 1:
            if (cont < 1):
                ret = rrdtool.graph('assets/'+self.archivordd + "DatagramasIP.png",
                                    "--start", str(tiempoInicial),  
                                    "--vertical-label=Equipo2IP/s",
                                    "DEF:inconexiones=" + 'assets/'+self.archivordd + "DatagramasIP.rrd:inconexiones:AVERAGE",
                                    "DEF:outconexiones=" + 'assets/'+self.archivordd + "DatagramasIP.rrd:outconexiones:AVERAGE",
                                    "LINE1:inconexiones#00FF00:InIP",
                                    "LINE1:outconexiones#FF0000:OutIP")
                tiempoInicial = int(time.time())
                cont = 5
              
            else:
                input_ip = int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.4.31.1.1.3.2'))
                output_ip= int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.4.31.1.1.20.2'))
                valor = "N:" + str(input_ip) + ':' + str(output_ip)
                print(valor)
                rrdtool.update('assets/'+self.archivordd + "DatagramasIP.rrd", valor)
                time.sleep(1)
                cont -= 1
        return

    def getRespuestasPING(self):
        ret = rrdtool.create('assets/'+self.archivordd+'RespuestasPING.rrd',
                            "--start", 'N', 
                            "--step", '1',
                            "DS:inconexiones:GAUGE:600:U:U",
                            "DS:outconexiones:GAUGE:600:U:U",  
                            "RRA:AVERAGE:0.5:1:600",
                            "RRA:AVERAGE:0.5:1:600")
        cont = 3
        tiempoInicial = int(time.time())
        while 1:
            if (cont < 1):
                ret = rrdtool.graph('assets/'+self.archivordd + "RespuestasPING.png",
                                    "--start", str(tiempoInicial), 
                                    "--vertical-label=Equipo2Respuestas/s",
                                    "DEF:inconexiones=" + 'assets/'+self.archivordd + "RespuestasPING.rrd:inconexiones:AVERAGE",
                                    "DEF:outconexiones=" + 'assets/'+self.archivordd + "RespuestasPING.rrd:outconexiones:AVERAGE",
                                    "LINE1:inconexiones#00FF00:In ping",
                                    "LINE1:outconexiones#FF0000:Out ping")
                tiempoInicial = int(time.time())
                cont = 3
            else:
                input_ping = int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.5.9.0'))
                output_ping= int(SnmpGet.consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.5.20.0'))
                valor = "N:" + str(input_ping) + ':' + str(output_ping)
                print(valor)
                rrdtool.update('assets/'+self.archivordd + "RespuestasPING.rrd", valor)
                time.sleep(1)
                cont -= 1
        return




