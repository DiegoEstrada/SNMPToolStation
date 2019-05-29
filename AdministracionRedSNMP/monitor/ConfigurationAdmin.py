import re
import subprocess
import telnetlib
from . import SnmpGet 
from ftplib import FTP

OIDHostname = "1.3.6.1.2.1.1.5.0"
VersionData = "2"
PortData = "161"
CommunityData = "gr_4cm3"
OIDOS = "1.3.6.1.2.1.1.1.0"
OIDInterfaces = "1.3.6.1.2.1.2.1.0"
OIDContact = "1.3.6.1.2.1.1.4.0"
OIDLocation = "1.3.6.1.2.1.1.6.0"
FileData = ""

class ConfigurationAdmin(object):
    #_ip = None              #string X.X.X.X/Y
    #_getway = None          #string X.X.X.X
    #_routerNetwork = None   #Dic {ip,fileConfig} 
    #_interface = None       #string tapX


    def __init__(self,ip,mask,getway,interface=None):
        print("CONSTRUCTOR")
        self.ip = ip
        self.mask = mask
        self.getway = getway
        #self.routeNetwork = routerNetwork
        if interface is None:
            self.interface = generateTap(self)
            if( addRule() == 0):
                a = 0
                #verifyConnection()
        else:
            self.interface = interface

    def __str__(self):
        return str("Agente con direccion IP "+ self.ip + " con interfaz "+self.interface)
    

    def verifyConnection(self,ip=None):
        """Ping al getway configurado con las reglas"""
        
        nvIp = ""
        if ip is None:
            nvIp = self.getway
        else:
            nvIp = ip
        print("Conectando con "+nvIp)
        png = subprocess.Popen("ping -c 8 "+nvIp,stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
        pngOutput = png.communicate()[0].decode("utf-8")
        print(pngOutput)

        #print(png.returncode)

        sentpc = re.findall("\d\%",pngOutput)
        if(int(sentpc[0][:-1])<=50):
            print("Conexion establecida")
        return png.returncode

    
    def generateTap(self):
        """Crea y configura una nueva Tap para ser usada"""
        sp = subprocess.Popen("tunctl -u diego",stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)

        bytesoutput = sp.communicate()[0]
        output = bytesoutput.decode("utf-8")
        tapVariable = re.findall("\'.+\'",output)
        retval = sp.returncode

        if( retval == 0):
            #print ((tapVariable[0]))

            
            #print(tapVariable[0])
            comand = "ifconfig " + tapVariable[0]  + " " +self.ip +"/"+self.mask+ " up"
            print("Activando la interfaz virtual "+tapVariable[0])
            #print(comand)
        
            activateVInt = subprocess.run(comand,stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
            #print(str(activateVInt.returncode))
            #responseActivateVInt = activateVInt.returncode #Podria usarse mejor wait()
            #print(responseActivateVInt)
            ifconfigVInt = subprocess.run("ifconfig " + tapVariable[0] ,stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
            #print(str(ifconfigVInt.returncode))
            if(ifconfigVInt.returncode == 0):
                print("Interfaz Creada exitosamente")

            return tapVariable[0]


    def addRule(self, netRoute):
        """Agrega reglas para permitir la comunicacion con otros routers a traves de la interfaz vietual"""
        
        
        rule = subprocess.run("route add -net  " + netRoute +" gw "+self.getway+ " dev "+ self.interface,stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
        outRule = rule.stdout.decode("utf-8")
        if(rule.returncode==0):
            print("Regla agregada con exito.\n"+ str(outRule)+"")
        else:
            print ("Error al agregar la regla ")
        
        return rule.returncode

    def downloadConfigFile(self,ip=None):
        """Realiza la descarga del archivo de configuracion
            del router via FTP y almacena la info en la BD"""
        hostToConnect = ""
        if ip is None:
            hostToConnect = self.getway
        else:
            hostToConnect = ip
            

        ftp = FTP(hostToConnect,'rcp','rcp')
        ftp.cwd('')  # cambiando al directorio donde esta el archivo de configuracion
        #ftp.retrlines('LIST') #imprimiendo un ls en el servidor FTP
        
        rutaArchivo = '/home/diego/Documents/Administracion de Servicios en Red/Examen1/AdministracionRedSNMP/assets/' +hostToConnect+ '.txt' # Ruta del archivo a subir
        startUpConfFile = 'startup-config'  # Nombre del archivo a descargar.
        localfile = open(rutaArchivo, 'wb')
        ftp.retrbinary('RETR ' + startUpConfFile, localfile.write, 1026)
        ftp.quit()
        abspath = localfile.name
        print(abspath)
        localfile.close()
        
        rule = subprocess.run("chmod 777  "+abspath,stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
        print("Archivo Descargado ")

        readFile = open(rutaArchivo, 'r')
        return readFile

    
    def uploadConfigFile(self,fielConf,ip=None):
        """Actualiza el archivo de configuracion del router"""
        hostToConnect = ""
        if ip is None:
            hostToConnect = self.getway
        else:
            hostToConnect = ip
        print("YYYYYYYYYYYYY")
        print(hostToConnect)
        ftp = FTP(hostToConnect,'rcp','rcp')
        ftp.cwd('')  # cambiando al directorio donde esta el archivo de configuracion
        #ftp.retrlines('LIST')
        #fs = FileSystemStorage(location='assets/')
        configToUpload = open('/home/diego/Desktop/CONFIGROUTER/' +hostToConnect+ '.txt','rb')
        fielConf = configToUpload
        nombreStartUp = 'startup-config'  # Nombre del archivo a actializar Inicio.
        nombreRunningUp = 'running-config'  # Nombre del archivo a actializar Inicio.
    
        ftp.storbinary('STOR ' + nombreStartUp, configToUpload)
        ftp.quit()
        print("Archivo enviado al router")

        tn = telnetlib.Telnet(hostToConnect)

        tn.read_until(b"User: ")
        tn.write(str("rcp" + "\n").encode("utf-8"))

        tn.read_until(b"Password: ")
        tn.write(str("rcp" + "\n").encode("utf-8"))
        print("Reiniciando la configuracion...")
        tn.write(str("enable  \nconfig \ncopy run start \nshow ip route \n").encode("utf-8"))
        #tn.write(b"config  \n")
        #tn.write(str("copy run start" + "\n").encode("utf-8"))
        #tn.write(b"copy run start  \n")
        #tn.write(b"exit  \n")
        #tn.write(str("show ip route \n").encode("utf-8"))
        #tn.write(b"show ip route  \n")
        #tn.write(b"show services\n")
        
        tn.close()
        #print("Hera")
        print(tn.read_sb_data().decode('utf-8'))

        print("\nCambios Aplicados al Router")
        
        return 0


    def querySNMPInfo(self, ip=None):
        """Consulta la informacion necesaria para administar el inventario"""
        dictio = {}

        hostToConnect = ""
        if ip is None:
            hostToConnect = self.getway
            dictio.update({'ip':self.ip})
        else:
            hostToConnect = ip
            dictio.update({'ip':ip})
        #dictio.update({'mask':self.mask}) #NO SE NECESITA PARA SNMP

        host = (SnmpGet.consultaSNMP('gr_4cm3',hostToConnect,161,2, OIDHostname))
        print("CONECTING TO "+hostToConnect)
        dictio.update({'hostname':str(host)})

        dictio.update({'version':VersionData})
        dictio.update({'port':PortData})
        #dictio.update({'group':GroupData})
        dictio.update({'community':CommunityData})
    

        os = (SnmpGet.consultaSNMP('gr_4cm3',hostToConnect,161,2, OIDOS))
        #print(os)
        dictio.update({'os':os})

        intrf = (SnmpGet.consultaSNMP('gr_4cm3',hostToConnect,161,2, OIDInterfaces))
        dictio.update({'interfaces':str(intrf)})

        location = (SnmpGet.consultaSNMP('gr_4cm3',hostToConnect,161,2, OIDLocation))
        dictio.update({'location':str(location)})

        contact = (SnmpGet.consultaSNMP('gr_4cm3',hostToConnect,161,2, OIDContact))
        dictio.update({'contact':str(contact)})

        #dictio.update({'file':FileData})
        
        return dictio

    def verifyLastVersion(self,contentFile):
        """Verifica si el ultimo archivo del router es igual al actual"""

        #f = open('/home/diego/Desktop/CONFIGROUTER/' +self.getway+ '.txt', "r")
        temp = open("tempo.txt","w")
        temp.write(contentFile)
        temp.close()

        f = open('tempo.txt', "r")
        lastVersion = ConfigurationAdmin.downloadConfigFile(self)
        #l = lastVersion.readable()
        for line in f:
            linea_server = line
            linea_nuevo = lastVersion.readline()
            if  linea_server == linea_nuevo:
                print("Archivos Iguales")
                #actualizar contenido en la bd
                #prender bandera de archivos diferentes
                return True
            else:
                print("Archivos distintos")
                #bandera de archivos diferentes = false
                return False
        
    