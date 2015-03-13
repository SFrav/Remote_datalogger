#!/usr/local/bin/python
import csv
import json
import requests
from subprocess import Popen
import sys
import socket
import time

#Check internet connection, parse to JSON, HTTP post then exit to main menu.

def is_connected():
  REMOTE_SERVER = "www.google.com"
  Popen('sudo sakis3g connect APN="safaricom" APN_USER="saf" APN_PASS="data"', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Checking"', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 32', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "connection"', shell=True)
  time.sleep(2)
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

def parseJSONpost():
  # Open the CSV  
  f = open( '/home/pi/weightTempdata.txt', 'rU' )
  reader = csv.DictReader( f, fieldnames = ( "LoggerID","Date","Time","HHID","Animal", "tare","Weight","Temperature")) 
  # Parse the CSV into JSON  
  out = json.dumps( [ row for row in reader ] )
  print "JSON parsed!"
  # Save the JSON  
  f = open( '/home/pi/Upload.json', 'w')
  f.write(out)
  print "JSON saved!"
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)   
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Loading"', shell=True)
  print out

  post_data = out

  r = requests.post('http://some.server/services/logging', post_data, auth=('user', 'pass'))

  print r.status_code
  print r.headers['content-type']
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)

  if r.status_code == 200:
      Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
      Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Data sent"', shell=True)
      Popen('sudo mv /home/pi/tempdata.txt /home/pi/dataBup/`date +%Y%m%d_%H%M`weightTempdata.txt', shell=True)
      time.sleep(3)

  elif r.status_code == 404:
      Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
      Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Upload failed"', shell=True)
      time.sleep(3)

if is_connected() ==False:
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "No connection"', shell=True)
    time.sleep(2)
#    Popen('sudo python /home/pi/menu.py dlTopSelect.mnu', shell=True) 
    sys.exit()

elif is_connected() ==True:
    parseJSONpost()
Popen('sudo sakis3g disconnect', shell=True)
Popen('sudo python /home/pi/menu.py dlTopSelect.mnu', shell=True)
sys.exit()

