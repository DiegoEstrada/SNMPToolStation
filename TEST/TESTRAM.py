import SnmpGet 
import time
import rrdtool
import os

v = '751.86 k'
a = float(v.split(".")[0])
print(a)


ret = rrdtool.create("TESTRAM.rdd",
                     "--start",'N',
                     "--step",'10',
                     "DS:RAMload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:24")

while 1:
	tiempo_final = int(rrdtool.last("TESTRAM.rdd"))
	tiempo_inicial = tiempo_final - 600
	carga_CPU = int(SnmpGet.consultaSNMP('gr_4cm3','localhost',161,2,'1.3.6.1.2.1.25.2.3.1.6.6'))
	valor = "N:" + str(carga_CPU)
	print (valor)
	ret=rrdtool.update("TESTRAM.rdd", valor)
	time.sleep(1)
	