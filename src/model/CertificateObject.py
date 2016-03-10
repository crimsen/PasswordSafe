'''
Created on Mar 7, 2016

@author: groegert
'''
from model.SecretObject import SecretObject

class CertificateObject(SecretObject):
    '''
    classdocs
    '''


    def __init__(self, title='', username='', password='', email='', location='', note='', createDate=None, endDate=None):
        SecretObject.__init__(self, title, password, note, createDate, endDate)
        
    def clone(self):
        retVal = CertificateObject()
        retVal.copyFrom(self)
        return retVal
    
    def copyFrom(self, certificateObject):
        SecretObject.copyFrom(self, certificateObject)
        