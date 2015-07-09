'''
Created on 12.05.2015

@author: timgroger
'''
import Tkinter as tk

class LockFrame(object):
    '''
    classdocs
    '''


    def __init__(self, mainWindow, mainController):
        '''
        Constructor
        '''
        
        self.mainWindow = mainWindow
        self.mainWindowFrame = self.mainWindow.getmainwindow()
        self.mainController = mainController
        
        self.lockframe = tk.Frame(master=self.mainWindowFrame)
        self.lockframe.pack(fill='both', expand=True)
        self.__buildLockFrame(self.lockframe)
        self.__buildMenuBarLock__(self.lockframe)        
        
    def __buildLockFrame(self, parent):
        self.frameLock = tk.Frame(master=parent)
#         self.labelFunny = tk.Label(master=self.frameLock,fg='red', text='YOU\nSHALL\nNOT\nPASS!', font='Arial 72 bold')
        self.framePassphrase = tk.Frame(master=self.frameLock)
        self.labelPassphrase = tk.Label(master=self.framePassphrase, text='Please insert your Passphrase:', underline=19)
        self.entryPassphrase = tk.Entry(master=self.framePassphrase, justify='center', show='*')
        self.labelFalse = tk.Label(master=self.framePassphrase, text='', fg='red')
        self.buttonUnlock = tk.Button(master=self.frameLock, text='Unlock', underline=0)
        self.mainWindowFrame.bind('<Alt-u>', self.pressunlock)
        self.buttonUnlock.bind('<1>', self.pressunlock)
        self.buttonUnlock.bind('<Return>', self.pressunlock)
        self.entryPassphrase.bind('<Return>', self.pressunlock)
        
        self.labelAccount = tk.Label(master=self.frameLock, text='Account: ')
        self.labelAccountChoosed = tk.Label(master=self.frameLock, text='test')
        
        
        
        self.frameLock.pack(side='top', fill='both', expand=True)
#         self.labelFunny.pack(expand=True)
        self.labelAccount.pack(side='left', anchor='n', padx=5, pady=5)
        self.labelAccountChoosed.pack(side='left', anchor='n', padx=5, pady=5)
        self.framePassphrase.place(relx=0.4, rely=0.4)
        self.labelPassphrase.pack(side='top', padx=5, pady=5, fill='both')
        self.entryPassphrase.pack(side='top', fill='both', padx=5, pady=5)
        self.labelFalse.pack(side='top', fill='both', padx=5, pady=5)
        self.buttonUnlock.pack(side='bottom', anchor='se')  
         
        self.entryPassphrase.focus()
        
    def __buildMenuBarLock__(self, parent):
        '''
        Build the MenuBar if the window is locked
        '''
        
        self.menuBarLocked = tk.Menu(master=parent)
        
        self.fileMenu = tk.Menu(master=self.menuBarLocked, tearoff=0)
        self.fileMenu.add_command(label='Options', underline=0, command=self.pressoptions)
        self.menuBarLocked.add_cascade(label='File', underline=0, menu=self.fileMenu)
        self.menuBarLocked.add_command(label='About', underline=0, command=self.pressAbout)
        
        self.mainWindowFrame.config(menu=self.menuBarLocked)
        
    def hide(self):
        self.mainWindowFrame.unbind('<Alt-u>')

    def pressunlock(self, event):
        passphrase = self.entryPassphrase.get()
        self.mainController.pressmainUnlock(passphrase)
        
    def pressoptions(self):
        self.mainWindow.pressoptions()
        
    def pressAbout(self):
        self.mainController.pressAbout()
        
    def setAccount(self, account):
        self.account = account
        self.labelAccountChoosed.config(text=self.account)
        
    def setlabelpassphrase(self):
        self.labelFalse.config(text='Your passphrase is wrong!')
        
    def destroy(self):
        self.lockframe.destroy()    
