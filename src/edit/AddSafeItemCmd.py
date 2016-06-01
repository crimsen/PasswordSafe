'''
Created on Feb 1, 2016

@author: groegert
'''
from edit.Cmd import Cmd

class AddSafeItemCmd(Cmd):
    '''
    classdocs
    '''


    def __init__(self, passwordSafe, passwordItem):
        Cmd.__init__(self, passwordSafe, passwordItem)
        '''
        Constructor
        '''

    def doExecute(self):
        self.subject.addSafeItem(self.val)
        f = self.val.getPasswordFile()
        if None == f:
            f = self.subject.option.getDefaultPasswordFile()
            self.val.setPasswordFile(f)
        f.setChanged(True)

    def canDo(self):
        return True
