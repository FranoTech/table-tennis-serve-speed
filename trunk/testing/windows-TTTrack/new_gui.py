#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
New UI for Tkinter TTTrack App
"""

from Tkinter import Tk, W, E, StringVar, IntVar
from ttk import Frame, Button, Label, Style, OptionMenu, Checkbutton
from ttk import Entry


class App(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Calculator")
        
        Style().configure("TButton", padding=(0, 5, 0, 5), 
            font='serif 10')
        
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        
        
        self.statusText = StringVar(self)
        self.statusText.set("Testing")
        self.statusBar = Label(self,
                          
                          font='serif 15',
                          background="red",
                          textvariable=self.statusText,
                          
                          )
        self.statusBar.grid(row=0, columnspan=4, sticky=W+E)

        self.current_port = StringVar(self)
        self.serialPortList = OptionMenu(self,
                                        self.current_port,
                                        'Port',
                                        *('Port1','Port2')
                                        )
        self.serialPortList.grid(row=1, column=0)


        self.distanceLabel = Label(self,
                               text="Distance (m):"
                              )
        self.distanceLabel.grid(row=1, column=1) 

        self.distanceEntry = Entry(self)   
        self.distanceEntry.grid(row=1, column=2) 

        self.speech_enabled = IntVar(value=1)
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