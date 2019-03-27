#from path import *
import rrdtool
import time
import datetime
from getSNMP import consultaSNMP
import tempfile
import sys
#from Notify import check_aberration

total_input_traffic = 0
#total_input_traffic = int(consultaSNMP('gr_4cm3','localhost','1.3.6.1.2.1.2.2.1.10.1'))

rrdpath = '/home/jorge/Escritorio/Trend-Non-Linear/'
pngpath = '/home/jorge/Escritorio/Trend-Non-Linear/'
rrdname= "netP.rrd"
pngfname="predictNLHistoric.png"
f = rrdpath + rrdname
png = pngpath + pngfname
title="Comportamiento anomalo, Alpha 0.1 Beta 0.0035"


def iniciarArchivo():
    # greater alpha/beta ---> last values are important
    # lower alpha/beta --> historical values are important
    ret = rrdtool.create(f,
                     "--start",'N',
                     "--step",'10',
                     "DS:inoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:30",
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
                     "RRA:FAILURES:20:5:7:4")

                
                


def predicInOctets():
        print("Inicia prediccion no lineal...")
        rrdtool.dump(f,'predHistoric.xml')
        #sys.exit(0)
        while 1:
            endDate = rrdtool.last(f) #ultimo valor del XML
            begDate = endDate - 50000
            InicioAyer=begDate - 86400
            FinAyer=endDate - 86400

            total_input_traffic = int(consultaSNMP('gr_4cm3','localhost','1.3.6.1.2.1.2.2.1.10.1'))
            total_output_traffic = int(consultaSNMP('gr_4cm3','localhost','1.3.6.1.2.1.2.2.1.16.1'))
            info = rrdtool.info(f) # RETURNS A DICTIONARY
            #print(info)
            #print("info['last_update']", info['last_update']) <--- LAST UPDATE VALUE
            #valor = str(info['last_update'] + 1) + ":" + str(total_input_traffic) + ":" + str(total_output_traffic)
            """
            CAMBIAR EL VALOR DE 180 PARA UN DESPLAZAMIENTO MAS RÁPIDO DE LA GRAFICA O QUITAR EL VALOR PARA QUE VAYA CONFORME
            AL STEP
            """
            valor = str(rrdtool.last(f) + 180) + ":" + str(total_input_traffic) + ":" + str(total_output_traffic)
            #valor = "N" + ":" + str(total_input_traffic) + ":" + str(total_output_traffic)
            print ("In Traffic:",valor, " bytes/s")
            ret = rrdtool.update(f, valor)
            #rrdtool.dump(f,'RRD/predHistoric.xml')
            time.sleep(0.5)
            print (check_aberration(rrdpath,rrdname))

            # Changes alpha/beta/gamma value, useful under specific situations. verify functionallity 
            #rrdtool.tune(f, '--alpha', '0.1')

            ret = rrdtool.graph(png,
                        '--start', str(begDate), '--end', str(endDate), '--title=' + title,
                        "--vertical-label=Bytes/s",
                        '--slope-mode',
                        "DEF:obs=" + f + ":inoctets:AVERAGE",
                        "DEF:obsAyer=" + f + ":inoctets:AVERAGE:start=" + str(InicioAyer) + ":end=" + str(FinAyer),
                        "DEF:pred=" + f + ":inoctets:HWPREDICT",
                        "DEF:dev=" + f + ":inoctets:DEVPREDICT",
                        "DEF:fail=" + f + ":inoctets:FAILURES",
                        "SHIFT:obsAyer:86400",

                    #"RRA:DEVSEASONAL:1d:0.1:2",
                    #"RRA:DEVPREDICT:5d:5",
                    #"RRA:FAILURES:1d:7:9:5""
                        "CDEF:scaledobs=obs,8,*",
                        "CDEF:scaledobsAyer=obsAyer,8,*",
                        "CDEF:upper=pred,dev,2,*,+",
                        "CDEF:lower=pred,dev,2,*,-",
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=pred,8,*",
                        "VDEF:FALLA1=fail,FIRST",
                        "VDEF:FALLA2=fail,LAST",
                    "TICK:fail#FDD017:1.0: Fallas",
                    "AREA:scaledobsAyer#9C9C9C:Ayer",
                    "LINE3:scaledobs#00FF00:In traffic",
                    "LINE1:scaledpred#FF00FF:Prediccion",
                    #"LINE1:outoctets#0000FF:Out traffic",
                    "LINE1:scaledupper#ff0000:Upper Bound Average bits in",
                    "LINE1:scaledlower#0000FF:Lower Bound Average bits in")
                    #"PRINT:FALLA1:'Val 1 '%Y\:%d\:%A\:%H\:%M\:%S:strftime",
                    #"PRINT:FALLA1",
                    #"PRINT:FALLA2:'Val 2 '%Y\:%d\:%A\:%H\:%M\:%S':strftime")
            #print(ret)
            

               


def check_aberration(rrdpath, fname):
    """This will check for begin and end of aberration
        in file. Will return:
        0 if aberration not found.
        1 if aberration begins
        2 if aberration ends
    """
    ab_status = 0
    infoFail={}
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
                           'PRINT:f0:MAX:%1.0lf' ,
                           'PRINT:f0:LAST:%1.0lf',
                           "VDEF:list=f0,LAST",
                           "PRINT:list:%Y\:%d\:%A\:%H\:%M\:%S:strftime")
    #print (values)
    fmin = int(values[2][0])
    fmax = int(values[2][1])
    flast = int(values[2][2])
    date = str(values[2][3])
    #print ("fmin="+str(fmin)+", fmax="+str(fmax)+",flast="+str(flast) + ", date=" + date)
    # check if failure value had changed.
    if (fmin != fmax):
        if (flast == 1):
            ab_status = 1
            infoFail['status'] = ab_status
            infoFail['date'] = date
        else:
            ab_status = 2
            infoFail['status'] = ab_status
            infoFail['date'] = date
    infoFail['status'] = ab_status
    infoFail['date'] = date
    return infoFail


def main():
    #iniciarArchivo()
    predicInOctets()


if __name__ == "__main__":
    main()
