from . import SnmpGet


def obtenerInfo(hostname, puerto, versionSNMP,comunidad):
    puerto=int(puerto)
    versionSNMP= int(versionSNMP)
    diccionario={'so':SnmpGet.consultaSNMPSO(comunidad,hostname,puerto,versionSNMP, '1.3.6.1.2.1.1.1.0'),
                 'tiempoReinicio':SnmpGet.consultaSNMPCompleta(comunidad,hostname,puerto,versionSNMP,'1.3.6.1.2.1.1.3.0'),
                 'locacion':SnmpGet.consultaSNMPCompleta(comunidad,hostname,puerto,versionSNMP,'1.3.6.1.2.1.1.6.0'),
                 'nombre': SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.1.5.0'),
                 'interfaces':SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.2.1.0'),
                 'contacto':SnmpGet.consultaSNMP(comunidad, hostname, puerto, versionSNMP, '1.3.6.1.2.1.1.4.0'),
                 'host':hostname
                 }
    #print(diccionario)
    return diccionario