'''
Created on May 8, 2015

@author: groegert
'''
from GuiOption import GuiOption

class Option(object):
    '''
    This class is a container for all the options that should persist over sessions.
    It does NOT cover any intelligent methodes, it is just a stupid container for the option model. 
    '''
    
    def __init__(self):
        self.email = None
        self.emailOld = None
        self.files = []
        self.gui = GuiOption()
    
    def getEmail(self):
        return self.email

    def getEmailOld(self):
        return self.emailOld

    def setEmail(self, val):
        self.email = val
        
    def getFiles(self):
        return self.files

    def getDefaultPasswordFile(self):
        retVal = [i for i in self.files if i.isDefault]
        return retVal[0]
