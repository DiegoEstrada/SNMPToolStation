import sys
import rrdtool
import time
from pysnmp.hlapi import *

class Grafica:
    def __init__(self,hostname,versionSNMP,puerto,comunidad,archivordd):
        print("CONSTRUCTOR")
        self.hostname = hostname
        self.versionSNMP = versionSNMP
        self.puerto = puerto
        self.comunidad = comunidad
        self.archivordd = archivordd


    def getTraficoRed(self):
        print("Graphing Trafico")
        ret = rrdtool.create('assets/'+self.archivordd+'TraficoRed.rrd',
                         "--start", 'N',  # N de now.
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
                                    "--vertical-label=Equipo2TICMP",
                                    "DEF:inoctets=" +'assets/'+ self.archivordd + "TraficoRed.rrd:inoctets:AVERAGE",
                                    "DEF:outoctets=" +'assets/'+ self.archivordd + "TraficoRed.rrd:outoctets:AVERAGE",
                                    "AREA:inoctets#00FF00:InTrafico",
                                    "AREA:inoctets#FF0000:OutTrafico")
                cont = 5
                tiempoInicial = int(time.time())
            else:
                inputTr = int(consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.2.2.1.10.1'))
                outputTr = int(consultaSNMP(self.comunidad, self.hostname, self.puerto, self.versionSNMP, '1.3.6.1.2.1.2.2.1.16.1'))
                valor = "N:" + str(inputTr) + ":" + str(outputTr)
                print(valor)
                rrdtool.update('assets/'+self.archivordd + "TraficoRed.rrd", valor)
                time.sleep(1)
                cont -= 1
        
        return


def consultaSNMP(comunidad, host,puerto,version, oid):
    version=version-1
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad, mpModel=version),
               UdpTransportTarget((host, puerto)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB = (' = '.join([x.prettyPrint() for x in varBind]))
            resultado = varB.split()[2]
    return resultado


def main():
    gr = Grafica('localhost',2,161,'gr_4cm3','gr_4cm3localhost')
    gr.getTraficoRed()



if __name__ == '__main__':
    main()
    pass

