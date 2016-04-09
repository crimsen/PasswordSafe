'''
Created on May 12, 2015

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

class FilesPage(EmptyPage):
    '''
    Page for the options dialog.
    This page shows up all files that have to be loaded.
    It provides adding and removing files.
    '''
    def __init__(self, parent, context):
        '''
        Constructor
        '''
        self.view = FilesPageView(parent)
        self.controller = FilesPageController(self.view, context)
    def setModel(self, model):
        self.controller.setModel(model)
        self.view.updateFromModel(model)

class FilesPageContext(EmptyPageContext):
    def __init__(self, option):
        EmptyPageContext.__init__(self, option)

class FilesPageView(EmptyPageView):
    def __init__(self, parent):
        self.__buildFrame__(parent)
    def __buildFrame__(self, parent):
        self.frame = tk.Frame(master=parent)
        self.fileBox = tk.Listbox(master=self.frame)
        self.frame.pack(side='top', fill='both', expand=True)
        self.fileBox.pack(side='top', fill='both', expand=True)

    def updateFromModel(self, model):
        files = [a.getFilename() for a in model.getFiles()]
        self.loadFileBox(files)

    def loadFileBox(self, files):
        self.fileBox.delete(0, 'end')
        for filename in files:
            self.fileBox.insert('end', filename)
        
class FilesPageController(EmptyPageController):
    def __init__(self, view, context):
        EmptyPageController.__init__(self, view, context)
