from . import SnmpGet 
from . import views
import time
import rrdtool
import os
import tempfile

"""Class to steect possible failures in CPU RAM and HD"""
OIDRAM = "1.3.6.1.4.1.2021.4.6.0"
OIDCPU = "1.3.6.1.4.1.2021.11.9.0"
#Examen usado OIDCPU = "1.3.6.1.2.1.25.3.3.1.2.1281"
OIDHD = "1.3.6.1.2.1.25.2.3.1.6.6"
OIDINTRAFFIC = "1.3.6.1.2.1.2.2.1.10.1"
dicUmbrales = {'CPU1':0}

class Thrend:
	

	def __init__(self, hostname,versionSNMP,puerto,comunidad,idAgente):
		"""idAgente nos permite generar un archivo rrd, png o xml unico para cada agente registrado en la bd mysql"""
		self.hostname = hostname
		self.versionSNMP = versionSNMP
		self.puerto = puerto
		self.comunidad = comunidad
		self.idAgente = idAgente
		
		

	def iniciarArchivos(self):
		retCPU = rrdtool.create("assets/"+self.idAgente+"CPU.rdd",
                     "--start",'N',
                     "--step",'10',
                     "DS:CPUload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:600")
		retRAM = rrdtool.create("assets/"+self.idAgente+"RAM.rdd",
                     "--start",'N',
                     "--step",'10',
                     "DS:RAMload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:600")

		retHD = rrdtool.create("assets/"+self.idAgente+"HD.rdd",
                     "--start",'N',
                     "--step",'10',
                     "DS:HDload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:600")		

		# greater alpha/beta ---> last values are important
		# lower alpha/beta --> historical values are important
		retNL = rrdtool.create("assets/"+self.idAgente+"NL.rdd",
						"--start",'N',
						"--step",'5',
						"DS:inoctets:COUNTER:600:U:U",
						"RRA:AVERAGE:0.5:1:2016",
					#RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
						"RRA:HWPREDICT:30:0.1:0.0035:10:3",
					#RRA:SEASONAL:seasonal period:gamma:rra-num
						"RRA:SEASONAL:10:0.1:2",
					###### GRAPH USING AVERAGE, TEST AND SEASONAL FOR TESTING ######
					#RRA:DEVSEASONAL:seasonal period:gamma:rra-num
						"RRA:DEVSEASONAL:10:0.1:2",
					#RRA:DEVPREDICT:rows:rra-num
						"RRA:DEVPREDICT:30:4",
					#RRA:FAILURES:rows:threshold:window length:rra-num
						"RRA:FAILURES:10:5:7:4")
					
					#HWPREDICT rra-num is the index of the SEASONAL RRA.
					#SEASONAL rra-num is the index of the HWPREDICT RRA.
					#DEVPREDICT rra-num is the index of the DEVSEASONAL RRA.
					#DEVSEASONAL rra-num is the index of the HWPREDICT RRA.
					#FAILURES rra-num is the index of the DEVSEASONAL RRA.



	def prediccionCPU(self):
		umbralCP1 = False
		umbralCP2 = False
		umbralCP3 = False
		
		while 1:
			tiempo_final = int(rrdtool.last("assets/"+self.idAgente+"CPU.rdd"))
			tiempo_inicial = tiempo_final - 600

			carga_CPU = int(SnmpGet.consultaSNMP(self.comunidad,self.hostname,self.puerto,self.versionSNMP,OIDCPU))
			valor = "N:" + str(carga_CPU)
			#print (valor) #DESCOMENTAR PARA VER VALORES SENSADOS
			ret=rrdtool.updatev("assets/"+self.idAgente+"CPU.rdd", valor)
			#rrdtool.dump(rrdpath+ rrdname,'trend.xml')
			time.sleep(1)
			ret = rrdtool.graphv("assets/"+self.idAgente+"CPU.png",
	                         "--start",str(tiempo_inicial),
	                         "--end",str(tiempo_final),
	                        "--title","Carga de CPU",
	                         "--vertical-label=Uso de la CPU (%)",
	                        '--lower-limit', '0',
	                        '--upper-limit', '100',
	                         "DEF:carga=assets/"+self.idAgente+"CPU.rdd:CPUload:AVERAGE",
							 
	                         "CDEF:umbral19=carga,19,LT,0,carga,IF",
	                         "CDEF:umbral24=carga,24,LT,0,carga,IF",
	                         "CDEF:umbral30=carga,30,LT,0,carga,IF",

							

	                         "VDEF:cargaMAX=carga,MAXIMUM",
	                         "VDEF:cargaMIN=carga,MINIMUM",
	                         "VDEF:cargaSTDEV=carga,STDEV",
	                         "VDEF:CPUavg=carga,AVERAGE",
	                         "VDEF:CPUlast=carga,LAST",

							 
	                         "AREA:carga#00FF00:Uso de CPU entre 0% y 19%",
	                         "AREA:umbral19#236CE0:Uso de CPU entre 20% y 24%",
	                         "AREA:umbral24#FFFF02:Uso de CPU entre 25% y 30%",
	                         "AREA:umbral30#FF1900:Uso de CPU mayor de 30 %",
	                         "HRULE:19#236CE0:",
	                         "HRULE:24#FFFF02:",
	                         "HRULE:30#FF1900:",
	                         "PRINT:cargaMAX:%6.2lf %S",
							 "GPRINT:cargaMAX:%6.2lf %S MAX",
	                         "GPRINT:cargaMIN:%6.2lf %S MIN",
	                         #"GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
	                         #"GPRINT:CPUlast:LAST %6.2lf %S",

	                         "GPRINT:CPUavg:%6.2lf %S AVG",
	                         
	                         "VDEF:m=carga,LSLSLOPE",
	                         "VDEF:b=carga,LSLINT",
	                         "CDEF:tendencia=carga,POP,m,COUNT,*,b,+",

							 "LINE2:tendencia#000000",

							 "CDEF:limite3=tendencia,30,50,LIMIT",
                         	 "VDEF:primer=limite3,FIRST",
                         	 "PRINT:primer:Tendencia a fallar el %A %d de %B del %Y a las %H\:%M\:%S:strftime",
                         	 "GPRINT:primer: Tendencia a fallar el %A %d de %B del %Y a las %H\:%M\:%S:strftime"

	                          )
	

			ultimo_valor=float(ret['print[0]'])
			tendencia = ret['print[1]']
			print("Tendencia -> "+tendencia)

			if (ultimo_valor> 19 and not umbralCP1):
				print("Sobrepasa Primer Umbral LOCAL")
				views.logging.info("La CPU supero el primer umbral READY")
				#views.sendEmail("jorgecast29@gmail.com","Evidencia 3","Equipo 10 grupo 4CM3\n Umbral 1 Superado")
				umbralCP1 = True
				#return 1

			if (ultimo_valor> 24 and not umbralCP2):
				print("Sobrepasa Segundo Umbral")
				views.logging.info("La CPU supero el segundo umbral SET")
				#views.sendEmail("jorgecast29@gmail.com","Evidencia 3","Equipo 10 grupo 4CM3\n Umbral 2 Superado")
				umbralCP2 = True
				#return 2

			if (ultimo_valor> 30 and not umbralCP3):
				print("Sobrepasa Tercer Umbral")
				views.logging.info("La CPU supero el tercer umbral GO")
				#views.sendEmail("jorgecast29@gmail.com","Evidencia 3","Equipo 10 grupo 4CM3\n Umbral 3 Superado")
				umbralCP3 = True
				#return 3


	

	def prediccionRAM(self):
		umbralRAM1 = False
		umbralRAM2 = False
		umbralRAM3 = False
		while 1:
			tiempo_final = int(rrdtool.last("assets/"+self.idAgente+"RAM.rdd"))
			tiempo_inicial = tiempo_final - 600

			carga_RAM = int(SnmpGet.consultaSNMP(self.comunidad,self.hostname,self.puerto,self.versionSNMP,OIDRAM))
			valor = "N:" + str(carga_RAM)
			print (valor)
			ret=rrdtool.update("assets/"+self.idAgente+"RAM.rdd", valor)
			#rrdtool.dump(rrdpath+ rrdname,'trend.xml')
			time.sleep(1)
			ret = rrdtool.graphv("assets/"+self.idAgente+"RAM.png",
	                         "--start",str(tiempo_inicial),
	                         "--end",str(tiempo_final),
	                        "--title","Estado de la memoria RAM",
	                         "--vertical-label=Memoria RAM Disponible",
	                        '--lower-limit', '0',
	                        '--upper-limit', '600000',
	                         "DEF:carga=assets/"+self.idAgente+"RAM.rdd:RAMload:AVERAGE",
	                         "CDEF:umbral1=carga,250000,GT,0,carga,IF",
	                         "CDEF:umbral2=carga,100000,GT,0,carga,IF",
	                         "CDEF:umbral3=carga,75000,GT,0,carga,IF",
	                         "VDEF:cargaMAX=carga,MAXIMUM",
	                         "VDEF:cargaMIN=carga,MINIMUM",
	                         "VDEF:cargaSTDEV=carga,STDEV",
	                         "VDEF:RAMavg=carga,AVERAGE",
	                         "VDEF:RAMlast=carga,LAST",
	                         "AREA:carga#00FF00:Entre 6 a 2.5 GB RAM Disponible",
	                         "AREA:umbral1#236CE0:Entre 2.5 a 1 GB RAM Disponible",
	                         "AREA:umbral2#FFFF02:Entre 1 GB a 750 MB RAM Disponible ",
	                         "AREA:umbral3#FF1900:Menos de 750 MB de RAM Disponible",
	                         "HRULE:250000#236CE0:",
	                         "HRULE:100000#FFFF02:",
	                         "HRULE:75000#FF1900:",
	                         "PRINT:cargaMAX:%6.2lf %S",
							"GPRINT:cargaMAX:%6.2lf %S MAX",
	                         "GPRINT:cargaMIN:%6.2lf %S MIN",
	                         #"GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
	                         #"GPRINT:RAMlast:LAST %6.2lf %S",

	                         "GPRINT:RAMavg:%6.2lf %S AVG",
	                         
	                         "VDEF:m=carga,LSLSLOPE",
	                         "VDEF:b=carga,LSLINT",
	                         "CDEF:tendencia=carga,POP,m,COUNT,*,b,+",

							"LINE2:tendencia#000000",

							"CDEF:limite3=tendencia,55000,75000,LIMIT",
                         	 "VDEF:primer=limite3,FIRST",
                         	 "PRINT:primer:Tendencia a fallar el %A %d de %B del %Y a las %H\:%M\:%S:strftime",
                         	 "GPRINT:primer: Tendencia a fallar el %A %d de %B del %Y a las %H\:%M\:%S:strftime"
	                          )
			#ATENCION -> 
			#Si se desea ver solo los recuadros quitar todas las lineas despues de los espacios en la linea 75
			#y quitar una coma al GPRINT

			if ( ret['print[0]'].find("k") != -1):
				ultimo_valor=float(ret['print[0]'].split(".")[0])*1000
			else:
				ultimo_valor=float(ret['print[0]'])

			print(ultimo_valor)

			if (ultimo_valor< 250000 and not umbralRAM1):
				print("Sobrepasa Primer Umbral ")
				umbralRAM1 = True

			if (ultimo_valor< 100000 and not umbralRAM2):
				print("SObrepasa Segundo Umbral")
				umbralRAM2 = True

			if (ultimo_valor< 75000 and not umbralRAM3):
				print("Sobrepasa Tercer Umbral")
				umbralRAM3 = True



	def prediccionHD(self):
			umbralHD1 = False
			umbralHD2 = False
			umbralHD3 = False
			while 1:
				tiempo_final = int(rrdtool.last("assets/"+self.idAgente+"HD.rdd"))
				tiempo_inicial = tiempo_final - 600

				carga_RAM = int(SnmpGet.consultaSNMP(self.comunidad,self.hostname,self.puerto,self.versionSNMP,OIDHD))
				valor = "N:" + str(carga_RAM)
				print (valor)
				ret=rrdtool.update("assets/"+self.idAgente+"HD.rdd", valor)
				#rrdtool.dump(rrdpath+ rrdname,'trend.xml')
				time.sleep(1)
				ret = rrdtool.graphv("assets/"+self.idAgente+"HD.png",
		                         "--start",str(tiempo_inicial),
		                         "--end",str(tiempo_final),
		                        "--title","Estado del Disco Duro",
		                         "--vertical-label=Memoria Disponible",
		                        '--lower-limit', '0',
		                        '--upper-limit', '160000',
		                         "DEF:carga=assets/"+self.idAgente+"HD.rdd:HDload:AVERAGE",
		                         "CDEF:umbralHD1=carga,142000,GT,0,carga,IF",
		                         "CDEF:umbralHD2=carga,132000,GT,0,carga,IF",
		                         "CDEF:umbralHD3=carga,120000,GT,0,carga,IF",
		                         "VDEF:cargaMAX=carga,MAXIMUM",
		                         "VDEF:cargaMIN=carga,MINIMUM",
		                         "VDEF:cargaSTDEV=carga,STDEV",
		                         "VDEF:HDavg=carga,AVERAGE",
		                         "VDEF:HDlast=carga,LAST",
		                         "AREA:carga#00FF00:Más de 16 GB Disponibles en DD",
		                         "AREA:umbralHD1#236CE0:Entre 15.9 a 15.5 GB en DD",
		                         "AREA:umbralHD2#FFFF02:Entre 15.4 a 15 GB en DD  %",
		                         "AREA:umbralHD3#FF1900:Menos  15 GB EN DD",
		                         "HRULE:142000#236CE0:",
		                         "HRULE:132000#FFFF02:",
		                         "HRULE:120000#FF1900:",
		                         "PRINT:cargaMAX:%6.2lf %S",
								 "GPRINT:cargaMAX:%6.2lf %S MAX",
	                         	 "GPRINT:cargaMIN:%6.2lf %S MIN",
	                        	 #"GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
	                         	 #"GPRINT:HDlast:LAST %6.2lf %S",

		                         "GPRINT:HDavg:%6.2lf %S AVG",
	                         
	                        	 "VDEF:m=carga,LSLSLOPE",
	                        	 "VDEF:b=carga,LSLINT",
	                         	 "CDEF:tendencia=carga,POP,m,COUNT,*,b,+",

								 "LINE2:tendencia#000000",

								 "CDEF:limite3=tendencia,110000,120000,LIMIT",
                         	 	 "VDEF:primer=limite3,FIRST",
                         	  	 "PRINT:primer:Tendencia a fallar el %A %d de %B del %Y a las %H\:%M\:%S:strftime",
                         	 	 "GPRINT:primer: Tendencia a fallar el %A %d de %B del %Y a las %H\:%M\:%S:strftime"
		                        )

				if ( ret['print[0]'].find("k") != -1):
					ultimo_valor=float(ret['print[0]'].split(".")[0])*1000
				else:
					ultimo_valor=float(ret['print[0]'])

				print(ultimo_valor)

				if (ultimo_valor< 142000 and not umbralHD1):
					print("Sobrepasa Primer Umbral ")
					umbralHD1 = True

				if (ultimo_valor< 132000 and not umbralHD2):
					print("SObrepasa Segundo Umbral")
					umbralHD2 = True

				if (ultimo_valor< 120000 and not umbralHD3):
					print("Sobrepasa Tercer Umbral")
					umbralHD3 = True



	
	def prediccionNoLineal(self):
		#title="Comportamiento anomalo, Alpha 0.1 Beta 0.0035"
		title = "Comportamiento anomalo, Proyeccion No Lineal"
		while 1:
			tiempo_final = int(rrdtool.last("assets/"+self.idAgente+"NL.rdd"))
			tiempo_inicial = tiempo_final - 600

			input_traffic = int(SnmpGet.consultaSNMP(self.comunidad,self.hostname,self.puerto,self.versionSNMP,OIDINTRAFFIC))
			valor = "N:" + str(input_traffic)
			#print (valor)
			ret=rrdtool.update("assets/"+self.idAgente+"NL.rdd", valor)
			#rrdtool.dump(rrdpath+ rrdname,'trend.xml')
			time.sleep(1)

			# ---- UNCOMMENT TO FUCK UP THE APPLICATION :D ----
			#print (check_aberration("assets/",self.idAgente+"NL.rdd"))
			
			# Changes alpha/beta/gamma value, useful under specific situations. verify functionallity 
            #rrdtool.tune(loc, '--alpha', '0.1')
			ret = rrdtool.graph(
				"assets/"+self.idAgente+"NL.png",
				'--start', str(tiempo_inicial), '--end', str(tiempo_final), '--title=' + title,
				"--vertical-label=Bytes/s",
				#'--slope-mode',
				"DEF:obs=" + "assets/"+self.idAgente+"NL.rdd" + ":inoctets:AVERAGE",
				#"DEF:outoctets=" + loc + ":outoctets:AVERAGE",
				"DEF:pred=" + "assets/"+self.idAgente+"NL.rdd" + ":inoctets:HWPREDICT",
				"DEF:dev=" + "assets/"+self.idAgente+"NL.rdd" + ":inoctets:DEVPREDICT",
				"DEF:fail=" + "assets/"+self.idAgente+"NL.rdd" + ":inoctets:FAILURES",

				#"RRA:DEVSEASONAL:1d:0.1:2",
				#"RRA:DEVPREDICT:5d:5",
				#"RRA:FAILURES:1d:7:9:5""
				"CDEF:scaledobs=obs,8,*",
				"CDEF:upper=pred,dev,2,*,+",
				"CDEF:lower=pred,dev,2,*,-",
				"CDEF:scaledupper=upper,8,*",
				"CDEF:scaledlower=lower,8,*",
				"CDEF:scaledpred=pred,8,*",
				"TICK:fail#FDD017:1.0:Fallas",
				"LINE3:scaledobs#00FF00:In traffic",
				"LINE1:scaledpred#FF00FF:Prediccion\\n",
				#"LINE1:outoctets#0000FF:Out traffic",
				"LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
				"LINE1:scaledlower#0000FF:Lower Bound Average bits in"
			)

			
			# It may be a good idea to call check_aberration() 
			# in order to send email to the admin after graphing 
			# if there is a return value of 1 or 2



	# ---- UNCOMMENT TO FUCK UP THE APPLICATION :D x2 ----
	"""def check_aberration(rrdpath, fname):
     This will check for begin and end of aberration
        in file. Will return:
        0 if aberration not found.
        1 if aberration begins
        2 if aberration ends
    
    ab_status = 0
    rrdfilename = rrdpath + fname

    info = rrdtool.info(rrdfilename)
    #print(info['filename'])
    rrdstep = int(info['step'])
    #print(rrdstep)
    lastupdate = info['last_update']
    previosupdate = str(lastupdate - rrdstep - 1)
    graphtmpfile = tempfile.NamedTemporaryFile()
    # Ready to get FAILURES  from rrdfile
    # will process failures array values for time of 2 last updates
    values = rrdtool.graph(graphtmpfile.name+'F',
                           'DEF:f0=' + rrdfilename + ':inoctets:FAILURES:start=' + previosupdate + ':end=' + str(lastupdate),
                           'PRINT:f0:MIN:%1.0lf',
                           'PRINT:f0:MAX:%1.0lf',
                           'PRINT:f0:LAST:%1.0lf')
    print (values)
    fmin = int(values[2][0])
    fmax = int(values[2][1])
    flast = int(values[2][2])
    print ("fmin="+fmin+", fmax="+fmax+",flast="+flast)
    # check if failure value had changed.
    if (fmin != fmax):
        if (flast == 1):
            ab_status = 1
        else:
            ab_status = 2
    return ab_status"""


"""
def main():
	trend = Thrend('localhost',2,161,'gr_4cm3','DiegoEG')
	trend.iniciarArchivos()
	trend.prediccionHD()

if __name__ == '__main__':
	main()
    
"""