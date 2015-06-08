'''
Created on 28.03.2015

@author: crimsen
'''
import gnupg
from model.passObject import PasswordObject
from model.PasswordSafeReader import PasswordSafeReader
from model.PasswordSafeWriter import PasswordSafeWriter

class PasswordSafe(object):
    
    def __init__(self, option):
        self.passwordSafe = []
        self.option = option
        self.gpg = gnupg.GPG()
                 
    def newPassObject(self, title='', username='', password='', email='', location='', note=''):
        '''
        Create a new passwordobject
        And save it in RAM
        '''
        passOb = PasswordObject(title, username, password, email, location, note)
        self.passwordSafe.append(passOb)
        self.passsafesort()
        self.markFileModified(passOb)

        #TODO: do we really want to safe everything when a new password is created?
        self.save()
        
    def loadPassObject(self, title, username, password, email, location, note):
        '''
        Load a Passobject from XML file
        '''
        
        passOb = PasswordObject(title, username, password, email, location, note)
        self.passwordSafe.append(passOb)
        self.passsafesort()
        return passOb
        
    
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
        
    def changePassOb(self, index, title='', username='', password='', email='', location='', note=''):
        '''
        Change the attributes of the passwordobject
        And write it in a file
        '''
        
        passOb=self.passwordSafe[index]
        passOb.setTitle(title)
        passOb.setUsername(username)
        passOb.setPassword(password)
        passOb.setEmail(email)
        passOb.setLocation(location)
        passOb.setNote(note)
        
        self.markFileModified(passOb)
           
        #TODO: do we really want to save on each password change? Why dont we backup here?
        self.save()
                                   
    def removePassOb(self, index):
        '''
        Delete a passwordobject
        And write it in a file
        '''
        passOb = self.passwordSafe[index]
        self.passwordSafe.remove(passOb)
        
        self.markFileModified(passOb)

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
                
    def markFileModified(self, passwordObject):
        passwordFile = passwordObject.getPasswordFile()
        if None == passwordFile:
            passwordFile = self.option.getDefaultPasswordFile()
        passwordFile.setChanged(True)

    
