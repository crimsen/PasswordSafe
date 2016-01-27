'''
Created on 28.03.2015

@author: crimsen
'''
import gnupg
from datetime import date
from model.NewPasswordObject import NewPasswordObject
from model.HistoryPasswordObject import HistoryPasswordObject
from model.PasswordSafeReader import PasswordSafeReader
from model.PasswordSafeWriter import PasswordSafeWriter

class PasswordSafe(object):
    
    def __init__(self, option):
        self.passwordSafe = []
        self.option = option
        self.gpg = gnupg.GPG()

    def newPassObject(self, title='', username='', password='', email='', location='', note='', createDate=None, history=[]):
        '''
        Create a new passwordobject
        And save it in RAM
        '''
        passOb = NewPasswordObject(title, username, password, email, location, note, createDate, history)
        self.addNewPasswordObject(passOb)
        
    def loadPassObject(self, title, username, password, email, location, note, createDate, history):
        '''
        Load a Passobject from XML file
        '''
        
        passOb = NewPasswordObject(title, username, password, email, location, note, createDate, history)
        passOb.haveCreateDate()
        self.passwordSafe.append(passOb)
        return passOb
    
    def loadHistoryPassObject(self, title, username, password, email, location, note, createDate=None, endDate=None):
        passOb = HistoryPasswordObject(title, username, password, email, location, note, createDate, endDate)
        passOb.haveCreateDate()
        passOb.haveEndDate()
        return passOb
    
    def createHistoryPasswordObject(self, passwordObject):
        retVal = HistoryPasswordObject()
        retVal.copyFrom(passwordObject)
        retVal.haveCreateDate()
        retVal.haveEndDate()
        return retVal
        
    def addPasswordObject(self, passwordObject):
        newPasswordObject = NewPasswordObject()
        newPasswordObject.copyFrom(passwordObject)
        self.addNewPasswordObject(newPasswordObject)
    
    def addNewPasswordObject(self, newPasswordObject):
        newPasswordObject.haveCreateDate()
        self.passwordSafe.append(newPasswordObject)
        self.passsafesort()
        self.markModified(newPasswordObject)
        #TODO: do we really want to safe everything when a new password is created?
        self.save()
    
    def load(self, passphrase):
        '''
        Load the xml-file
        Save the passwordobjects in RAM
        '''
        passwordSafeReader = PasswordSafeReader(self.option, self.gpg)
        passwordSafeReader.read(self, passphrase)
               
    def save(self):
        '''
        Write the xml-file
        '''
        passwordSafeWriter = PasswordSafeWriter(self.option, self.gpg)
        passwordSafeWriter.write(self)
        
        self.passsafesort()
        
    def changePasswordObject(self, passwordObject, newPasswordObject):
        '''
        Change the attributes of the passwordobject
        And write it in a file
        '''
        
        historyPasswordObject = self.createHistoryPasswordObject(passwordObject)
        origPasswordFile = passwordObject.getPasswordFile()
        passwordObject.copyFrom(newPasswordObject)
        passwordObject.addHistory(historyPasswordObject)
        passwordObject.setCreateDate(date.today())
        self.markModified(passwordObject)
        if origPasswordFile != passwordObject.getPasswordFile():
            self.markFileModified(origPasswordFile)
        #TODO: do we really want to save on each password change? Why dont we backup here?
        self.save()
                                   
    def removePassOb(self, passOb):
        '''
        Delete a passwordobject
        And write it in a file
        '''
        self.passwordSafe.remove(passOb)
        
        self.markModified(passOb)

        #TODO: do we really want to save on each password change? Why dont we backup here?
        self.save()
                    
    def passsafesort(self):
        self.passwordSafe = self.sortfunc(self.passwordSafe)
     
    def sortfunc(self, array):
        less = []
        equal = []
        greater = []
    
        if len(array) > 1:
            pivot = array[0].getTitle().lower()
            for x in array:
                if x.getTitle().lower() < pivot:
                    less.append(x)
                if x.getTitle().lower() == pivot:
                    equal.append(x)
                if x.getTitle().lower() > pivot:
                    greater.append(x)
            return self.sortfunc(less)+equal+self.sortfunc(greater)
        else:  
            return array 
    
    def printFu(self, list):
        for x in list:
            print(x.getTitle())
            
    def getSafe(self):
        return self.passwordSafe
    
    def getTitle(self, index):
        return self.passwordSafe[index].getTitle()
    
    def getUsername(self, index):
        return self.passwordSafe[index].getUsername()
    
    def getPassword(self, index):
        return self.passwordSafe[index].getPassword()
    
    def getEmail(self, index):
        return self.passwordSafe[index].getEmail()
    
    def getLocation(self, index):
        return self.passwordSafe[index].getLocation()
    
    def getNote(self, index):
        return self.passwordSafe[index].getNote()
    
    def getSafeIndex(self, index):
        return self.passwordSafe[index]
    
    def close(self):
        del self.passwordSafe
                
    def markModified(self, passwordObject):
        passwordFile = passwordObject.getPasswordFile()
        self.markFileModified(passwordFile)

    def markFileModified(self, passwordFile):
        if None == passwordFile:
            passwordFile = self.option.getDefaultPasswordFile()
        passwordFile.setChanged(True)
