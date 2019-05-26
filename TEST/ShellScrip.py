import re
import subprocess

#Simple way to execute Shell commands
#os.system("ls -la")

#However subprocess module provides more powerful facilities for spawning new processes;

sp = subprocess.Popen("tunctl -u diego",stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)

bytesoutput = sp.communicate()[0]
output = bytesoutput.decode("utf-8")
tapVariable = re.findall("\'.+\'",output)
retval = sp.wait()

if( retval >= 0):
    print ((tapVariable[0]))



#subprocess.run(["ls", "-l"]) 

