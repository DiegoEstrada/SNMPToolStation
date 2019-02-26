import shutil, os
from threading import Thread
import time

def main():
     print ("hello world	")
     t = Thread(target=copyDJANGO, args=(1,))
     t.start()




def copyDJANGO(i):
	#ruta = os.getcwd() + os.sep
	origen = '/home/diego/Documents/Administracion de Servicios en Red/Examen1/AdministracionRedSNMP/assets/Agentes.txt'
	destino =  '/home/diego/Documents/Administracion de Servicios en Red/Examen1/AdministracionRedSNMP/staticfiles/Agentes.txt'
	while True :
		
		if os.path.exists(origen):
		    with open(origen, 'rb') as forigen:
		        with open(destino, 'wb') as fdestino:
		            shutil.copyfileobj(forigen, fdestino)
		            print("Archivo copiado")
		            time.sleep(5)


if __name__ == '__main__':
	main()
	pass

