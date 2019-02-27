from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from . import SnmpGet
from . import Grafica
from threading import *
import json
import os
import time

# Create your views here.
def index(request):
    lanzaProceso2()
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
        print(array)
        oidINterfaces = '1.3.6.1.2.1.2.1.0'
        #interfaces = "Down"
        
        interfaces = SnmpGet.consultaSNMP(str(array[3]),str(array[0]),int(str(array[2])),int(str(array[1])),oidINterfaces)
        print(interfaces)
        status = int(interfaces)
        if status>0:
            status="Up"
        else:
            status="Down"

        #print(interfaces)

        diccionario = {'nombre':str(array[4]),
                        'host':str(array[0]),
                       'version':str(array[1]),
                       'puerto':str(array[2]),
                       'status':str(status),
                       'interfaces':str(interfaces),
                       'grupo':str(array[3])}

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



##Not used to HTTP ###



def lanzaProceso1():
    pid=os.fork()
    if pid:
        # parent
        #while True:
        print("I'm the parent DJANGO")
            #time.sleep(0.5)    
    else:
        # child
        #while True:
            print("I'm just a child Grafica 1")
            Grafica.iniciarGrafica1('localhost',2,161,'gr_4cm3','gr_4cm3localhost')
            #time.sleep(0.5)

    #hilo1 = Timer(5.0,Grafica1.iniciarGrafica1('localhost',2,161,'gr_4cm3','gr_4cm3localhost'))
    #hilo1.daemon = True
    #hilo1.start()
    print("Sigo Adelante")
    return

def lanzaProceso2():
    pid=os.fork()
    if pid:
        # parent
        print("I'm the parent Django")   
    else:
        # child
            print("I'm just a child Grafica 2")
            Grafica.iniciarGrafica2('localhost',2,161,'gr_4cm3','gr_4cm3localhost')

    print("Sigo Adelante")
    return


def lanzaProceso3():
    pid=os.fork()
    if pid:
        # parent
        print("I'm the parent Django")   
    else:
        # child
            print("I'm just a child Grafica 3")
            Grafica.iniciarGrafica3('localhost',2,161,'gr_4cm3','gr_4cm3localhost')

    print("Sigo Adelante")
    return


def lanzaProceso4():
    pid=os.fork()
    if pid:
        # parent
        print("I'm the parent Django")   
    else:
        # child
            print("I'm just a child Grafica 4")
            Grafica.iniciarGrafica4('localhost',2,161,'gr_4cm3','gr_4cm3localhost')

    print("Sigo Adelante")
    return


def lanzaProceso5():
    pid=os.fork()
    if pid:
        # parent
        print("I'm the parent Django")   
    else:
        # child
            print("I'm just a child Grafica 5")
            Grafica.iniciarGrafica5('localhost',2,161,'gr_4cm3','gr_4cm3localhost')

    print("Sigo Adelante")
    return






