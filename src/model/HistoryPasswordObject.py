'''
Created on 13.06.2015

@author: timgroger
'''
from model.passObject import PasswordObject
from datetime import datetime

class HistoryPasswordObject(PasswordObject):
    '''
    classdocs
    '''


    def __init__(self, title='', username='', password='', email='', location='', note='', endDate=''):
        '''
        Constructor
        '''
        PasswordObject.__init__(self, title, username, password, email, location, note)
        
        self.endDate = self.controlDate(endDate)
        
    def controlDate(self, endDate):
        if endDate == '':
            date = datetime.now()
            endDate = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
        return endDate
    
    def setEndDate(self, endDate):
        self.endDate = self.controlDate(endDate)
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