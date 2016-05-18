'''
Created on May 13, 2016

@author: groegert
'''

class ListenerCont(object):
    '''
    container that stores listeners and provide firing events
    '''
    def __init__(self):
        self.listeners = []
    def addListener(self, listener):
        self.listeners.append(listener)
    def removeListener(self, listener):
        self.listeners.remove(listener)
    def fire(self, *param):
        for listener in self.listeners:
            listener(*param)
