'''
Created on 13.06.2015

@author: timgroger
'''
from model.passObject import PasswordObject
from datetime import date

class HistoryPasswordObject(PasswordObject):
    '''
    classdocs
    '''


    def __init__(self, title='', username='', password='', email='', location='', note='', createDate=None,endDate=None):
        '''
        Constructor
        '''
        PasswordObject.__init__(self, title, username, password, email, location, note, createDate)
        
        self.endDate = endDate
        
    def haveEndDate(self):
        if self.endDate == None:
            self.endDate = date.today()
    
    def setEndDate(self, endDate):
        self.endDate = endDate
    def getEndDate(self):
        return self.endDate
    
if __name__=='__main__':
    passw = HistoryPasswordObject('Title', 'Username', 'Password', 'Email', 'Location', 'Das\nist\neine\nNote')
    
    print passw.getTitle()
    print passw.getUsername()
    print passw.getPassword()
    print passw.getEmail()
    print passw.getLocation()
    print passw.getNote()
    print passw.getEndDate()