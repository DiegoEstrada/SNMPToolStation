import SnmpGet 
import time
import rrdtool
import os

"""Class to steect possible failures in CPU RAM and HD"""
OIDRAM = "1.3.6.1.4.1.2021.4.6.0"
#__OIDCPU = "1.3.6.1.4.1.2021.11.9.0"
OIDCPU = "1.3.6.1.2.1.25.3.3.1.2.1281"
OIDHD = "1.3.6.1.2.1.25.2.3.1.6.6"


	

def prediccionCPU():

	rrdtool.dump("assets/source3.rrd",'assets/salida.xml"')
	
	while 1:
		tiempo_final = int(rrdtool.last("assets/source3.rrd"))
		tiempo_inicial = 1539659123


		time.sleep(1)
		ret = rrdtool.graphv("assets/RES.png",
                         "--start",str(tiempo_inicial),
                         "--end",str(tiempo_final+5000),
                        "--title","Carga de CPU",
                         "--vertical-label=Uso de la CPU (%)",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                         "DEF:carga=assets/source3.rrd:CPUload:AVERAGE",
                         
                         
                         "CDEF:umbral90=carga,90,LT,0,carga,IF",
                         
                         
                         "VDEF:cargaMAX=carga,MAXIMUM",
                         "VDEF:cargaMIN=carga,MINIMUM",
                         "VDEF:cargaSTDEV=carga,STDEV",
                         "VDEF:CPUavg=carga,AVERAGE",
                         "VDEF:CPUlast=carga,LAST",
                         "AREA:carga#00FF00:Uso de CPU entre 0% y 25%",
                         
                         
                         "AREA:umbral90#FF1900:Uso mayor de 90%",
                         
                         "HRULE:90#FF1900:",
                         "PRINT:cargaMAX:%6.2lf %S",
                         
                         "GPRINT:cargaMIN:%6.2lf %SMIN",
                         "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                         "GPRINT:CPUlast:%6.2lf %SLAST",



                         "COMMENT:Now          Min             Avg             Max",
                         "GPRINT:CPUlast:%12.0lf%s",
                         "GPRINT:cargaMIN:%10.0lf%s",
                         "GPRINT:CPUavg:%13.0lf%s",
                         "GPRINT:cargaMAX:%13.0lf%s",
                         "VDEF:m=carga,LSLSLOPE",
                         "VDEF:b=carga,LSLINT",
                         'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                         "CDEF:limite=tendencia,85,100,LIMIT",
                         "VDEF:primer=limite,FIRST",
                         "PRINT:primer:'Supera en '%Y\:%d\:%A\:%H\:%M\:%S:strftime",
                         "GPRINT:primer:%Y\:%d\:%A\:%H\:%M\:%S:strftime",
                         "LINE2:tendencia#000000" 


                          )
		#ATENCION -> 
		#Si se desea ver solo los recuadros quitar todas las lineas despues de los espacios en la linea 75
		#y quitar una coma al GPRINT
		
		ultimo_valor=float(ret['print[0]'])
		noultimo_valor=(ret['print[1]'])
		#print("Maximo -> "+str(ultimo_valor))
		print(noultimo_valor)


		
			

		
		
	

def main():
	
	#trend.iniciarArchivos()
	prediccionCPU()
	#trend.prediccionHD()
	#trend.prediccionHD()

if __name__ == '__main__':
	main()