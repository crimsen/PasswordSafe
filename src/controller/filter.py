'''
Created on 18.04.2015

@author: crimsen
'''
from __builtin__ import True

class PassSafeFilter(object):
    '''
    classdocs
    '''
 
    def __init__(self, passsafe):
        self.passsafe = passsafe
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
        self.filteredpasssafe = [ po for po in self.passsafe if self.checkAttributes(po) ]
    
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
            
    def getFilteredpasssafe(self):
        return self.filteredpasssafe
    
    def printFilteredpasssafe(self):
        for po in self.filteredpasssafe:
            print(getattr(po, 'title'))
            print(getattr(po, 'username'))
            print('\n')
        
    