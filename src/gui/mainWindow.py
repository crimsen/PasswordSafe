'''
Created on 15.04.2015

@author: crimsen
'''
import Tkinter as tk
from Tkinter import StringVar
from gui.LockFrame import LockFrame
from gui.UnlockFrame import UnlockFrame

class MainWindow(object):
    '''
    classdocs
    '''

    
    def __init__(self, controller):
            
        self.mainWindow = tk.Tk()
        self.mainWindow.title('Passwordsafe')
        self.mainWindow.geometry('900x500')
        
        self.maincontroller = controller
        
        self.account = ''
        
        self.lockframe = None
        self.unlockframe = None
        
        self.showlockframe()
        
    def __initUnlockFrame__(self):
        self.unlockframe = UnlockFrame(self, self.maincontroller) 

    def __initLockFrame__(self):
        
        self.lockframe = LockFrame(self, self.maincontroller)
        
    def insertTitleBox(self, passSafe):
        self.unlockframe.insertTitleBox(passSafe)
            
    def getlockframe(self):
        return self.lockframe
    
    def getunlockframe(self):
        return self.unlockframe
    
    def getmainwindow(self):
        return self.mainWindow
    
    def setlockframe(self):
        self.__initLockFrame__()
        
    def setunlockframe(self):
        self.__initUnlockFrame__()
        
    def showunlockframe(self):
        if self.lockframe != None:
            self.lockframe.destroy()
        self.__initUnlockFrame__(self.mainWindow)
        
    def showlockframe(self):
        if self.unlockframe != None:
            self.unlockframe.destroy()
        self.__initLockFrame__()
    
    def pressoptions(self):
        self.maincontroller.pressoptions()
    
    def presslock(self):
        self.maincontroller.pressmainLock()
            
    def pressunlock(self, passphrase):
        self.maincontroller.pressmainUnlock(passphrase)   
            
    def setlabelpassphrase(self):
        self.lockframe.setlabelpassphrase()
                
    def setAccount(self, account):
        self.account = account
        self.lockframe.setAccount(account)
        
    def setfills(self, *params):
        self.unlockframe.setfills(params)
        
    def setTime(self, time):
        self.unlockframe.setTime(time) 
        
    def show(self):
        self.mainWindow.mainloop()   