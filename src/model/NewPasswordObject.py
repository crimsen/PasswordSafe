'''
Created on 13.06.2015

@author: timgroger
'''
from model.passObject import PasswordObject


class NewPasswordObject(PasswordObject):
    '''
    classdocs
    '''


    def __init__(self, title='', username='', password='', email='', location='', note='', createDate=None, history=[]):
        PasswordObject.__init__(self, title, username, password, email, location, note, createDate)
        self.history = history
        
    def setHistory(self, history):
        self.history = history
    
    def addHistory(self, history):
        self.history.append(history)
        
    def getHistory(self):
        return self.history
        