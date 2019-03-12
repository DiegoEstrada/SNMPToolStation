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
                     "--step",'60',
                     "DS:CPUload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:24")
    #print(ret)


def graficar():
    while 1:

        tiempo_final = int(rrdtool.last(rrdpath+"/"+rrdname))
        tiempo_inicial = tiempo_final - 3600


        carga_CPU = int(SnmpGet.consultaSNMP('gr_4cm3','localhost',161,2,'1.3.6.1.2.1.25.3.3.1.2.196608'))
        valor = "N:" + str(carga_CPU)
        print (valor)
        ret=rrdtool.update(rrdpath+"/"+rrdname, valor)
        #rrdtool.dump(rrdpath+ rrdname,'trend.xml')
        time.sleep(1)
        print("Graphing")


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
                         "--vertical-label=Uso de CPU (%)",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                         "DEF:carga="+rrdpath+"/"+rrdname+":CPUload:AVERAGE",
                         "CDEF:umbral25=carga,25,LT,0,carga,IF",
                         "VDEF:cargaMAX=carga,MAXIMUM",
                         "VDEF:cargaMIN=carga,MINIMUM",
                         "VDEF:cargaSTDEV=carga,STDEV",
                         "VDEF:cargaLAST=carga,LAST",
                         "AREA:carga#00FF00:Carga del CPU",
                         "AREA:umbral25#FF9F00:Tráfico de carga mayor que 25",
                         "HRULE:25#FF0000:Umbral 1 - 25%",
                         "PRINT:cargaMAX:%6.2lf %S",
                         "GPRINT:cargaMIN:%6.2lf %SMIN",
                         "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                         "GPRINT:cargaLAST:%6.2lf %SLAST" )
        ultimo_valor=float(ret['print[0]'])

        if ultimo_valor>23:
            print("Sobrepasa Umbral línea base")

def main():
    iniciar()
    graficar()


if __name__ == '__main__':
    main()

