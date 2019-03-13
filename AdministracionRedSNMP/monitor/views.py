from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.mail import send_mail
from . import SnmpGet
from . import Grafica
import logging
from threading import *
import json
import os
import time
from . import forms
from . import ObtenerInformacion
from .models import *

# Create your views here.
def index(request):
    logging.basicConfig(filename='monitor/snmpTool.log',format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)

    #grafica = Grafica.Grafica('localhost',2,161,'gr_4cm3','gr_4cm3localhost')
    """
    lanzarGrafica(1,grafica)
    lanzarGrafica(2,grafica)
    lanzarGrafica(3,grafica)
    lanzarGrafica(4,grafica)
    lanzarGrafica(5,grafica)
    """

    testLogInfo("Testing Log")
    return render(request, 'adminlte/index.html')

def verAgentes(request):
    if request.method == 'GET':
        agents = Agent.objects.all()
        lista = []
        for agent in agents:
            oidINterfaces = '1.3.6.1.2.1.2.1.0'
            interfaces = SnmpGet.consultaSNMP(str(agent.grupo),str(agent.hostname),int(agent.puerto),int(agent.version),oidINterfaces)
            print(interfaces)
            status = int(interfaces)
            if status>0:
                status="Up"
            else:
                status="Down"

            diccionario = {'nombre':str(agent.name),
                            'host':str(agent.hostname),
                        'version':str(agent.version),
                        'puerto':str(agent.puerto),
                        'status':str(status),
                        'interfaces':str(interfaces),
                        'grupo':str(agent.grupo)}

            lista.append(diccionario)
        retorno = {'lista':lista}

    elif request.method == 'POST':
        agentForm = forms.newAgentForm(request.POST)
        if agentForm.is_valid():
            name = agentForm.cleaned_data['name']
            hostname =  agentForm.cleaned_data['hostname']
            version = int(agentForm.cleaned_data['version'])
            puerto = int(agentForm.cleaned_data['puerto'])
            grupo = agentForm.cleaned_data['grupo']
            email = agentForm.cleaned_data['email']
            
        
        # Guardado en base de datos
        newAgent = Agent(name, hostname, version, puerto, grupo, email)
        newAgent.save()

        agents = Agent.objects.all()
        lista = []
        for agent in agents:
            oidINterfaces = '1.3.6.1.2.1.2.1.0'
            interfaces = SnmpGet.consultaSNMP(str(agent.grupo),str(agent.hostname),int(agent.puerto),int(agent.version),oidINterfaces)
            print(interfaces)
            status = int(interfaces)
            if status>0:
                status="Up"
            else:
                status="Down"

            diccionario = {'nombre':str(agent.name),
                            'host':str(agent.hostname),
                        'version':str(agent.version),
                        'puerto':str(agent.puerto),
                        'status':str(status),
                        'interfaces':str(interfaces),
                        'grupo':str(agent.grupo)}

            lista.append(diccionario)
        retorno = {'lista':lista}
    
    return render(request, 'adminlte/agentes.html',context=retorno)

def agregarAgente(request):
    agentForm = forms.newAgentForm()
    context = {'agentForm': agentForm}
    return render(request, 'adminlte/agregarAgente.html', context)

def verAgente(request):
    return render(request, 'adminlte/verAgente.html')

def estadoAgente(request):
    return render(request, 'adminlte/verAgente.html')

def obtenerInfo(request, name):
    try:
        agent = Agent.objects.get(pk=name)
        detallesAgente = ObtenerInformacion.obtenerInfo(agent.hostname, agent.puerto, agent.version, agent.grupo)
    except agent.DoesNotExist:
        raise Http404("Agente no encontrado!")
    
    context = {'detallesAgente':detallesAgente,
                'nombreHost': name}

    return render(request,'adminlte/verAgente.html',context)


def verProyeccion(request):
    res = 0
    #res = sendEmail('diegoestradag97@gmail.com')
    print(res)

    #agents = getAgentsAvailable()
    agents  = ['DiegoEG','Agente Local']

    dic = {'resCorreo':res, 'agentes':agents}
    return render(request,'adminlte/verProyeccion.html',context=dic)


def deleteAgent(request, name):
    # CHANGE TO HTTP DELETE METHOD
    if request.method == 'GET':
        try:
            agent = Agent.objects.get(pk=name)
            agent.delete()
            success = True
        except agent.DoesNotExist:
            success = False
            raise Http404("Agente no encontrado!")
        entry = False
    context = {'success': success, 'entry': entry}
    return render(request,'adminlte/index.html',context=context)


##Not used to HTTP ###

def getAgentsAvailable():
    li = []
    return li


def sendEmail(email):

    subject = 'SNMP Tool Monitor Notification '
    message = 'Its probably that your computer fail' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    recipient_list.append(str(email))
    res = send_mail(subject,message,email_from,recipient_list,)

    return res 

def testLogInfo(message):
    logging.info(message)

def lanzarGrafica(id,grafica):
    
    pid=os.fork()
    if pid:
        # parent
        print("I'm the parent, Django")   
    else:
        # child
            print("I'm just a child Grafica ")
            if int(id)==1:
                #print("UNO")
                grafica.getTraficoRed()
            elif int(id)==2:
                #print("DOS")
                grafica.getICMP()
            elif int(id)==3:
                #print("TRES")
                grafica.getSegmentosTCP()
            elif int(id)==4:
                #print("CUATRO")
                grafica.getDatagramasIP()
            elif int(id)==5:
                #print("TRES")
                grafica.getRespuestasPING()
            else:
                print("Opcion invalida")
            

    print("Sigo Adelante")
    return
