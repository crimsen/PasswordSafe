'''
Created on 28.03.2015

@author: crimsen
'''
from datetime import date

class PasswordObject(object):


    def __init__(self, title='', username='', password='', email='', location='', note='', createDate=None):
        self.passwordFile = None
        self.title = title
        self.username = username
        self.password = password
        self.email = email
        self.location = location
        self.note = note
        self.createDate = createDate
        
    def haveCreateDate(self):
        if self.createDate == None:
            self.createDate = date.today()
    
    def copyFrom(self, passwordObject):
        self.passwordFile = passwordObject.passwordFile
        self.title = passwordObject.title
        self.username = passwordObject.username
        self.password = passwordObject.password
        self.email = passwordObject.email
        self.location = passwordObject.location
        self.note = passwordObject.note
        self.createDate = passwordObject.createDate
    
    def setPasswordFile(self, passwordFile):
        self.passwordFile = passwordFile
    def setTitle(self, title):
        self.title = title
    def setUsername(self, username):
        self.username = username
    def setPassword(self, password):
        self.password = password
    def setEmail(self, email):
        self.email = email
    def setLocation(self, location):
        self.location = location
    def setNote(self, note):
        self.note = note
    def setCreateDate(self, createDate):
        self.createDate = createDate
    
    def getPasswordFile(self):
        return self.passwordFile
    def getTitle(self):
        return self.title
    def getUsername(self):
        return self.username
    def getPassword(self):
        return self.password
    def getEmail(self):
        return self.email
    def getLocation(self):
        return self.location
    def getNote(self):
        return self.note
    def getCreateDate(self):
        return self.createDate
    def getAll(self):
        return [self.title, self.username, self.password, self.email, self.location, self.note, self.createDate]
        