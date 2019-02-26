from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from . import SnmpGet
#from . import Grafica1
import json

# Create your views here.
def index(request):

    return render(request, 'adminlte/index.html')

def verAgentes(request):

    a = staticfiles_storage.path("Agentes.txt")
    #a = url = static('Agentes.txt')
    archivo = open(a, 'r')
    lineas=archivo.readlines()
    #print(lineas)
    lista = []

    for linea in lineas:
        #print(linea)
        array = linea.split(",")
        oidINterfaces = '1.3.6.1.2.1.2.1.0'
        interfaces = SnmpGet.consultaSNMP(str(array[4]),str(array[1]),int(str(array[3])),int(str(array[2])),oidINterfaces)
        status = int(interfaces)
        if status>0:
            status="Up"
        else:
            status="Down"

        #print(interfaces)

        diccionario = {'nombre':str(array[0]),
                        'host':str(array[1]),
                       'version':str(array[2]),
                       'puerto':str(array[3]),
                       'status':str(status),
                       'interfaces':str(interfaces),
                       'grupo':str(array[4])}

        lista.append(diccionario)
    retorno = {'lista':lista}
    archivo.close()
    return render(request, 'adminlte/agentes.html',context=retorno)

def agregarAgente(request):
    return render(request, 'adminlte/agregarAgente.html')

def verAgente(request):
    return render(request, 'adminlte/verAgente.html')

def estadoAgente(request):
    return render(request, 'adminlte/verAgente.html')

def obtenerInfo(request, nombreHost):

    """hostname = "localhost"
    hostname = str(local)
    puerto = 161
    versionSNMP = 2
    comunidad = 'gr_4cm3'"""
    print(nombreHost)

    

    #diccionario={'descripcion':SnmpGet.consultaSNMP(comunidad,hostname,puerto,versionSNMP, '1.3.6.1.2.1.1.1.0'), 'icmp':SnmpGet.consultaSNMP(comunidad,hostname,puerto,int(2),'1.3.6.1.2.1.5.1.0 ')}
    diccionario = {'host': nombreHost}
    #jsonArray = json.dumps(diccionario)
    #json_Serialized = serializers.serialize('json',jsonArray)
    
    #print(diccionario)
    #context = {'object':diccionario}
    context = diccionario
    return render(request,'adminlte/verAgente.html',context)



def devuelveAgentes():
    #print("Oro vos")
    archivo = open(ruta, 'r')
    lineas=archivo.readlines()
    #contenido = str(hostname) + ',' + str(versionSNMP) + ',' + str(puerto) + ',' + str(comunidad) + ',' + str(nombreBase)+'\n'
    #bandera = False
    lista = [];
    for linea in lineas:
        array = linea.split(",")
        oidINterfaces = '1.3.6.1.2.1.2.1.0'
        interfaces = consultaSNMP(str(array[3]),str(array[0]),int(str(array[2])),int(str(array[1])),oidINterfaces)
        status = int(interfaces);
        if status>0:
            status="Up"
        else:
            status="Down"

        #print(interfaces)

        diccionario = {'host':str(array[0]),
                       'version':str(array[1]),
                       'puerto':str(array[2]),
                       'status':str(status),
                       'interfaces':str(interfaces),
                       'grupo':str(array[3])}

        lista.append(diccionario)


    print(lista)
    archivo.close()
    return  


##Not used to HTTP ###
