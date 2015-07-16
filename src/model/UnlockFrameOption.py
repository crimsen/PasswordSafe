'''
Created on Jul 13, 2015

@author: groegert
'''

class UnlockFrameOption(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.filterEntry = ""
        self.selectedPassword = ""
        self.checkTitle = True
        self.checkUsername = True
        self.checkPassowrd = False
        self.checkEmail = True
        self.checkLocation = True
        self.checkNote = True
