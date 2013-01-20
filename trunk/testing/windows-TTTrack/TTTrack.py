import pyttsx
import serial
import struct
import thread
import Queue
from time import sleep
from Tkinter import *


#Tk tutorials
#http://www.tkdocs.com/tutorial/index.html

serial_data = Queue.Queue(1)

#Serial Port Communication Thread
#######################################

def SerialMonitorThread(port):
    ser = serial.Serial(port,9600)
    while(1):
        if ser.read() == 'H':
            answer = struct.unpack('I', ser.read(4))[0]
        if ser.read() == 'E':
            serial_data.put(answer)

#Serial Port Utility Functions
#########################################

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
    #returns ('COMX','COMY', ... or ('No Ports',)
    ports = tuple([port for num, port in scan()]) 
    return ports if len(ports) > 0 else tuple(["No Ports"])


class App:
    
    def __init__(self, master):

        self.frame = Frame(master)
        self.frame.pack()
        
        self.sbartext = StringVar(self.frame)
        self.current_port = StringVar(self.frame)
        self.speech_enabled = IntVar(value=1)
        
        #Setup serial ports / options
        
        self.current_port.set(generatePortsTuple()[0])
        
        if self.current_port.get() == "No Ports":
          self.sbartext.set("No Sensor")
        else:
          thread.start_new_thread(SerialMonitorThread, (self.current_port.get(),))
          self.sbartext.set("Awaiting reading")
          
        # Set up serial port option menu
        
        self.serialports = OptionMenu(self.frame, 
                                      self.current_port, 
                                      *generatePortsTuple(), 
                                      command=self.updateSerialPort
                                      )
        self.serialports.pack(side=LEFT)

        #Text to speech on/off button
        self.engine = pyttsx.init()
        
        self.speechOnOff = Checkbutton(self.frame, 
                                        text="Talk when new speed detected",
                                        variable=self.speech_enabled
                                        )
        self.speechOnOff.pack(side=LEFT)

        #Exit Button
        self.button = Button(self.frame, 
                              text="QUIT", 
                              fg="red", 
                              command=self.frame.quit
                              )
        self.button.pack(side=RIGHT)

        #Status bar setup
        self.sbarframe = Frame(master)
        self.sbarlabel = Label(self.sbarframe,
                                       bd = 1,
                                       relief = SUNKEN,
                                       anchor = W,
                                       bg = "red",
                                       textvariable = self.sbartext,
                                       font=("Helvetica", 64)
                                       )
        self.sbarframe.pack(side = BOTTOM, fill = X)
        self.sbarlabel.pack(fill = X)
        
        #Start reading sensor values
        self.readSensor()

    
    def readSensor(self):
        if serial_data.full():
                self.sbartext.set(str(serial_data.get()))
                serial_data.task_done()
                self.frame.update()
                if self.speech_enabled.get():
                    self.engine.say(self.sbartext.get() + " kilometres per hour")
                    self.engine.runAndWait()
        self.frame.after(50, self.readSensor)
    
    def updateSerialPort(self, portselection):
        #this does nothing yet but should restart serial port thread with new port
        print portselection
        print self.current_port.get()

#Main application loop set up and run
#######################################

root = Tk()
root.title("Table Tennis Speed Tracker")
root.geometry("680x145")
app = App(root)
root.mainloop()

########################################