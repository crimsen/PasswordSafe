'''
Created on May 3, 2016

@author: groegert
'''
from model.PasswordSafe import PasswordSafe
from model.SafeItem import SafeItem

class PasswordSafeContentProvider(object):
    '''
    default content provider of the password safe
    '''

    def __init__(self, afilter=None):
        self.filter = afilter
    def getChildren(self, item):
        retVal = None
        if type(item) == PasswordSafe:
            if None != self.filter:
                retVal = self.filter.doFilterSafe(item.getSafe())
            else:
                retVal = item.getSafe()
        elif type(item) == SafeItem:
            retVal = item.getHistory()
        return retVal
    def canFilter(self):
        return None != self.filter
    def setFilterString(self, filterString):
        self.filter.setFilterString(filterString)
