import SnmpGet 
import time
import rrdtool
import os

carga_CPU = 0

rrdpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pngpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rrdname = "trend.rdd"



def iniciar():
    #print(rrdpath)
    ret = rrdtool.create(rrdpath+"/"+rrdname,
                     "--start",'N',
                     "--step",'10',
                     "DS:CPUload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:24")
    #print(ret)


def prediccionCPU():
    umbralCP1 = False
    umbralCP2 = False
    umbralCP3 = False
    while 1:

        tiempo_final = int(rrdtool.last(rrdpath+"/"+rrdname))
        tiempo_inicial = tiempo_final - 600


        carga_CPU = int(SnmpGet.consultaSNMP('gr_4cm3','localhost',161,2,'1.3.6.1.2.1.25.3.3.1.2.196608'))
        valor = "N:" + str(carga_CPU)
        print (valor)
        ret=rrdtool.update(rrdpath+"/"+rrdname, valor)
        #rrdtool.dump(rrdpath+ rrdname,'trend.xml')
        time.sleep(1)
        #print("Graphing")


        ret = rrdtool.graph( pngpath+"/trend.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Carga CPU",
                     "--title=Uso de CPU",
                     "--color", "ARROW#009900",
                     '--vertical-label', "Uso de CPU (%)",
                     '--lower-limit', '0',
                     '--upper-limit', '100',
                     "DEF:carga="+rrdpath+"/"+rrdname+":CPUload:AVERAGE",
                     "AREA:carga#00FF00:Carga CPU",
                     "LINE1:30",
                     "AREA:5#ff000022:stack",
                     "VDEF:CPUlast=carga,LAST",
                     "VDEF:CPUmin=carga,MINIMUM",
                     "VDEF:CPUavg=carga,AVERAGE",
                     "VDEF:CPUmax=carga,MAXIMUM",

                    "COMMENT:Now          Min             Avg             Max",
                     "GPRINT:CPUlast:%12.0lf%s",
                     "GPRINT:CPUmin:%10.0lf%s",
                     "GPRINT:CPUavg:%13.0lf%s",
                     "GPRINT:CPUmax:%13.0lf%s",
                     "VDEF:m=carga,LSLSLOPE",
                     "VDEF:b=carga,LSLINT",
                     'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                    "LINE2:tendencia#FFBB00" )


        ret = rrdtool.graphv( pngpath+"deteccion.png",
                         "--start",str(tiempo_inicial),
                         "--end",str(tiempo_final),
                        "--title","Carga de CPU",
                         "--vertical-label=Uso de la CPU (%)",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                         "DEF:carga="+rrdpath+"/"+rrdname+":CPUload:AVERAGE",
                         "CDEF:umbral25=carga,25,LT,0,carga,IF",
                         "CDEF:umbral40=carga,40,LT,0,carga,IF",
                         "CDEF:umbral55=carga,55,LT,0,carga,IF",
                         "VDEF:cargaMAX=carga,MAXIMUM",
                         "VDEF:cargaMIN=carga,MINIMUM",
                         "VDEF:cargaSTDEV=carga,STDEV",
                         "VDEF:CPUavg=carga,AVERAGE",
                         "VDEF:CPUlast=carga,LAST",
                         "AREA:carga#00FF00:Uso de CPU entre 0% y 25%",
                         "AREA:umbral25#236CE0:Uso de CPU entre 26% y 40%",
                         "AREA:umbral40#FFFF02:Uso de CPU entre 41% y 55%",
                         "AREA:umbral55#FF1900:Uso de CPU entre 41% y 55%",
                         "HRULE:25#236CE0:",
                         "HRULE:40#FFFF02:",
                         "HRULE:55#FF1900:",
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
                         "LINE2:tendencia#000000" 
                          )

        """ATENCION -> 
                Si se desea ver solo los recuadros quitar todas las lineas despues de los espacios en la linea 98
                y quitar una coma al GPRINT 
        """
        ultimo_valor=float(ret['print[0]'])

        if (ultimo_valor>25 and not umbralCP1):
            print("Sobrepasa Primer Umbral ")
            umbralCP1 = True
        
        if (ultimo_valor > 40 and not umbralCP2):
            print("Sobrepasa Primer Umbral ")
            umbralCP2 = True

        if (ultimo_valor > 55 and not umbralCP3):
            print("Sobrepasa Primer Umbral ") 
            umbralCP3 = True  

            

def main():
    iniciar()
    prediccionCPU()

if __name__ == '__main__':
    main()

