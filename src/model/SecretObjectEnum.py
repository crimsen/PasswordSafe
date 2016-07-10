'''
Created on Feb 17, 2016

@author: groegert
'''

from enum import Enum

class SecretObjectEnum(Enum):
    '''
    classdocs
    '''
    password = 1
    smime = 2
    gpg = 3
