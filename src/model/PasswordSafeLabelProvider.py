'''
Created on May 3, 2016

@author: groegert
'''
from model.SafeItem import SafeItem
from model.SecretObject import SecretObject

class PasswordSafeLabelProvider(object):
    '''
    default label provider for the password safe
    '''

    def __init__(self):
        pass
    def getLabel(self, item):
        retVal = ''
        if type(item) == SafeItem:
            retVal = item.getTitle()
        elif isinstance(item, SecretObject):
            retVal = item.getEndDate().isoformat()
        return retVal