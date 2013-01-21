import pyttsx
import serial
import struct
import thread
import Queue
from time import sleep
from Tkinter import *


#Tk tutorials
#http://www.tkdocs.com/tutorial/index.html

#thread safe one element queue to hold most recent result
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

#Calculate Speeed based on microseconds and distance
#############################################

def calc_speed(microseconds, distance_in_m):
    #1m/s = 3.6 km/h
    return ( float(distance_in_m) * 3.6 ) / (float(microseconds) * float(10 ** -6) )
    
#############################################

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
                                        text="Talk",
                                        variable=self.speech_enabled
                                        )
        self.speechOnOff.pack(side=LEFT)
        
        #Distance input in metres
        self.distance = Label(self.frame,
                               text="Distance (m):"
                              )
        self.speechOnOff.pack(side=LEFT, fill=X)  
        
        self.input_dist = Entry(self.frame)
        self.input_dist.pack(side=LEFT)
        self.input_dist.insert(0, "0.6")

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
                speed = '{0:.2f}'.format(calc_speed(serial_data.get(), self.input_dist.get()))
                self.sbartext.set( speed + ' km/h')
                serial_data.task_done()
                self.frame.update()
                if self.speech_enabled.get():
                    self.engine.say(speed + " kilometres per hour")
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