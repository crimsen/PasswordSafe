'''
Created on 28.03.2015

@author: crimsen
'''

class PasswordObject(object):


    def __init__(self, title, username, password, email, location, note):
        self.passwordFile = None
        self.title = title
        self.username = username
        self.password = password
        self.email = email
        self.location = location
        self.note = note
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
    def getAll(self):
        return [self.title, self.username, self.password, self.email, self.location, self.note]
        