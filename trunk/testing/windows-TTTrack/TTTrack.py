#!python2.7
# -*- coding: utf-8 -*-

"""
Author: Fergal O Grady
E-mail: fergalogrady@gmail.com
This application communicates with an arduino attached to two custom light gates
It receives the time in microseconds and calculates speed based on distance travelled / time

"""

from Tkinter import Tk, W, E, StringVar, IntVar
from ttk import Frame, Button, Label, Style, OptionMenu, Checkbutton
from ttk import Entry
import serial
import pyttsx
import struct
import thread
import threading
import Queue



#Serial Port Communication Thread
#######################################

#thread safe one element queue
serial_data = Queue.Queue(1)

lo = threading.Lock()
thread_exit = threading.Event()

def SerialMonitorThread(port):
    ser = serial.Serial(port,9600)
    while not lo.locked():
        if ser.read() == 'H':
            answer = struct.unpack('I', ser.read(4))[0]
        if ser.read() == 'E':
            serial_data.put(answer)
    ser.close()
    thread_exit.set()
    thread.exit()

#Serial Port Utility Functions
#########################################

def scanPorts():
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
    ports = tuple([port for num, port in scanPorts()]) 
    return ports if len(ports) > 0 else tuple(["No Ports"])


#Calculate Speeed based on microseconds and distance
#############################################

def calc_speed(microseconds, distance_in_m):
    #1m/s = 3.6 km/h
    return ( float(distance_in_m) * 3.6 ) / (float(microseconds) * float(10 ** -6) )


#Main application
#############################################


class App(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initVar()
        self.initUI()
        self.engine = pyttsx.init()
        self.readSensor()
    
    def initVar(self):
        self.status_text = StringVar(self)
        self.status_text.set("Initializing")

        self.available_ports = generatePortsTuple()
        self.current_port = StringVar(self)
        self.current_port.set(self.available_ports[0])
        
        if self.current_port.get() == "No Ports":
          self.status_text.set("No Sensor")
        else:
          thread.start_new_thread(SerialMonitorThread, (self.current_port.get(),))
          self.status_text.set("Awaiting reading")

        self.input_distance = StringVar(value="0.6")
        self.speech_enabled = IntVar(value=1)

    def initUI(self):
    
      self.parent.title("Table Tennis Speed Tracker")

      Style().configure("TMenubutton", padding=(5, 0, 5, 0), 
          font='serif 10')

      self.columnconfigure(0, pad=5)
      self.columnconfigure(1, pad=5)
      self.columnconfigure(2, pad=5)
      self.columnconfigure(3, pad=5)
      
      self.rowconfigure(0, pad=3)
      self.rowconfigure(1, pad=3)
      
      self.statusBar = Label(self,
                        font='Helvetica 50',
                        foreground="#E8E8E8",
                        background="#A31919",
                        textvariable=self.status_text,
                        
                        )
      self.statusBar.grid(row=0, columnspan=4, sticky=W+E)
      
      self.serialPortList = OptionMenu(self,
                                      self.current_port,
                                      self.current_port.get(),
                                      *self.available_ports,
                                      command=self.updateSerialPort
                                      )
      self.serialPortList.grid(row=1, column=0)
      #print self.serialPortList.winfo_class()

      self.distanceLabel = Label(self,
                                 text="Distance (m):",
                                 padding=(10,0,0,0)
                            )
      self.distanceLabel.grid(row=1, column=1, sticky=E) 

      self.distanceEntry = Entry(self,
                                 textvariable=self.input_distance)   
      self.distanceEntry.grid(row=1, column=2, sticky=W)

      self.speechButton = Checkbutton(self, 
                                      text="Speak Results",
                                      variable=self.speech_enabled,
                                      padding=(10,0,5,0)
                                      )
      self.speechButton.grid(row=1, column=3)       
      
      self.pack()

    def updateSerialPort(self, port_choice):
      #stop current serial Monitor Thread and start new one for selected port. 
      if not self.status_text.get() == "No Sensor":
        lo.acquire(True)
        thread_exit.wait()
        lo.release()
        if self.current_port.get() == "No Ports":
          self.status_text.set("No Sensor")
        else:
          thread.start_new_thread(SerialMonitorThread, (self.current_port.get(),))
          self.status_text.set("Awaiting reading")
        thread_exit.clear()
        

    def readSensor(self):
      if serial_data.full():
        speed = '{0:.2f}'.format(calc_speed(serial_data.get(), self.input_distance.get()))
        self.status_text.set( speed + ' km/h')
        serial_data.task_done()
        self.update()
        if self.speech_enabled.get():
          self.engine.say(speed + " kilometres per hour")
          self.engine.runAndWait()
      self.after(50, self.readSensor)

def main():
  
    root = Tk()
    app = App(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  