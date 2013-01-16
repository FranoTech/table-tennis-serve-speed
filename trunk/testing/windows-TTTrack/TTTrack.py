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
 
def generatePortsTuple():
    return tuple([port for num, port in scan()])

from Tkinter import *

class App:

    on = False
    

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()
        
        self.current_port = StringVar(frame)
        available_ports = generatePortsTuple()
        self.serialports = OptionMenu(frame, self.current_port, *generatePortsTuple(), command=self.updateSerialPort)
        self.serialports.pack(side=LEFT)
        
        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Talk", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        self.on = not self.on
        print "On" if self.on else "Off"
    
    def updateSerialPort(self, portselection):
        print portselection
        print self.current_port


#run main application loop
root = Tk()
app = App(root)
root.mainloop()
