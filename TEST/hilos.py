from pysnmp.hlapi import *
from threading import *
import time
import rrdtool


total_input_traffic = 0
total_output_traffic = 0
oid = "1.3.6.1.2.1.2.2.1.10.1"
comunidad = "variation/virtualtable"
host = "10.100.71.200"
nombreBase = "grafica"
puerto = 1024
version = 2



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
            print(resultado)
    return resultado


def iniciarGrafica1(host,version,puerto,comunidad,nombreBase):

    ret = rrdtool.create(nombreBase+'.rrd',
                         "--start", 'N',  # N de now.
                         "--step", '1',
                         "DS:inoctets:COUNTER:600:U:U",  # DS: "String" nombre de la variable
                         "RRA:AVERAGE:0.5:1:600")
    contadorDeGraficación = 3
    tiempoInicial = int(time.time())
    while 1:
        if (contadorDeGraficación < 1):
            ret = rrdtool.graph(nombreBase + ".png",
                                "--start", str(tiempoInicial),  # Abrir XML y checar un valor válido y existente
                                #                "--end", "N",
                                "--vertical-label=Octects/s",
                                "DEF:inoctets=" + nombreBase + ".rrd:inoctets:AVERAGE",
                                "AREA:inoctets#00FF00:IfInOctects"
                                )
            contadorDeGraficación = 3
            tiempoInicial = int(time.time())
        else:
            total_input_traffic = int(consultaSNMP(comunidad, host, puerto, version, oid))# el 3 es de grupo de interfaz y checar si funciona la inalambrica en la interfaz 3
            #total_output_traffic = int(consultaSNMP(comunidad, hostname, puerto, version, oid))
            valor = "N:" + str(total_input_traffic) 
            print(valor)
            rrdtool.update(nombreBase + ".rrd", valor)
            rrdtool.dump(nombreBase + '.rrd', nombreBase + '.xml')
            time.sleep(1)
            contadorDeGraficación -= 1
    return

def mandarGrafica1():
    
    #hilo2 = threading.Thread(name="ObtenerIndormación", target=consultaSNMP(hostname, puerto, version, comunidad))
    #hilo2.start()
    iniciarGrafica1(host, version, puerto, comunidad, nombreBase)
    return



def ciclo1():
    
    print("1")
        #time.sleep(1);
        

    return

def ciclo2():
    while 1:
        print("2")
        #time.sleep(2);
        

    return

def main():
     print ("hello world	")

     t = Timer(1.0, ciclo2)
     t.start()
     while 1:
         print("Seguimos")
     


    #hilo1=threading.Thread(name="Graficar1",target=mandarGrafica1)
	#hilo1.start()
     
     


     #res = consultaSNMP(comunidad,host,puerto,version,oid)
     #graf = iniciarGrafica1(host,version,puerto,comunidad,nombreBase)
     #mandarGrafica1()
     #print()






if __name__ == '__main__':
	main()
	pass
