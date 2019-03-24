from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from monitor.models import Image
from django.core import serializers
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
from rest_framework import viewsets
from monitor.serializers import ImageSerializer
from . import SnmpGet
from . import Grafica
from . import Thrend
import logging
import json
import os
import time
from . import forms
from . import ObtenerInformacion
from .models import *

from . import Invoker
invoker = Invoker.Invoker()
print (hex(id(invoker)))
invoker.startA()



# Create your views here.
def index(request):

    return render(request, 'adminlte/index.html')

def verAgentes(request):
    if request.method == 'GET':
        agents = Agent.objects.all()
        lista = []
        for agent in agents:
            oidINterfaces = '1.3.6.1.2.1.2.1.0'
            interfaces = SnmpGet.consultaSNMP(str(agent.grupo),str(agent.hostname),int(agent.puerto),int(agent.version),oidINterfaces)
            #print(interfaces)
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
            #print(interfaces)
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
    
    agents  = getAgentsAvailable()

    dic = { 'agentes':agents}
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

def actualizaImg(request):
    iStatic = static('DiegoEGCPU.png')
    img = str(settings.STATICFILES_DIRS[0])+"/DiegoEGCPU.png"
    i = "./assets/DiegoEGCPU.png"
    image_data = open(img, "rb").read()
    #image_data, mimetype="image/png"
    return HttpResponse(iStatic)



class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer






##Not used to HTTP ###



def sendEmail(email,subject,message):

    #subject = 'Evidencia 3 '
    #message = 'Equipo 10 Grupo 4CM3' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    recipient_list.append(str(email))
    res = send_mail(subject,message,email_from,recipient_list,)
    if res:
        print("Correo Electronico enviado a "+email)
        logging.info("Correo Electronico enviado a "+email)
    else: 
        print("Ocurrió un error al enviar el correo elcronico a "+email)
        logging.info("Ocurrió un error al enviar el correo elcronico a "+email)
    
    return  


def getAgentsAvailable():

        agents = Agent.objects.all()
        li = []
        d = {}
        for agent in agents:
            d = {}
            d['name'] = agent.name
            d['hostname'] = agent.hostname
            d['version'] = agent.version
            d['puerto'] = agent.puerto
            d['grupo'] = agent.grupo
            d['email'] = agent.email
            li.append(d)
        
        return li



