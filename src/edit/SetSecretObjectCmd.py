'''
Created on Jan 29, 2016

@author: groegert
'''
from edit.Cmd import Cmd
from datetime import date

class SetSecretObjectCmd(Cmd):
    '''
    this class sets a new
    '''


    def __init__(self, safeItem, secretObject):
        '''
        Constructor
        '''
        Cmd.__init__(self, safeItem, secretObject)
    
    def doExecute(self):
        d = date.today()
        orig = self.subject.getCurrentSecretObject()
        orig.setEndDate(d)
        val = self.val.getCurrentSecretObject()
        val.setCreateDate(d)
        self.subject.addSecretObject(val)
        f = self.subject.getPasswordFile()
        f.setChanged(True)
        fnew = self.val.getPasswordFile()
        if fnew != f:
            fnew.setChanged(True)
            self.subject.setPasswordFile(fnew)
    
    def canDo(self):
        return True
        