import rrdtool
from path import *
tiempo_final = int(rrdtool.last(rrdpath+"trend.rrd"))
tiempo_inicial = tiempo_final - 3600


ret = rrdtool.graphv( pngpath+"deteccion.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                    "--title","Carga de CPU",
                     "--vertical-label=Uso de CPU (%)",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                     "DEF:carga="+rrdpath+rrdname+":CPUload:AVERAGE",
                     "CDEF:umbral25=carga,25,LT,0,carga,IF",
                     "CDEF:umbral40=carga,40,LT,0,carga,IF",
                     "CDEF:umbral55=carga,55,LT,0,carga,IF",
                     "VDEF:cargaMAX=carga,MAXIMUM",
                     "VDEF:cargaMIN=carga,MINIMUM",
                     "VDEF:cargaSTDEV=carga,STDEV",
                     "VDEF:cargaLAST=carga,LAST",
                     "AREA:carga#00FF00:Carga del CPU",
                     "AREA:umbral25#FAFF00:Tráfico de carga mayor que 25",
                     "AREA:umbral40#FF9F00:Tráfico de carga mayor que 40",
                     "AREA:umbral55#FF1900:Tráfico de carga mayor que 55",
                     "HRULE:25#00FF50:Umbral 1 - 25%",
                     "HRULE:40#0090FF:Umbral 26 - 40%",
                     "HRULE:55#E100FF:Umbral 41 - 55%",
                     "PRINT:cargaMAX:%6.2lf %S",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST" )
#print (ret)
#print(ret.keys())
#print(ret.items())

ultimo_valor=float(ret['print[0]'])

if ultimo_valor>23:
    print("Sobrepasa Umbral línea base")


def main():
    


if __name__ == '__main__':
    main()