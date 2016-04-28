'''
Created on Feb 11, 2016

@author: groegert
'''
from model.SecretObject import SecretObject

class XmlMapping(object):
    '''
    classdocs
    '''

    title = 'title'
    password = 'password'
    note = 'note'
    createDate = 'createdate'
    endDate = 'enddate'
    version = 'version'
    type = 'type'
    username = 'username'
    email = 'email'
    location = 'location'
    
    secretObject = 'secretobject'
    safeItem = 'safe'

    fileName = 'filename'
    secretKey = 'secretkey'
    publicKey = 'publickey'

    def __init__(self):
        '''
        Constructor
        '''
    
    def getElementName(self, item):
        retVal = ''
        if type(item) is SecretObject:
            retVal = self.secretObject
        return retVal
