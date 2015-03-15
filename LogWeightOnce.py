import time
import datetime
import sys
import ConfigParser
from subprocess import Popen, PIPE
#import subprocess
#from BitWizard.bw import *  # Import SPI and device classes

def dataLogging():
    #Open Log File
    f=open('tempdata.txt','a')
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y/%m/%d,%H:%M:%S")
    cowName = cow()

    config = ConfigParser.ConfigParser()
    config.read("/home/pi/config.ini")
    pipe1 = Popen('sudo ./2readADC', shell=True, stdout=PIPE).stdout
    weight = pipe1.read()
#    .communicate()
#    exit_code = weight.wait()
    cmd = ['sudo sh /home/pi/showTemp.sh']
    pipe2 = Popen(cmd, shell=True, stdout=PIPE).stdout
    temperature = pipe2.read()
    outstring = str(timestamp)+","+weight+ ","+temperature+"\n"
    f.write(outstring)
    f.close()

    print outstring
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)   
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Recorded"', shell=True)
    time.sleep(2)
    Popen('sudo python /home/pi/menu.py dlTopSelect.mnu', shell=True)
    sys.exit()

dataLogging()
