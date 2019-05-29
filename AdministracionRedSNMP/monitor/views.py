from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from monitor.models import Image
from django.contrib.staticfiles.templatetags.staticfiles import static
from rest_framework import viewsets
from . import SnmpGet
from . import ConfigurationAdmin
import os
#import logging
import time
from . import forms
#from . import ConfigurationAdmin
from .models import *
from django.core.files.storage import FileSystemStorage

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
            print(interfaces)
            status = int(0)
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

"""
def obtenerInfoRouter(request, name):
    try:
        router = Router.objects.get(pk=name)

        r = ConfigurationAdmin.ConfigurationAdmin(router.ip,router.getway,"tap0")
        detallesRouter = r.querySNMPInfo()
        #detallesAgente = ObtenerInformacion.obtenerInfo(agent.hostname, agent.puerto, agent.version, agent.grupo)

    except router.DoesNotExist:
        raise Http404("Agente no encontrado!")
    
    context = {'detallesRouter':detallesRouter,
                'nombreHost': name}

    return render(request,'adminlte/inventario.html',context)
"""

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

def adminInventario(request):

    return render(request,'adminlte/inventario.html')


def cargarArchivosConf(request):

    return render(request,'adminlte/configArchivos.html')


def subirArchivoConf(request):
    if request.method == 'POST' and request.FILES['config-file']:
        # Usando IP actualizariamos tabla con info de Router!
        print(request.POST['IP'])
        config_file = request.FILES['config-file']
        fs = FileSystemStorage(location='assets/')
        filename = fs.save(config_file.name, config_file)
        uploaded_file_url = fs.url(filename)
        return render(request, 'adminlte/configArchivos.html', {
            'uploaded_file_url': uploaded_file_url
        })


"""
def actualizaImg(request):
    iStatic = static('DiegoEGCPU.png')
    img = str(settings.STATICFILES_DIRS[0])+"/DiegoEGCPU.png"
    i = "./assets/DiegoEGCPU.png"
    image_data = open(img, "rb").read()
    #image_data, mimetype="image/png"
    return HttpResponse(iStatic)
"""

###Not used to HTTP ###


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


def getRoutersAvailable():

        routers = Router.objects.all()
        li = []
        d = {}
        for router in router:
            d = {}
            d['ip'] = router.ip
            d['hostname'] = router.hostname
            d['version'] = router.version
            d['puerto'] = router.puerto
            d['grupo'] = router.grupo
            d['os'] = router.os
            d['interfaces'] = router.interfaces
            d['ubicacion'] = router.ubicacion
            d['archivo'] = router.archivo
            li.append(d)
        
        return li


