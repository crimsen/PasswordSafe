'''
Created on Mar 3, 2016

@author: groegert
'''
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
    import tkinter.messagebox
else:
    import Tkinter as tk
    import tkMessageBox as messagebox

class MessageWindow(object):
    '''
    classdocs
    '''


    def __init__(self, title, message):
        '''
        Constructor
        '''
        messagebox.showinfo(title, message)
