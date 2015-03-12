#Python application to stream sensor data to Plotly.
import plotly.plotly as py
import json
import time
import datetime
from subprocess import Popen, PIPE
from plotly.graph_objs import *
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


with open('./config.json') as config_file:
    plotly_user_config = json.load(config_file)

py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])

trace1 = Scatter(
    x=[],  # init. data lists
    y=[], 
    mode='markers',
    name='Weight',                             
    stream=Stream(
        token=plotly_user_config['plotly_streaming_tokens'][1],
        maxpoints=200 
    )
)


trace2 = Scatter(
    x=[],  # init. data lists
    y=[],    
    mode='markers',
    name='Temp(c)', 
    stream=Stream(
        token=plotly_user_config['plotly_streaming_tokens'][2],
        maxpoints=200       
    )
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

url = py.plot(fig, filename='Weight and temperature recordings loggedTest2:', fileopt='extend')


s1 = py.Stream(plotly_user_config['plotly_streaming_tokens'][1])
s2 = py.Stream(plotly_user_config['plotly_streaming_tokens'][2])
s1.open()
s2.open()

weight=0.0
temp= 0.0
Button=""
#the main sensor reading and plotting loop
while Button[:2]!='82':
    pipe1 = timeout_command('sudo ./2readADC', 0.5)
    if pipe1 >0.0:
        weight=pipe1
    s1.write({'x': datetime.datetime.now(), 'y': weight})
    pipe2 = Popen('sudo sh showTempExternal.sh', shell=True, stdout=PIPE).stdout
    #If temperature is registered under 0 deg, use previous temp
    y1 = pipe2.read()
    if float(y1) >= 0:
        temp = y1
    s2.write({'x': datetime.datetime.now(), 'y': temp})

    pipe3 = Popen('sudo bw_tool -a 94 -I -D /dev/i2c-1 -R 30:b', shell=True, stdout=PIPE).stdout
    Button = pipe3.read()
    WeightScreen = 'sudo bw_tool -I -D /dev/i2c-1 -a 94 -t '+'"'+str(weight)+'"'
    TempScreen = 'sudo bw_tool -I -D /dev/i2c-1 -a 94 -t '+'"'+str(temp)+'"'
    #Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 16 -v 0', shell=True)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
    Popen(WeightScreen, shell=True)
    time.sleep(0.1)
    Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 32', shell=True)
    Popen(TempScreen, shell=True)
    # delay between stream posts
    time.sleep(0.15)
