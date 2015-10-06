'''
Created on 18.04.2015

@author: crimsen
'''
from __builtin__ import True

class PassSafeFilter(object):
    '''
    classdocs
    '''
 
    def __init__(self, passwordSafe):
        self.passwordSafe = passwordSafe
        self.filterstring = ''
        self.filterattribute = []
        self.filteredpasssafe = []
        
    def setFilterstring(self, keystring):
        self.filterstring = keystring
        self.doFilter()
    
    def setFilterattribute(self, attributlist):
        self.filterattribute = []
        self.filterattribute = [ attribut for attribut in attributlist ]
        for attribut in self.filterattribute:
            if attribut == '':
                self.filterattribute.remove(attribut)
    
    def doFilter(self):
        self.filteredpasssafe = []
        self.filteredpasssafe = [ po for po in self.passwordSafe.getSafe() if self.checkAttributes(po) ]
    
    def checkAttributes(self, po):
        if self.filterstring == '' or self.filterstring == None:
            return True
        else:
            for attribut in self.filterattribute:
                try:
                    if self.filterstring.lower() in getattr(po, str(attribut)).lower():
                        return True
                except:
                    pass
        return False
            
    def getSafe(self):
        return self.filteredpasssafe
    
    def printFilteredpasssafe(self):
        for po in self.filteredpasssafe:
            print(getattr(po, 'title'))
            print(getattr(po, 'username'))
            print('\n')
        
    def getTitle(self, index):
        return self.filteredpasssafe[index].getTitle()
    
    def getUsername(self, index):
        return self.filteredpasssafe[index].getUsername()
    
    def getPassword(self, index):
        return self.filteredpasssafe[index].getPassword()
    
    def getEmail(self, index):
        return self.filteredpasssafe[index].getEmail()
    
    def getLocation(self, index):
        return self.filteredpasssafe[index].getLocation()
    
    def getNote(self, index):
        return self.filteredpasssafe[index].getNote()