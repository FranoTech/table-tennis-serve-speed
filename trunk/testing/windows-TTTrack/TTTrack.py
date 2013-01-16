import pyttsx
import serial

#usage of text to speech engine:
#engine = pyttsx.init()
#engine.say('45.7 kilometres per hour')
#engine.say('60 kilometres per hour.')
#engine.runAndWait()

#scan() returns the [(number,portstr), ...] of each available port



def scan():
   # scan for available ports. return a list of tuples (num, name)
   available = []
   for i in range(256):
       try:
           s = serial.Serial(i)
           available.append( (i, s.portstr))
           s.close()
       except serial.SerialException:
           pass
   return available
   

