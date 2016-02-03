'''
Created on 28.03.2015

@author: crimsen
'''
from model.SecretObject import SecretObject

class PasswordObject(SecretObject):


    def __init__(self, title='', username='', password='', email='', location='', note='', createDate=None, endDate=None):
        SecretObject.__init__(self, title, password, note, createDate, endDate)
        self.username = username
        self.email = email
        self.location = location
        
    def clone(self):
        retVal = PasswordObject()
        retVal.copyFrom(self)
        return retVal
    
    def copyFrom(self, passwordObject):
        SecretObject.copyFrom(self, passwordObject)
        self.username = passwordObject.username
        self.email = passwordObject.email
        self.location = passwordObject.location
    
    def setUsername(self, username):
        self.username = username
    def setEmail(self, email):
        self.email = email
    def setLocation(self, location):
        self.location = location

    def getUsername(self):
        return self.username
    def getEmail(self):
        return self.email
    def getLocation(self):
        return self.location
    def getAll(self):
        return [self.title, self.username, self.password, self.email, self.location, self.note, self.createDate]
