'''
Created on Mar 16, 2016

@author: groegert
'''

class NewSafeItemWindowOption(object):
    '''
    these are the options / model that are needed to safe and restore gui.NewSafeItemWindow
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.canChangeSafeItemType = True
        self.currentPage = 0
        self.safeItemType = None
        self.safeItem = None
