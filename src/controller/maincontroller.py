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
from gui.OptionWindow import OptionWindow
import sys
from gui.AboutFrame import AboutFrame
from gui.PassGenWindow import PassGenWindow
from edit.EditingDomain import EditingDomain
from gui.MessageWindow import MessageWindow

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
        self.editingDomain = EditingDomain()
        self.__initGUI__()
        self.time = 0
        
    def getMainWindow(self):
        return self.mainWindow.getmainwindow()
    
    def getOption(self):
        return self.option
        
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
            self.pressOptions()
        else: self.loadoption()
        
    def pressLock(self):
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
            #self.filter = PassSafeFilter(self.passsafe.getSafe())
            self.editingDomain.setModel(self.passsafe)
            self.mainWindow.hideLockFrame()
            self.mainWindow.setunlockframe()
            print('unlock complete')
            if 0 != self.option.gui.autolock:
                self.startTimeControl()
            self.settimeback()
            self.warnOnFileVersion()
        except:
            print(sys.exc_info())
            self.mainWindow.setlabelpassphrase()
            
    def pressOptions(self):
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
    
    def copyToClipBoard(self, entry):
        self.mainWindow.mainWindow.clipboard_clear()
        self.mainWindow.mainWindow.clipboard_append(entry)
        
    def pressAbout(self):
        self.aboutFrame = AboutFrame()
        
    def pressPassGen(self):
        self.passGenWindow = PassGenWindow(self, self.mainWindow)
    
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
            print(self.time)
            if self.time <= 0:
                if self.time !=-1:
                    self.pressLock()
            else:
                self.mainWindow.setTime(self.time)
                self.mainWindow.getmainwindow().after(1000, self.timecontrol)
        else:
            self.mainWindow.setTime(None)
    
    def resetTime(self):
        self.time = self.option.gui.autolock

    def settimeback(self):
        #legacy
        self.resetTime()
        
    def settimezero(self):
        self.time = 0
       
    def show(self):
        self.mainWindow.show()
    
    def warnOnFileVersion(self):
        if not self.option.getWarnOnFileVersionDone():
            self.option.setWarnOnFileVersionDone(True)
            fileNames = []
            for f in self.option.getFiles():
                if f.getLoadVersion() != f.getVersion():
                    fileNames.append(f.getFilename())
            if 0 < len(fileNames):
                message = 'When safing PasswordFile'
                if 1 < len(fileNames):
                    message += 's'
                message += ': \n'
                message += ',\n'.join(fileNames)
                message += ',\n then the file version will be upgraded.' 
                MessageWindow(message)
