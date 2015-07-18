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
from gui.AboutFrame import AboutFrame

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
            self.mainWindow.setunlockframe()
            print('unlock complete')
            self.updateTitleBox()
            if 0 != self.option.gui.autolock:
                self.startTimeControl()
            self.settimeback()
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
        self.loadoption()
        #do we need to start the autolock?
        # might be it is already started
        # --> take self.time to decide whether autolock is started
        if 0 == self.time and None != self.mainWindow.getunlockframe() and 0 != self.option.gui.autolock:
            self.startTimeControl()
        self.settimeback()
        
    def controlOptionSave(self):
        
        if self.mainWindow.getunlockframe() == None:
            self.pressOptionSave()
        elif self.mainWindow.getlockframe() == None:
            if self.option.getEmail() != self.option.getEmailOld():
                self.pressmainLock()
                self.pressOptionSave()
            else:
                self.pressOptionSave()
    
    def pressnewpass(self):
        self.settimeback()
        self.newpasswindow = NewPassWindow(self)
        self.newpasswindow.setTimeControl(self)
        self.newpasswindow.show()
        
    def presschangepass(self, index):
        self.settimeback()
        passObFilter = self.filter.getFilteredpasssafe()[index]
        self.changepass = ChangePassWindow(self, passObFilter)
        self.changepass.setTimeControl(self)
        self.changepass.show()

    def addPasswordObject(self, passwordObject):
        print('save new password')
        self.passsafe.addPasswordObject(passwordObject)
        self.filter = PassSafeFilter(self.passsafe.getSafe())
        self.updateTitleBox()
        self.settimeback()
        
    def changePasswordObject(self, origPasswordObject, passwordObject):
        print('save passwordchanges')
        self.passsafe.changePasswordObject(origPasswordObject, passwordObject)
        self.filter = PassSafeFilter(self.passsafe.getSafe())
        self.updateTitleBox()
        self.settimeback()

    def pressremovepass(self, index):
        print('password deleted')
        
        passObFilter = self.filter.getFilteredpasssafe()[index]
        for passObSafe in self.passsafe.getSafe():
            if passObFilter == passObSafe:
                self.passsafe.removePassOb(passObSafe)
        

        self.filter = PassSafeFilter(self.passsafe.getSafe())
        self.updateTitleBox()
        self.settimeback()
        
    def pressViewHistory(self, index):
        history = self.filter.getFilteredpasssafe()[index].getHistory()
        self.viewHistory = ViewHistory(self, self.mainWindow, history)
        self.viewHistory.show()
        
    def pressCopy(self, entry):
        self.mainWindow.mainWindow.clipboard_clear()
        self.mainWindow.mainWindow.clipboard_append(entry)
        
    def pressAbout(self):
        self.aboutFrame = AboutFrame()
    
    def loadoption(self):
        print('loadoptions')
        self.optionloader = OptionLoader(self.optionfile, self)
        self.optionloader.loadOptions(self.optionfile, self.option)
        self.accounts = self.optionloader.getaccounts()
        self.account = self.option.getEmail()
        self.mainWindow.setAccount(self.account)
    
    def loadPassOb(self, index):
        print('load PasswordObject')
        if -1  != index:
            title = self.filter.getTitle(index)
            username = self.filter.getUsername(index)
            password = self.filter.getPassword(index)
            email = self.filter.getEmail(index)
            location = self.filter.getLocation(index)
            note = self.filter.getNote(index)
        else:
            title = ""
            username = ""
            password = ""
            email = ""
            location = ""
            note = ""
        
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
    
    def startTimeControl(self):
        self.mainWindow.getmainwindow().after(1000, self.timecontrol)

    def timecontrol(self):
        # we need to check the autolock every time because it might be changed in option dialog while
        # a self.timecontrol was queued
        if 0 != self.option.gui.autolock:
            self.time -= 1
            print self.time
            if self.time <= 0:
                if self.time !=-1:
                    self.pressmainLock()
            else:
                self.mainWindow.setTime(self.time)
                self.mainWindow.getmainwindow().after(1000, self.timecontrol)
        else:
            self.mainWindow.setTime(None)
            
    def updatefilter(self, filterstring='', filterattribute=[]):
        self.filter.setFilterstring(filterstring)
        self.filter.setFilterattribute(filterattribute)
        self.updateTitleBox()
        self.settimeback()
        
    def updateTitleBox(self):
        self.filter.doFilter()
        self.mainWindow.insertTitleBox(self.filter.getFilteredpasssafe())
        if 0 != len(self.filter.getFilteredpasssafe()):
            self.mainWindow.getunlockframe().setTitleBoxIndex(0)
        else:
            self.loadPassOb(-1)
    
    def resetTime(self):
        self.time = self.option.gui.autolock

    def settimeback(self):
        #legacy
        self.resetTime()
        
    def settimezero(self):
        self.time = 0
       
    def show(self):
        self.mainWindow.show()
    
