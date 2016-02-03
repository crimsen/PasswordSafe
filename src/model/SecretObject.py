'''
Created on Jan 28, 2016

@author: groegert
'''
from datetime import date

class SecretObject(object):
    '''
    Base of the secrets that can be stored in the safe
    '''
    def __init__(self, title='', password='', note='', createDate=None, endDate=None):
        '''
        Constructor
        '''
        self.title = title
        self.password = password
        self.note = note
        self.createDate = createDate
        self.endDate = endDate
        
    def clone(self):
        retVal = SecretObject()
        retVal.copyFrom(self)
        return retVal
    
    def copyFrom(self, passwordObject):
        self.title = passwordObject.title
        self.password = passwordObject.password
        self.note = passwordObject.note
        self.createDate = passwordObject.createDate
        self.endDate = passwordObject.endDate

    def haveCreateDate(self):
        if self.createDate == None:
            self.createDate = date.today()
    def haveEndDate(self):
        if self.endDate == None:
            self.endDate = date.today()
    
    def setTitle(self, title):
        self.title = title
    def setPassword(self, password):
        self.password = password
    def setNote(self, note):
        self.note = note
    def setCreateDate(self, createDate):
        self.createDate = createDate
    def setEndDate(self, endDate):
        self.endDate = endDate

    def getTitle(self):
        return self.title
    def getPassword(self):
        return self.password
    def getNote(self):
        return self.note
    def getCreateDate(self):
        return self.createDate
    def getEndDate(self):
        return self.endDate
