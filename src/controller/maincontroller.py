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
        
        self.mainWindow = MainWindow(self)
        
    def pressmainLock(self):
        if self.mainWindow.getunlockframe() != None:
            self.mainWindow.getunlockframe().destroy()
        self.mainWindow.setlockframe()
    
    def pressmainUnlock(self):
        if self.existingFile(self.optionfile):
            self.loadoption()
            self.passsafe = PasswordSafe(self.safefile, self.account, self)
            if self.mainWindow.getlockframe() != None:
                self.mainWindow.getlockframe().destroy()
            self.mainWindow.setunlockframe()
            self.mainWindow.insertTitleBox(self.passsafe.getSafe())
        else:
            self.mainWindow.showoptionerror()
            
    def pressoptions(self):
        self.optionloader = OptionLoader(self.optionfile, self)
        self.accounts = self.optionloader.getaccounts()
        
        self.optionwindow = OptionWindow(self.accounts, self)
        self.optionwindow.show()
        
    def pressoptionsave(self, entry):
        self.optionloader.writeEmailOption(entry, self.optionfile)
    
    def pressnewpass(self):
        self.newpasswindow = NewPassWindow(self)
        self.newpasswindow.show()
        
    def presschangepass(self, index):
        title = self.passsafe.getTitle(index)
        username = self.passsafe.getUsername(index)
        password = self.passsafe.getPassword(index)
        email = self.passsafe.getEmail(index)
        location = self.passsafe.getLocation(index)
        note = self.passsafe.getNote(index)
        self.changepass = ChangePassWindow(self, index, title, username, password, email, location, note)
            
    def pressnewpasssave(self, title, username, password, email, location, note):
        self.passsafe.newPassObject(title, username, password, email, location, note) 
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
        
    def presschangepasssave(self, index, title, username, password, email, location, note):
        self.passsafe.changePassOb(index, title, username, password, email, location, note)
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
    
    def pressremovepass(self, index):
        self.passsafe.removePassOb(index)
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
               
    def loadoption(self):
        self.optionloader = OptionLoader(self.optionfile, self)
        self.accounts = self.optionloader.getaccounts()
        self.account = self.optionloader.getemail()
    
    def loadPassOb(self, index):
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
        
    def controlNone(self, attr):
        if attr == 'None':
            retVal = ''
        else:
            retVal = attr 
        return retVal
       
    def show(self):
        self.mainWindow.show()