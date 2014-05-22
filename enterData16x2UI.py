#!/usr/local/bin/python
import sys
import tty
import termios
from subprocess import Popen

Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)

def getch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
     tty.setraw(sys.stdin.fileno())
     ch = sys.stdin.read(1)
  finally:
     termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

char = ""
while True:
# Temp file to store the cow names to overwrite later
  f=open('data.txt','a')
  char = char + getch()
  lastchar = char[-1]
  charpass = char[:-1]+"'"

#Backspace - removes last letter
  if (lastchar == "\x7f"):
      char = char[:-2]

# save name to file with tab or enter
  if (lastchar == "+"): #replace char
      f.write ("'"+ charpass+"\n")
      f.close()  
      char = ""
      Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
      Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Ok"', shell=True)
      time.sleep(1)

#  Exit and save with esc
  if (lastchar == u"\u001b"):
      f.close()
      #Replace file - change dir to required
      Popen('sudo cp data.txt /home/pi/', shell=True)
      Popen('sudo rm data.txt', shell=True)
      #Clear screen     
      Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
	  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Saved"', shell=True)
      time.sleep(2)
      break

# option to exit completely without saving. 
  if (lastchar == "-"): #replace char with something?
      Popen('sudo rm data.txt', shell=True)
	  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -t "Cancelled"', shell=True)
      time.sleep(2)
	  break

  cmd = 'sudo bw_tool -I -D /dev/i2c-1 -a 94 -t " '
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -w 10:0', shell=True)
  Popen('sudo bw_tool -I -D /dev/i2c-1 -a 94 -r 17 -v 0', shell=True)
  Popen(cmd + char +'"', shell=True)

