'''
Created on Mar 14, 2016

@author: groegert
'''
from EmptyPage import EmptyPage
from model.SecretObjectEnum import SecretObjectEnum
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
    import tkinter.ttk as ttk
else:
    import Tkinter as tk
    import ttk as ttk

class SafeItemPage(EmptyPage):
    '''
    Page / form that lets select the type of a SafeItem 
    '''
    def __init__(self, parent, context):
        '''
        Constructor
        '''
        self.view = SafeItemPageView(parent)
        self.controller = SafeItemPageController(self.view, context)
    def apply(self):
        self.controller.apply()
    def setModel(self, model):
        self.controller.setModel(model)
    def getFrame(self):
        return self.view.frame;

class SafeItemPageContext(object):
    def __init__(self, option):
        self.option = option

class SafeItemPageView(object):
    def __init__(self, parent):
        self.__buildframe__(parent)
    def __buildframe__(self, parent):
        self.frame = tk.Frame(master=parent)
        self.comboType = ttk.Combobox(master=self.frame, state='readonly')
        self.comboType['values'] = [e.name for e in SecretObjectEnum]

        self.comboType.pack(side='top', padx=5, pady=5, fill='x')
        self.frame.pack(side='top', fill='both', expand=True)
    def updateFromModel(self, model):
        safeItemType = model.safeItemType
        if None == safeItemType:
            safeItemType = SecretObjectEnum.password
        self.updateType(safeItemType)
    def updateType(self, safeItemType):
        self.comboType.set(safeItemType.name)
    def writeToModel(self, model):
        name = self.comboType.get()
        model.safeItemType = SecretObjectEnum[name]

class SafeItemPageController(object):
    def __init__(self, view, context):
        self.view = view
        self.context = context
    def setModel(self, model):
        self.model = model
        self.view.updateFromModel(model)
    def apply(self):
        self.view.writeToModel(self.model)
