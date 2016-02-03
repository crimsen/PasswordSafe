'''
Created on Jan 29, 2016

@author: groegert
'''

class Cmd(object):
    '''
    Base of all commands that can be executed via the editing domain
    '''

    def __init__(self, subject, val):
        '''
        Constructor
        '''
        self.subject = subject
        self.val = val
    def doExecute(self):
        pass
    def undoExecute(self):
        pass
    
    def canDo(self):
        return False
    def canUndo(self):
        return False

'''
    def markModified(self, passwordObject):
        passwordFile = passwordObject.getPasswordFile()
        self.markFileModified(passwordFile)

    def markFileModified(self, passwordFile):
        if None == passwordFile:
            passwordFile = self.option.getDefaultPasswordFile()
        passwordFile.setChanged(True)
'''