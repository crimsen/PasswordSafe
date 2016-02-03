'''
Created on 28.03.2015

@author: crimsen
'''

from model.PasswordSafeReader import PasswordSafeReader
from model.PasswordSafeWriter import PasswordSafeWriter
from model.SafeItem import SafeItem
from model.passObject import PasswordObject
import gnupg

class PasswordSafe(object):
    '''
    This is the store that contains the root of the data model
    It is also used as factory for different types of passwords
    '''
    
    def __init__(self, option):
        self.passwordSafe = []
        self.option = option
        self.gpg = gnupg.GPG()

    def createPasswordItem(self, title='', username='', password='', email='', location='', note='', createDate=None, history=[]):
        passwordObject = PasswordObject(title, username, password, email, location, note, createDate)
        passwordObject.haveCreateDate()
        retVal = SafeItem(passwordObject, history)
        return retVal
    
    def createPasswordObject(self, title, username, password, email, location, note, createDate=None, endDate=None):
        retVal = PasswordObject(title, username, password, email, location, note, createDate, endDate)
        retVal.haveCreateDate()
        retVal.haveEndDate()
        return retVal

    def addSafeItem(self, safeItem):
        self.passwordSafe.append(safeItem)
    
    def removeSafeItem(self, safeItem):
        self.passwordSafe.remove(safeItem)
                    
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
                
