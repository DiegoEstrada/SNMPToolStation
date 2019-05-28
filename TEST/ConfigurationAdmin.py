import re
import subprocess

class ConfigurationAdmin(object):
    #_ip = None              #string X.X.X.X/Y
    #_getway = None          #string X.X.X.X
    #_routerNetwork = None   #Dic {ip,fileConfig} 
    #_interface = None       #string tapX


    def __init__(self,ip,getway,routerNetwork,interface=None):
        print("CONSTRUCTOR")
        self.ip = ip
        self.getway = getway
        self.routeNetwork = routerNetwork
        if interface is None:
            generaTap()
            #self.interface = "tap0"
        else:
            self.interface = interface

    def __str__(self):
        return str("Agente con direccion IP "+ self.ip + "con interfaz "+self.interface)
    

    def verifyConnection(self):
        """Ping al getway configurado con las reglas"""
        pass
    
    def generateTap(self):
        """Crea y configura una nueva Tap para ser usada"""
        pass

    def downloadConfigFile():
        """Realiza la descarga del archivo de configuracion
            del router via FTP y almacena la info en la BD"""
        pass
    
    def uploadConfigFile():
        """Actualiza el archivo de configuracion del router"""
        pass
    