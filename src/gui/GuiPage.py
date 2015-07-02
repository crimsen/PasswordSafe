'''
Created on 18.06.2015

@author: groegert
'''

from OptionPage import OptionPage
import Tkinter as tk

class GuiPage(OptionPage):
    '''
    classdocs
    '''


    def __init__(self, parent, option):
        '''
        Constructor
        '''
        OptionPage.__init__(self, parent, option)

    def __buildFrame__(self, parent):
        self.autolockVar = tk.IntVar();
        self.frameMain = tk.Frame(master=parent)
        self.autolock = tk.Checkbutton(master=self.frameMain,text='Lock User Interface automatically', variable=self.autolockVar, command=self.onToggleAutolock)
        autolockFrame = tk.Frame(master=self.frameMain)
        self.autolockLabel = tk.Label(master=autolockFrame, text='Delay in Seconds:')
        self.autolockSeconds = tk.Spinbox(master=autolockFrame, from_=0, to=3600)
        self.frameMain.pack(side='top', fill='both', expand=True)
        self.autolock.pack(side='top', anchor='nw')
        autolockFrame.pack(side='top', fill='x', padx=["10m",0])
        self.autolockLabel.pack(side='left')
        self.autolockSeconds.pack(side='left')

    def readFromOption(self):
        '''
        reads values from the option object and sets the ui according to the values
        '''
        self.autolockValue = self.option.autolock
        self.autolockEnabled = 0 != self.autolockValue

    def updateWindow(self):
        '''
        prepares the window with possible settings and updates the ui
        '''
        self.readFromOption()
        self.updateWidgets()

    def apply(self):
        autolock = 0
        if self.autolockEnabled:
            autolock = int(self.autolockSeconds.get())
        self.option.autolock = autolock

    def updateWidgets(self):
        autolock = self.autolockEnabled
        if autolock:
            self.autolock.select()
            self.autolockLabel.configure(state='normal')
            self.autolockSeconds.configure(state='normal')
            self.autolockSeconds.delete(0, 'end')
            self.autolockSeconds.insert('end', self.autolockValue)
        else:
            self.autolock.deselect()
            self.autolockSeconds.delete(0, 'end')
            self.autolockSeconds.insert('end', self.autolockValue)
            self.autolockLabel.configure(state='disabled')
            self.autolockSeconds.configure(state='disabled')

    def onToggleAutolock(self):
        autolock = self.autolockVar.get()
        self.autolockEnabled = 0 != autolock
        if 0 != autolock:
            # currently we do not have a saved value for autolock
            # so on switching on set it to default 60
            if 0 == self.autolockValue:
                self.autolockValue = 60
        self.updateWidgets()
