#Python application to upload recorded sensor values to Plotly site.
import plotly.plotly as py
import json
import time
import datetime
from subprocess import Popen, PIPE
from plotly.graph_objs import *
import csv
import sys
import socket


#Check connection, Check if CSV is available, read CSV, append data to Plotly, back-up file

def is_connected():
  REMOTE_SERVER = "www.google.com"
  #Popen('sudo sakis3g connect APN="internet" APN_USER="user" APN_PASS="pass"', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Checking"', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 32', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "connection"', shell=True)
  time.sleep(0.25)
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


def PlotlyUpload():
  with open('./config.json') as config_file:
    plotly_user_config = json.load(config_file)

  py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])

  f = open('weightTempdata.txt')
  csv_f = csv.reader(f)
  CSVtimeDate = []
  CSVWeight = []
  CSVTemp = []
  for row in csv_f:
     CSVtimeDate.append(row[0])
     CSVWeight.append(row[1])
     CSVTemp.append(row[2])
  f.close()

  trace1 = Scatter(
        x=CSVtimeDate,
        y=CSVWeight,
        mode='markers',
        name='Weight'
  )


  trace2 = Scatter(
        x=CSVtimeDate,
        y=CSVTemp,
        mode='markers',
        name='Temp(c)'
  )



  data = Data([trace1, trace2]) 

  layout = Layout(
    title='Logged temperature and weight',
    xaxis=XAxis(
        title='Time',
        titlefont=Font(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=YAxis(
        title='Sensors',
        titlefont=Font(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
  )

 # Make figure object
  fig = Figure(data=data, layout=layout)

  #ToDo: Insert loggerID into recording, reading from config file
  url = py.plot(fig, filename='Weight and temperature recordings loggedTest2:', fileopt='extend')

  #ToDo: Only move if sucessfully sent
  Popen('sudo mv /home/pi/weightTempdata.txt /home/pi/dataBup/`date +%Y%m%d_%H%M`weightTempdata.txt', shell=True)

  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Data uploaded"', shell=True)  
  time.sleep(2)

if is_connected() ==False:
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "No connection"', shell=True)
    time.sleep(2)
    Popen('sudo python /home/pi/menu.py dlTopSelect.mnu', shell=True) 
    sys.exit()

elif is_connected() ==True:
    PlotlyUpload()
#Popen('sudo sakis3g disconnect', shell=True)
#Popen('sudo python /home/pi/menu.py dlTopSelect.mnu', shell=True)
#sys.exit()
