'''
Created on May 27, 2015

@author: thomas
'''

class PasswordFileOption(object):
    '''
    classdocs
    '''
    defaultVersion = 2

    def __init__(self, filename, encodeId, isDefault=False, needBackup=False, version=defaultVersion):
        '''
        Constructor
        '''
        self.filename = filename
        self.encodeId = encodeId
        self.isDefault = isDefault
        self.needBackup = needBackup
        self.version = version
        self.loadVersion = 0
        # per default the ischanged is true to save always
        self.resetChanged()

    def getFilename(self):
        return self.filename
    
    def getEncodeId(self):
        return self.encodeId
    
    def getLabel(self):
        retVal = self.filename
        if None == retVal:
            retVal = 'Default'
        return retVal
    
    def getVersion(self):
        return self.version
    
    def getLoadVersion(self):
        return self.loadVersion
    def setLoadVersion(self, version):
        self.loadVersion = version

    def setChanged(self, val):
        self.isChanged = val

    def resetChanged(self):
        self.isChanged = False
    