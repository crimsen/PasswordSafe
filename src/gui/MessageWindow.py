'''
Created on Mar 3, 2016

@author: groegert
'''
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class MessageWindow(object):
    '''
    classdocs
    '''


    def __init__(self, message):
        '''
        Constructor
        '''
        self.root = tk.Toplevel()
        self.root.title('Message')
        self.__buildFrame__(self.root, message)

    def __buildFrame__(self, parent, message):
        self.mainFrame = tk.Frame(master=parent)
        self.message = tk.Label(master=self.mainFrame, text=message)
        self.mainFrame.pack(expand=True, fill='both')
        self.message.pack(side='top', fill='both', expand=True, anchor='center')