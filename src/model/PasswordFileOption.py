'''
Created on May 27, 2015

@author: thomas
'''

class PasswordFileOption(object):
    '''
    classdocs
    '''


    def __init__(self, filename, encodeId, isDefault=False, needBackup=False):
        '''
        Constructor
        '''
        self.filename = filename
        self.encodeId = encodeId
        self.isDefault = isDefault
        self.needBackup = needBackup
        # per default the ischanged is true to save always
        self.isChanged = True

    def getFilename(self):
        return self.filename
        