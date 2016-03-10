'''
Created on Feb 17, 2016

@author: groegert
'''

import sys
if sys.hexversion >= 0x3040000:
    from enum import Enum
else:
    from flufl.enum import Enum

class SecretObjectEnum(Enum):
    '''
    classdocs
    '''
    password = 1
    smime = 2
    gpg = 3
