'''
Created on Jan 29, 2016

@author: groegert
'''
from .Cmd import Cmd

class DeleteSafeItemCmd(Cmd):
    '''
    deletes a safe item from the passwordsafe
    '''

    def __init__(self, passwordSafe, safeItem):
        '''
        Constructor
        '''
        Cmd.__init__(self, passwordSafe, safeItem)
        
    def doExecute(self):
        self.subject.removeSafeItem(self.val)
        f = self.val.getPasswordFile()
        f.setChanged(True)

    def canDo(self):
        return True
