import rrdtool
import tempfile

def check_aberration(f):
    """This will check for begin and end of aberration
        in file. Will return:
        0 if aberration not found.
        1 if aberration begins
        2 if aberration ends
    """
    ab_status = 0
    infoFail={}
    rrdfilename = f

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

