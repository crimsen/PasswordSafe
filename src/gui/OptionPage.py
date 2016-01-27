'''
Created on May 18, 2015

@author: groegert
'''
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk


class OptionPage(object):
    '''
    classdocs
    '''


    def __init__(self, parent, option):
        '''
        Constructor, all derived pages should be created using such constructor
        '''
        self.option = option
        self.__buildFrame__(parent)
        self.updateWindow()
    
    def __buildFrame__(self, parent):
        self.frameMain = tk.Frame(master=parent)
        self.frameMain.pack(side='top', fill='both', expand=True)

    def updateWindow(self):
        '''
        prepares the window with possible settings and updates the ui
        '''
        pass

    def apply(self):
        '''
        all derived pages should have an apply function to write the values from the ui into the model
        '''
        pass
