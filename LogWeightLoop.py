#Python application for writing sensor values to file. Written by Simon Fraval.
#Based on use with Raspberry Pi and Bitwizard RPI_UI.
import time
import datetime
import sys
from subprocess import Popen, PIPE
#import subprocess
#from BitWizard.bw import *  # Import SPI and device classes
import signal
import os

def timeout_command(command, timeout):
    #import subprocess, datetime, os, time, signal
    start = datetime.datetime.now()
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    while process.poll() is None:
      time.sleep(0.1)
      now = datetime.datetime.now()
      if (now - start).seconds> timeout:
        os.kill(process.pid, signal.SIGKILL)
        os.waitpid(-1, os.WNOHANG)
        return None
    return process.stdout.read()

weight = "0.0"
temp = "0.0"
def dataLogging():
    #Open weight log file
    if weight > 0:
        weight=weight
    else:
        global weight
    if temp > 0:
        temp=temp
    else:
        global temp
    f=open('weightTempdata.txt','a')
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    pipe1 = timeout_command('sudo ./2readADC', 1)
    if pipe1 >0.0:
        weight=pipe1
    pipe2 = Popen('sudo sh showTempExternal.sh', shell=True, stdout=PIPE).stdout
    #If temperature is registered under 0 deg, use previous temp
    y1 = pipe2.read()
    if float(y1) >= 0:
        #Get the first 5 characters of the temp readout
        temp = y1[:5]
    outstring = timestamp+","+weight+","+temp+"\n"
    print (outstring)
    f.write(outstring)
    f.close()

    WeightScreen = 'sudo bw_tool -I -D /dev/i2c-1 -a 94 -t '+'"Weight: '+str(weight)+'"'
    TempScreen = 'sudo bw_tool -I -D /dev/i2c-1 -a 94 -t '+'"Temp: '+str(temp)+'"'
    #Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 16:0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
    Popen(WeightScreen, shell=True)
    time.sleep(0.1)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 32', shell=True)
    Popen(TempScreen, shell=True)

#Run the loop

Button=""
while Button[:2]!='82':
    dataLogging()
    pipe3 = Popen('sudo bw_tool -a 94 -I -D /dev/i2c-1 -R 30:b', shell=True, stdout=PIPE).stdout
    Button = pipe3.read()
    # delay between data entries
    time.sleep(0.15)
