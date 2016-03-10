'''
Created on Mar 4, 2016

@author: groegert
'''
from EmptyPage import EmptyPage
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class CertificatePage(EmptyPage):
    '''
    compare to OptionPage derived pages
    '''


    def __init__(self, parent, context):
        '''
        Constructor
        '''
        self.view = CertificatePageView(parent)
        self.controller = CertificatePageController(self.view, context)
    
    def apply(self):
        self.controller.apply()

class CertificatePageContext(object):
    def __init__(self, option):
        self.option = option

class CertificatePageView(object):
    def __init(self, parent):
        self.__buildframe__(parent)
    def __buildframe__(self, parent):
        self.frame = tk.Frame(master=parent)
        self.frame.pack(side='top', fill='both', expand=True)

class CertificatePageController(object):
    def __init__(self, view, context):
        self.view = view
        self.context = context
    def apply(self):
        pass
