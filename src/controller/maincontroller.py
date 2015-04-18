'''
Created on 15.04.2015

@author: crimsen
'''
from gui.mainWindow import MainWindow
from model.passSafe import PasswordSafe
from model.optionLoader import OptionLoader
import os
from gui.optionWindow import OptionWindow
from gui.newPassWindow import NewPassWindow
from gui.changePassWindow import ChangePassWindow
import time


class MainController(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__searchFiles__()
        self.__initGUI__()
        self.time = 0
        
        
    def __searchFiles__(self):
        '''
        Search Safe and Option-File
        If not exist create path
        '''
        home = os.environ['HOME']
        
        self.safefile = home+'/Documents/.PasswordSafe/safe.xml'
        self.optionfile = home+'/Documents/.PasswordSafe/option.xml'
        
        self.dirfile = os.path.dirname(self.safefile)
        if not os.path.exists(self.dirfile):
            os.makedirs(self.dirfile)
        print(str(self.dirfile))  
    
    def existingFile(self, filename):
        retVal = False
        if os.path.isfile(filename):
            retVal = True
        return retVal   
    
    def __initGUI__(self):
        print('init gui')
        self.mainWindow = MainWindow(self)
        
    def pressmainLock(self):
        print('locking screen')
        self.settimezero()
        if self.mainWindow.getunlockframe() != None:
            self.mainWindow.getunlockframe().destroy()
        self.mainWindow.setlockframe()
    
    def pressmainUnlock(self, passphrase):
        print('try to unlock screen')
        if self.existingFile(self.optionfile):
            self.loadoption()
            try:
                self.passsafe = PasswordSafe(self.safefile, self.account, passphrase, self)
                if self.mainWindow.getlockframe() != None:
                    self.mainWindow.getlockframe().destroy()
                self.mainWindow.setunlockframe()
                print('unlock complete')
                self.mainWindow.insertTitleBox(self.passsafe.getSafe())
                self.settimeback()
                self.mainWindow.getmainwindow().after(1000, self.timecontrol)
            except:
                self.mainWindow.setlabelpassphrase()
        else:
            print('fail to unlock screen')
            self.mainWindow.showoptionerror()
            
    def pressoptions(self):
        self.settimeback()
        print('open options')
        self.optionloader = OptionLoader(self.optionfile, self)
        self.accounts = self.optionloader.getaccounts()
        
        self.optionwindow = OptionWindow(self.accounts, self)
        self.optionwindow.show()
        
    def pressoptionsave(self, entry):
        print('save options')
        self.optionloader.writeEmailOption(entry, self.optionfile)
        self.settimeback()
    
    def pressnewpass(self):
        print('open newpassword')
        self.settimeback()
        self.newpasswindow = NewPassWindow(self)
        self.newpasswindow.show()
        
    def presschangepass(self, index):
        self.settimeback()
        print('open changepassword')
        title = self.passsafe.getTitle(index)
        username = self.passsafe.getUsername(index)
        password = self.passsafe.getPassword(index)
        email = self.passsafe.getEmail(index)
        location = self.passsafe.getLocation(index)
        note = self.passsafe.getNote(index)
        self.changepass = ChangePassWindow(self, index, title, username, password, email, location, note)
            
    def pressnewpasssave(self, title, username, password, email, location, note):
        print('save new password')
        self.passsafe.newPassObject(title, username, password, email, location, note) 
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
        self.settimeback()
        
    def presschangepasssave(self, index, title, username, password, email, location, note):
        print('save passwordchanges')
        self.passsafe.changePassOb(index, title, username, password, email, location, note)
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
        self.settimeback()
    
    def pressremovepass(self, index):
        print('password deleted')
        self.passsafe.removePassOb(index)
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
        self.settimeback()
               
    def loadoption(self):
        print('loadoptions')
        self.optionloader = OptionLoader(self.optionfile, self)
        self.accounts = self.optionloader.getaccounts()
        self.account = self.optionloader.getemail()
    
    def loadPassOb(self, index):
        print('load PasswordObject')
        title = self.passsafe.getTitle(index)
        username = self.passsafe.getUsername(index)
        password = self.passsafe.getPassword(index)
        email = self.passsafe.getEmail(index)
        location = self.passsafe.getLocation(index)
        note = self.passsafe.getNote(index)
        
        title = self.controlNone(title)
        username = self.controlNone(username)
        password = self.controlNone(password)
        email = self.controlNone(email)
        location = self.controlNone(location)
        note = self.controlNone(note)
        
        self.mainWindow.setfills(title, username, password, email, location, note)
        self.settimeback()
        
    def controlNone(self, attr):
        if attr == 'None':
            retVal = ''
        else:
            retVal = attr 
        return retVal
    
    def timecontrol(self):
        self.time -= 1
        print self.time
        if self.time <= 0:
            if self.time !=-1:
                self.pressmainLock()
        else:
            self.mainWindow.setTime(self.time)
            self.mainWindow.getmainwindow().after(1000, self.timecontrol)
    
    def settimeback(self):
        self.time = 60
        
    def settimezero(self):
        self.time = 0
       
    def show(self):
        self.mainWindow.show()
    