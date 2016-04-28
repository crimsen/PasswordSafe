'''
Created on Mar 7, 2016

@author: groegert
'''
from model.SecretObject import SecretObject

class CertificateObject(SecretObject):
    '''
    classdocs
    '''

    def __init__(self, title='', password='', note='', createDate=None, endDate=None):
        SecretObject.__init__(self, title, password, note, createDate, endDate)
        self.secretKey = None
        self.secretKeyFileName = ''
        self.publicKey = None
        self.publicKeyFileName = ''
        
    def clone(self):
        retVal = CertificateObject()
        retVal.copyFrom(self)
        return retVal
    
    def copyFrom(self, certificateObject):
        SecretObject.copyFrom(self, certificateObject)
        self.secretKey = certificateObject.secretKey
        self.secretKeyFileName = certificateObject.secretKeyFileName
        self.publicKey = certificateObject.publicKey
        self.publicKeyFileName = certificateObject.publicKeyFileName
        
    def getSecretKeyFileName(self):
        return self.secretKeyFileName
    def setSecretKeyFileName(self, fileName):
        self.secretKeyFileName = fileName
    def getSecretKey(self):
        return self.secretKey
    def setSecretKey(self, secretKey):
        self.secretKey = secretKey

    def getPublicKeyFileName(self):
        return self.publicKeyFileName
    def setPublicKeyFileName(self, fileName):
        self.publicKeyFileName = fileName
    def getPublicKey(self):
        return self.publicKey
    def setPublicKey(self, publicKey):
        self.publicKey = publicKey
        