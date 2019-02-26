from pysnmp.hlapi import *

def consultaSNMP(comunidad, host,puerto,version, oid):
    version=version-1
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad, mpModel=version),
               UdpTransportTarget((host, puerto)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB = (' = '.join([x.prettyPrint() for x in varBind]))
            resultado = varB.split()[2]
    return resultado