'''
Created on 15.04.2015

@author: crimsen
'''
from Tkinter import Frame
import Tkinter as tk

class LockFrame(Frame):
    '''
    classdocs
    '''


    def __init__(self, parent, mainwindow):
        '''
        Constructor
        '''
        
        self.mainwindow = mainwindow
        
        Frame.__init__(self, parent)
        
        self.parent = parent

    def __buildLockFrame(self, parent):
        self.frameLock = tk.Frame(master=parent)
        self.labelFunny = tk.Label(master=self.frameLock,fg='red', text='YOU\nSHALL\nNOT\nPASS!', font='Arial 72 bold')
#         self.framePassphrase = tk.Frame(master=self.frameLock, bg='green')
#         self.labelPassphrase = tk.Label(master=self.framePassphrase, text='Please insert your Passphrase:')
#         self.entryPassphrase = tk.Entry(master=self.framePassphrase, justify='center')
#         self.labelFalse = tk.Label(master=self.framePassphrase, text='')
        self.buttonUnlock = tk.Button(master=self.frameLock, text='Unlock')
        
        
        
        self.frameLock.pack(side='top', fill='both', expand=True)
        self.labelFunny.pack(expand=True)
#         self.framePassphrase.place(relx=0.4, rely=0.4)
#         self.labelPassphrase.pack(side='top', padx=5, pady=5, fill='both')
#         self.entryPassphrase.pack(side='top', fill='both', padx=5, pady=5)
#         self.labelFalse.pack(side='top', fill='both', padx=5, pady=5)
        self.buttonUnlock.pack(side='bottom', anchor='se')   
        
    def __buildMenuBarLock__(self, parent):
        '''
        Build the MenuBar if the window is locked
        '''
        
        self.menuBarLocked = tk.Menu(master=parent)
        
        self.fileMenu = tk.Menu(master=self.menuBarLocked, tearoff=0)
        self.fileMenu.add_command(label='Options', command=self.optionWindow)
        self.menuBarLocked.add_cascade(label='File', menu=self.fileMenu)
        
        self.mainWindow.config(menu=self.menuBarLocked)     