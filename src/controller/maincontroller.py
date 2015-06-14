'''
Created on 15.04.2015

@author: crimsen
'''
from gui.mainWindow import MainWindow
from model.passSafe import PasswordSafe
from model.optionLoader import OptionLoader
from model.OptionWriter import OptionWriter
from model.Option import Option
import os
from gui.optionWindow import OptionWindow
from gui.newPassWindow import NewPassWindow
from gui.changePassWindow import ChangePassWindow
from controller.filter import PassSafeFilter
import sys
from gui.ViewHistory import ViewHistory

class MainController(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.option = Option( )
        self.searchOptionFile()
        self.__initGUI__()
        self.time = 0
        
    def searchOptionFile(self):
        '''
        Search Option-File
        If not exist create path
        '''
        home = os.environ['HOME']
        
        self.optionfile = home+'/Documents/.PasswordSafe/option.xml'
        
        self.dirfile = os.path.dirname(self.optionfile)
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
        if not self.existingFile(self.optionfile):
            self.pressoptions()
        else: self.loadoption()
        
    def pressmainLock(self):
        print('locking screen')
        self.settimezero()
        self.mainWindow.hideUnlockFrame()
        self.mainWindow.setlockframe()
        self.mainWindow.setAccount(self.option.getEmail())
    
    def pressmainUnlock(self, passphrase):
        print('try to unlock screen')
        try:
            self.passsafe = PasswordSafe(self.option)
            self.passsafe.load(passphrase)
            self.filter = PassSafeFilter(self.passsafe.getSafe())
            self.mainWindow.hideLockFrame()
            self.filter.doFilter()
            self.mainWindow.setunlockframe()
            print('unlock complete')
            self.mainWindow.insertTitleBox(self.filter.getFilteredpasssafe())
            self.settimeback()
            self.mainWindow.getmainwindow().after(1000, self.timecontrol)
        except:
            print sys.exc_info()
            self.mainWindow.setlabelpassphrase()
            
    def pressoptions(self):
        self.settimeback()
        print('open options')
        self.optionwindow = OptionWindow(self.option, self)
        self.optionwindow.show()
        
    def pressOptionSave(self):
        print('save options')
        writer = OptionWriter()
        writer.write(self.option, self.optionfile)
        self.settimeback()
        self.loadoption()
    
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
        self.filter = PassSafeFilter(self.passsafe.getSafe())
        self.filter.doFilter() 
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
        self.settimeback()
        
    def presschangepasssave(self, index, title, username, password, email, location, note):
        print('save passwordchanges')
        self.passsafe.changePassOb(index, title, username, password, email, location, note)
        self.filter = PassSafeFilter(self.passsafe.getSafe())
        self.filter.doFilter()
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
        self.settimeback()
    
    def pressremovepass(self, index):
        print('password deleted')
        self.passsafe.removePassOb(index)
        self.filter = PassSafeFilter(self.passsafe.getSafe())
        self.filter.doFilter()
        self.mainWindow.insertTitleBox(self.passsafe.getSafe())
        self.settimeback()
        
    def pressViewHistory(self, index):
        history = self.passsafe.getSafe()[index].getHistory()
        self.viewHistory = ViewHistory(self.mainWindow, history)
        self.viewHistory.show()
        
    def pressCopy(self, entry):
        self.mainWindow.mainWindow.clipboard_clear()
        self.mainWindow.mainWindow.clipboard_append(entry)
    
    def loadoption(self):
        print('loadoptions')
        self.optionloader = OptionLoader(self.optionfile, self)
        self.optionloader.loadOptions(self.optionfile, self.option)
        self.accounts = self.optionloader.getaccounts()
        self.account = self.option.getEmail()
        self.mainWindow.setAccount(self.account)
    
    def loadPassOb(self, index):
        print('load PasswordObject')
        title = self.filter.getTitle(index)
        username = self.filter.getUsername(index)
        password = self.filter.getPassword(index)
        email = self.filter.getEmail(index)
        location = self.filter.getLocation(index)
        note = self.filter.getNote(index)
        
        title = self.controlNone(title)
        username = self.controlNone(username)
        password = self.controlNone(password)
        email = self.controlNone(email)
        location = self.controlNone(location)
        note = self.controlNone(note)
        
        self.mainWindow.setfills(title, username, password, email, location, note)
        self.settimeback()
        
    def controlNone(self, attr):
        if (attr == None) or (attr == 'None'):
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
            
    def updatefilter(self, filterstring='', filterattribute=[]):
        self.filter.setFilterstring(filterstring)
        self.filter.setFilterattribute(filterattribute)
        self.filter.doFilter()
        self.mainWindow.insertTitleBox(self.filter.getFilteredpasssafe())
        self.settimeback()
    
    def settimeback(self):
        self.time = 60
        
    def settimezero(self):
        self.time = 0
       
    def show(self):
        self.mainWindow.show()
    
