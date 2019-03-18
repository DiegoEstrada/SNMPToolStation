from monitor.models import Agent
from monitor.Thrend import Thrend
from monitor.Grafica import Grafica
import logging
import os
import time

logging.basicConfig(filename='monitor/snmpTool.log',format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
graphs = []
thrends = []

class Invoker(object):

    __instance = None
    

    def __str__(self):
        return 'Just self  '

    def __new__(cls):
        if Invoker.__instance is None:
            Invoker.__instance = object.__new__(cls)
            print("=== Invoker started ===")
            logging.info("Invoker Creado" )
        
        return Invoker.__instance


    def getAgentsAvailable():
        print("Agentes Registrados \n")
        agents = Agent.objects.all()
        li = []
        d = {}
        for agent in agents:
            d['name'] = agent.name
            d['hostname'] = agent.hostname
            d['version'] = agent.version
            d['puerto'] = agent.puerto
            d['grupo'] = agent.grupo ##ESTO ME CAGO PARA ENCONTRARLO IBA PUERTO :,(
            d['email'] = agent.email
            li.append(d)
        
        return li

    def startA(self):

        agentsList = Invoker.getAgentsAvailable()

        for agent in agentsList:
            name = agent.get('name')
            hostname = agent.get('hostname')
            version = int(agent.get('version'))
            port = int(agent.get('puerto'))
            group = agent.get('grupo')
            email = agent.get('email')

            print("Agent ->" +str(name) + " IP -> "+str(hostname)+" Group -> "+str(group))
            logging.info("Agente Detectectado "+ str(name) + " " +str(hostname)+"  "+str(group))
            grafica = Grafica(hostname,version,port,group,name)
            thrend = Thrend(hostname,version,port,group,name)

            graphs.append(grafica)
            thrends.append(thrend)

        print("=== Agent-Graphs Relationchip Succesfull ===")


        print("=== Starting RRD tool Graphing ===")

        for graph in graphs:
            Invoker.lanzarGrafica(1,graph) ##Trafico de Red
            #Invoker.lanzarGrafica(2,graph) ##ICMP
            #Invoker.lanzarGrafica(3,graph) ##Segmentos TCP
            #Invoker.lanzarGrafica(4,graph) ## Datagramas IP
            #Invoker.lanzarGrafica(5,graph) ## Respuestas PING

        print("=== Graphing all Agents at current Time ===")

        print("=== Starting Thrend Prediction ===")
        

        
        #trend.iniciarArchivos()
        #lanzarProyecciones("CPU",trend)

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
        
        
