'''
Created on 28.03.2015

@author: crimsen
'''
import gnupg
import os
from datetime import datetime
import shutil
from model.passObject import PasswordObject
from model.PasswordSafeReader import PasswordSafeReader
from model.PasswordSafeWriter import PasswordSafeWriter

class PasswordSafe(object):
    
    def __init__(self, option, controller):
        self.passwordSafe = []
        self.option = option
        self.filename = option.getFiles()[0].getFilename()
        self.account = option.getEmail()
        self.maincontroller = controller
        self.gpg = gnupg.GPG()
                 
    def newPassObject(self, title='', username='', password='', email='', location='', note=''):
        '''
        Create a new passwordobject
        And save it in RAM
        '''
        passOb = PasswordObject(str(title), str(username), str(password), str(email), str(location), str(note))
        self.passwordSafe.append(passOb)
        self.passsafesort()
        
        #TODO: do we really want to safe everything when a new password is created?
        self.save()
        self.backupsafe()
        
    def loadPassObject(self, title, username, password, email, location, note):
        '''
        Load a Passobject from XML file
        '''
        
        passOb = PasswordObject(str(title), str(username), str(password), str(email), str(location), str(note))
        self.passwordSafe.append(passOb)
        self.passsafesort()
        
    
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
           
        #TODO: do we really want to save on each password change? Why dont we backup here?
        self.save()
                                   
    def removePassOb(self, index):
        '''
        Delete a passwordobject
        And write it in a file
        '''
        self.passwordSafe.remove(self.passwordSafe[index])
        
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
    
    def backupsafe(self):
        
        home = os.environ['HOME']
        today = datetime.today()
        
        self.backup = home+'/Documents/.PasswordSafe/'+self.account+'/backup/'
        if not os.path.exists(self.backup):
            os.makedirs(self.backup)
        print self.backup
        
        shutil.copy(self.filename, self.backup+str(today.year)+'-'+str(today.month)+'-'+str(today.day)+'-safe.xml')
        print ('backup completed')
     
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
                
    
    