'''
Created on May 12, 2015

@author: thomas
'''

import Tkinter as tk

class FilesPage(object):
    '''
    Page for the options dialog.
    This page shows up all files that have to be loaded.
    It provides adding and removing files.
    '''


    def __init__(self, parent, option):
        '''
        Constructor
        '''
        self.option = option
        self.__buildFrame__(parent)
        self.updateWindow()
        
    def __buildFrame__(self, parent):
        self.frameMain = tk.Frame(master=parent)
        self.fileBox = tk.Listbox(master=self.frameMain)
        self.frameMain.pack(side='top', fill='both', expand=True)
        self.fileBox.pack(side='top', fill='both', expand=True)

    def readFromOption(self):
        '''
        reads values from the option object and sets the ui according to the values
        '''
        files = [a.getFilename() for a in self.option.getFiles()]
        self.loadFileBox(files)

    def updateWindow(self):
        '''
        prepares the window with possible settings and updates the ui
        '''
        self.readFromOption()

    def loadFileBox(self, files):
        self.fileBox.delete(0, 'end')
        for filename in files:
            self.fileBox.insert('end', filename)
        
