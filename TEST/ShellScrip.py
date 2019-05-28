import re
import subprocess
import  telnetlib 
#Simple way to execute Shell commands
#os.system("ls -la")

#Test ping responses
#png = subprocess.Popen("ping -c 4 192.168.0.1",stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
#pngOutput = png.communicate()[0].decode("utf-8")
#print(pngOutput)

#print(png.returncode)

#sentpc = re.findall("\d\%",pngOutput)
#if(int(sentpc[0][:-1])<=50):
#    print("Conexion establecida")

ip="192.168.203.5/24"
getway="192.168.203.15"
routerNetwork = "192.168.203.0/24" #Esto podria ser una lista para poder conectarse a las diferentes redes
archivo = open("ospf-R3.startup-config.txt","r")
#However subprocess module provides more powerful facilities for spawning new processes;
"""
print("Creando una interfaz virtual")
sp = subprocess.Popen("tunctl -u diego",stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)

bytesoutput = sp.communicate()[0]
output = bytesoutput.decode("utf-8")
tapVariable = re.findall("\'.+\'",output)
retval = sp.returncode

if( retval == 0):
    #print ((tapVariable[0]))

    
    #print(tapVariable[0])
    comand = "ifconfig " + tapVariable[0]  + " " +ip + " up"
    print("Activando la interfaz virtual "+tapVariable[0])
    #print(comand)
 
    activateVInt = subprocess.run(comand,stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
    #print(str(activateVInt.returncode))
    #responseActivateVInt = activateVInt.returncode #Podria usarse mejor wait()
    #print(responseActivateVInt)
    ifconfigVInt = subprocess.run("ifconfig " + tapVariable[0] ,stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
    #print(str(ifconfigVInt.returncode))
    if(ifconfigVInt.returncode == 0):
        print("Interfaz Creada.\nAgregando regla de conexion")
        rule = subprocess.run("route add -net  " + routerNetwork +" gw "+getway+ " dev "+ tapVariable[0],stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
        outRule = rule.stdout.decode("utf-8")
        if(rule.returncode>=0):
            print("Regla agregada con exito.\n"+ str(outRule)+"\nVerificando conectividad con el router\n")
            png = subprocess.run("ping -c 4 " + getway,stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
            pngOutput = png.stdout.decode("utf-8")
            print(pngOutput)
            sentpc = re.findall("\d\%",pngOutput)
            if(int(sentpc[0][:-1])<=50 and png.returncode == 0): #verifica paquetes perdidos
                print("\nConexion exitosa con el router a traves de "+tapVariable[0]+ "via "+getway)
            else:
                print("\nConexion fallida ")
            
"""
################Reiniciando el router via Telnet ##################

 #telnet = subprocess.Popen("telnet " + getway, stdin=subprocess.PIPE, stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, universal_newlines=True)

tn = telnetlib.Telnet(getway)

tn.read_until(b"User: ")
tn.write(str("rcp" + "\n").encode("utf-8"))

tn.read_until(b"Password: ")
tn.write(str("rcp" + "\n").encode("utf-8"))

tn.write(str("ena \nconfig \n\copy run start\nrestart \n").encode("utf-8"))
#tn.write(str("config " + "\r\n").encode("utf-8"))
#tn.write(b"restart\n")
#tn.write(str("ena \n").encode("utf-8")")

tn.close()

#print(telnetOut)



