'''
Created on Jul 7, 2016

@author: groegert
'''
import os

class Environment(object):
    '''
    classdocs
    '''
    profileDir = os.environ['HOME'] + '/.PasswordSafe'


    def __init__(self):
        '''
        Constructor
        '''
        
