'''
Created on Mar 4, 2016

@author: groegert
'''
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk


class EmptyPage(object):
    '''
    classdocs
    '''

    @staticmethod
    def createContext(parentContext):
        return EmptyPageContext(parentContext.getOption())

    def __init__(self, parent, context):
        '''
        Constructor
        '''
        self.view = EmptyPageView(parent)
        self.controller = EmptyPageController(self.view, context)
    
    def apply(self):
        self.controller.apply()
        
    def setModel(self, model):
        pass

class EmptyPageContext(object):
    def __init__(self, option):
        self.option = option

class EmptyPageView(object):
    def __init__(self, parent):
        self.__buildframe__(parent)
    def __buildframe__(self, parent):
        self.frame = tk.Frame(master=parent)
        self.label = tk.Label(master=self.frame, text='unknown object type')

        self.frame.pack(side='top', fill='both', expand=True)
        self.label.pack(side='top', padx=5, pady=5, anchor='w')

class EmptyPageController(object):
    def __init__(self, view, context):
        self.view = view
        self.context = context
    def apply(self):
        pass
    def setModel(self, model):
        self.model = model
