from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from monitor.models import Image
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib import messages
from rest_framework import viewsets
from . import SnmpGet
from . import ConfigurationAdmin
import os
#import logging
import time
from . import forms
from . import ObtenerInformacion
from .models import *
from django.core.files.storage import FileSystemStorage

from . import Invoker
invoker = Invoker.Invoker()
print (hex(id(invoker)))
invoker.startA()

ipTapSalida = "192.168.202.5"
interfaceControl = "tap0"
master = Router.objects.get(pk=ipTapSalida)
outAndConrol = ConfigurationAdmin.ConfigurationAdmin(master.ip,master.mascara,master.getway,interfaceControl)
print("Master creado "+str(outAndConrol))





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

def verRouters(request):
    if request.method == 'GET':
        #ipTapSalida = ipTapSalida[:-3] #Just the IP
        


        routers = Router.objects.all()
        

        ips = []
        lista = []
        for router in routers:
            #print(router.ip[:-3]) ##PUEDE QUE LA MASCARA SEA MENOR Y QUIE EL ULTIMO DIGITO DEL ULTOMO OCTETO
            ips.append(router.ip)
        
        ips.remove(ipTapSalida)
        diccio = outAndConrol.querySNMPInfo() 
        lista.append(diccio)

        for ip in ips:
            diccio = outAndConrol.querySNMPInfo(ip)
            lista.append(diccio)

        retorno = {'lista':lista}
        #print(retorno)
    return render(request, 'adminlte/inventario.html',context=retorno)

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


def obtenerInfoRouter(request, name):
    try:
       
       
        r = Router.objects.get(pk=name)
        print(r)

        #print("Hera")  
        if ipTapSalida == name:
            print("CONTECTANDO AL GETWAY")
            detallesRouter = outAndConrol.querySNMPInfo()
        else:      
            detallesRouter = outAndConrol.querySNMPInfo(r.ip) 

        ultimo = outAndConrol.verifyLastVersion(r.archivo)
        arch = r.archivo

    except r.DoesNotExist:
        raise Http404("Agente no encontrado!")
    finally:
        context = {'detallesRouter':detallesRouter}

        context.update({"file":str(arch)})
        context.update({'last':str(ultimo)})

    return render(request,'adminlte/verRouters.html', message = "Helo" )


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
        ip = str(request.POST['IP'])
        config_file = request.FILES['config-file']
        #type(config_file)
        fs = FileSystemStorage(location='assets/')
        if not fs.exists:
            print("Tes")
            filename = fs.save(config_file.name, config_file)
            uploaded_file_url = fs.url(config_file)

        tosend = fs.open(config_file.name,"rb")


        ret = outAndConrol.uploadConfigFile(tosend,ip)
        #fs.path()
        #print(str(fs.base_location()))
        if ret == 0:
            messages.success(request, 'Archivo '+config_file.name+" fue conigurado correctamente")
            # Atualiza registro bd
            
            dicRout = ConfigurationAdmin.querySNMPInfo(ip)
            
            rout = Router.objects.get(pk=ip)
            rout.hostname = dicRout['hostname']
            rout.version = dicRout['version']
            rout.puerto = dicRout['port']
            rout.os = dicRout['os']
            rout.interfaces = dicRout['interfaces']
            rout.ubicacion = dicRout['location']
            rout.contactto = dicRout['contact']
            # LLenar mascara y gateway
            rout.save()

        else:
            messages.error(request, "No fue posible  conigurar el archivo de manera correcta")
        return render(request, 'adminlte/configArchivos.html')
    elif request.method == 'GET':
        return render(request,"'adminlte/configArchivos.html")
def bajarArchivoConf(request):

    if request.method == 'GET':
        return render(request,'adminlte/descargaArchivo.html')
        
    elif request.method == 'POST':
        print(request.POST['IP'])
        ip = str(request.POST['IP'])
        res = outAndConrol.downloadConfigFile(ip)
        print(res.name)
        dictiona = {"nothing":""}
        messages.success(request, 'Archivo '+res.name+" descargado con éxito")
        print("Guardando la informacion en la bd")

        if ip == outAndConrol.getway:
            di = outAndConrol.querySNMPInfo()
        
        else:
            r = Router.objects.get(pk=ip)
            di = outAndConrol.querySNMPInfo(ip)

        
        return render(request,'adminlte/descargaArchivo.html',context=dictiona)
        

    


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


