'''
Created on Jan 29, 2016

@author: groegert
'''
from model.CertificateObject import CertificateObject
from model.passObject import PasswordObject
from model.SecretObjectEnum import  SecretObjectEnum

class SafeItem(object):
    '''
    Class that covers multiple SecretObjects to provide a history and
    covers the passwordFile this item is related to
    The current password is always secretObjects[0].
    The other items are history objects
    '''

    def __init__(self, secretObject, history=[]):
        '''
        Constructor
        '''
        self.passwordFile = None
        if isinstance(secretObject, list):
            self.secretObjects = secretObject
        else:
            self.secretObjects = [secretObject]
            self.secretObjects.extend(history)
    
    def clone(self):
        secretItem = self.secretObjects[0].clone()
        retVal = SafeItem(secretItem)
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
        retVal = None
        obj = self.getCurrentSecretObject()
        if type(obj) == PasswordObject:
            retVal = SecretObjectEnum.password
        elif type(obj) == CertificateObject:
            retVal = SecretObjectEnum.smime
        return retVal
            
        