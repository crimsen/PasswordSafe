'''
Created on 18.06.2015

@author: groegert
'''

from gui.EmptyPage import EmptyPage
from gui.EmptyPage import EmptyPageContext
from gui.EmptyPage import EmptyPageController
from gui.EmptyPage import EmptyPageView
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class GuiPage(EmptyPage):
    '''
    classdocs
    '''


    def __init__(self, parent, context):
        '''
        Constructor
        '''
        self.view = GuiPageView(parent)
        self.controller = GuiPageController(self.view, context)
    def setModel(self, model):
        self.controller.setModel(model)
        self.view.updateFromModel(model)

class GuiPageContext(EmptyPageContext):
    def __init__(self, option):
        EmptyPageContext.__init__(self, option)

class GuiPageView(EmptyPageView):
    def __init__(self, parent):
        self.__buildFrame__(parent)
    def __buildFrame__(self, parent):
        self.autolockVar = tk.IntVar();
        self.frame = tk.Frame(master=parent)
        self.autolock = tk.Checkbutton(master=self.frame,text='Lock User Interface automatically', variable=self.autolockVar)
        autolockFrame = tk.Frame(master=self.frame)
        self.autolockLabel = tk.Label(master=autolockFrame, text='Delay in Seconds:')
        self.autolockSeconds = tk.Spinbox(master=autolockFrame, from_=0, to=3600)
        self.frame.pack(side='top', fill='both', expand=True)
        self.autolock.pack(side='top', anchor='nw')
        autolockFrame.pack(side='top', fill='x', padx=["10m",0])
        self.autolockLabel.pack(side='left')
        self.autolockSeconds.pack(side='left')

    def updateModel(self, model):
        autolock = 0
        if self.autolockEnabled:
            autolock = int(self.autolockSeconds.get())
        model.autolock = autolock

    def updateFromModel(self, model):
        self.autolockValue = model.autolock
        self.autolockEnabled = 0 != self.autolockValue
        self.updateWidgets()

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

class GuiPageController(EmptyPageController):
    def __init__(self, view, context):
        EmptyPageController.__init__(self, view, context)
        self.view.autolock.configure(command=self.onToggleAutolock)
    def apply(self):
        self.view.updateModel(self.model)
        
    def onToggleAutolock(self):
        view = self.view
        autolock = view.autolockVar.get()
        view.autolockEnabled = 0 != autolock
        if 0 != autolock:
            # currently we do not have a saved value for autolock
            # so on switching on set it to default 60
            if 0 == view.autolockValue:
                view.autolockValue = 60
        view.updateWidgets()
