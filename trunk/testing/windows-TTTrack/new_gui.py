#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
New UI for Tkinter TTTrack App
"""

from Tkinter import Tk, W, E, StringVar, IntVar
from ttk import Frame, Button, Label, Style, OptionMenu, Checkbutton
from ttk import Entry


#Serial Port Utility Functions
#########################################
import serial

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

#############################################

class App(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initVar()
        self.initUI()
    
    def initVar(self):
        self.statusText = StringVar(self)
        self.statusText.set("Initializing")
        self.available_ports = generatePortsTuple()
        self.current_port = StringVar(self)
        self.current_port.set(self.available_ports[0])
        self.speech_enabled = IntVar(value=1)

    def initUI(self):
      
        self.parent.title("Table Tennis Speed Tracker")
        
        Style().configure("TButton", padding=(0, 5, 0, 5), 
            font='serif 10')
        
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        
        self.statusBar = Label(self,
                          font='Helvetica 48',
                          foreground="#E8E8E8",
                          background="#A31919",
                          textvariable=self.statusText,
                          
                          )
        self.statusBar.grid(row=0, columnspan=4, sticky=W+E)
        
        self.serialPortList = OptionMenu(self,
                                        self.current_port,
                                        self.current_port.get(),
                                        *self.available_ports
                                        )
        self.serialPortList.grid(row=1, column=0)

        self.distanceLabel = Label(self,
                                   text="Distance (m):"
                              )
        self.distanceLabel.grid(row=1, column=1) 

        self.distanceEntry = Entry(self)   
        self.distanceEntry.grid(row=1, column=2) 

        self.speechButton = Checkbutton(self, 
                                        text="Talk",
                                        variable=self.speech_enabled
                                        )
        self.speechButton.grid(row=1, column=3)       
        
        self.pack()

def main():
  
    root = Tk()
    app = App(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  