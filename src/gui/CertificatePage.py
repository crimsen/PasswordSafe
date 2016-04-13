'''
Created on Mar 4, 2016

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

class CertificatePage(EmptyPage):
    def __init__(self, parent, context):
        self.view = CertificatePageView(parent)
        self.controller = CertificatePageController(self.view, context)

class CertificatePageContext(EmptyPageContext):
    def __init__(self, option):
        EmptyPageContext.__init__(self, option)

class CertificatePageView(EmptyPageView):
    def __init__(self, parent):
        self.__buildframe__(parent)
    def __buildframe__(self, parent):
        self.frame = tk.Frame(master=parent)
        self.label = tk.Label(master=self.frame, text='Certificate')

        self.frame.pack(side='top', fill='both', expand=True)
        self.label.pack(side='top', padx=5, pady=5, anchor='w')

class CertificatePageController(EmptyPageController):
    def __init__(self, view, context):
        EmptyPageController.__init__(self, view, context)
