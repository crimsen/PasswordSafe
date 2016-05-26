'''
Created on 09.07.2015

@author: crimsen
'''
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class AboutFrame(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title('About PasswordSafe')
        self.root.geometry('200x200')
        
        self.__buildFrame__(self.root)
    
    def __buildFrame__(self,parent):
        
        self.mainFrame = tk.Frame(master=parent)
        self.labelPasswordSafe = tk.Label(master=self.mainFrame, text='PasswordSafe', font=('Arial 22 bold'))
        self.labelInfo = tk.Label(master=self.mainFrame, text='Version 2.0.1')
        
        self.mainFrame.pack(expand=True, fill='both')
        self.labelPasswordSafe.pack(side='top', fill='both', expand=True, anchor='center')
        self.labelInfo.pack(side='top', fill='both', expand=True, anchor='center')
