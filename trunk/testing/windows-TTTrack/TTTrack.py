import pyttsx
import serial
from Tkinter import *

#usage of text to speech engine:
#engine = pyttsx.init()
#engine.say('45.7 kilometres per hour')
#engine.say('60 kilometres per hour.')
#engine.runAndWait()

#scan() returns the [(number,portstr), ...] of each available port

#need to asyn monitor serial port 
#http://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
#http://code.activestate.com/recipes/82965-threads-tkinter-and-asynchronous-io/
#http://matteolandi.blogspot.ie/2012/06/threading-with-tkinter-done-properly.html

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
    ports = tuple([port for num, port in scan()]) 
    return ports if len(ports) > 0 else tuple(["No Ports"])


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()
        
        self.current_port = StringVar(frame)
        available_ports = generatePortsTuple()
        self.serialports = OptionMenu(frame, self.current_port, *generatePortsTuple(), command=self.updateSerialPort)
        self.serialports.pack(side=LEFT)
        
        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.speech_enabled = IntVar()
        self.speechOnOff = Checkbutton(frame, text="Talk", variable=self.speech_enabled, command=self.speechChanger)
        self.speechOnOff.pack(side=LEFT)

    def speechChanger(self):
        #may not be necessary
        print self.speech_enabled.get()
    
    def updateSerialPort(self, portselection):
        print portselection
        print self.current_port.get()

#the following runs main application loop
root = Tk()
root.title("Table Tennis Track")
root.geometry("450x200")
app = App(root)
root.mainloop()
