'''
Created on Jan 29, 2016

@author: groegert
'''
from model.CertificateObject import CertificateObject
from model.PasswordObject import PasswordObject
from model.SecretObjectEnum import  SecretObjectEnum

class SafeItem(object):
    '''
    Class that covers multiple SecretObjects to provide a history and
    covers the passwordFile this item is related to
    The current password is always secretObjects[0].
    The other items are history objects
    '''

    @staticmethod
    def getSecretObject(item):
        retVal = item
        if type(item) == SafeItem:
            retVal = item.getCurrentSecretObject()
        return retVal

    def __init__(self, secretObject, secretObjectEnum, history=[]):
        '''
        Constructor
        '''
        self.passwordFile = None
        self.secretObjectEnum = secretObjectEnum
        if isinstance(secretObject, list):
            self.secretObjects = secretObject
        else:
            self.secretObjects = [secretObject]
            self.secretObjects.extend(history)
    
    def clone(self):
        secretItem = self.secretObjects[0].clone()
        retVal = SafeItem(secretItem, self.secretObjectEnum)
        retVal.setPasswordFile(self.getPasswordFile())
        return retVal

    def setPasswordFile(self, passwordFile):
        self.passwordFile = passwordFile

    def getPasswordFile(self):
        return self.passwordFile
    
    def getCurrentSecretObject(self):
        return self.secretObjects[0]
    
    def getHistory(self):
        return self.secretObjects[1:]

    def addSecretObject(self, secretObject):
        self.secretObjects.insert(0, secretObject)

    def getTitle(self):
        return self.secretObjects[0].getTitle()
    
    def getType(self):
        return self.secretObjectEnum
            
        