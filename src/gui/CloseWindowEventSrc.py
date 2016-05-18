'''
Created on May 13, 2016

@author: groegert
'''

from gui.ListenerCont import ListenerCont

class CloseWindowEventSrc(object):
    '''
    class that provides close window events and handling related listeners
    '''
    def __init__(self):
        self.listenerCont = ListenerCont()
    def addCloseWindowListener(self, listener):
        self.listenerCont.addListener(listener)
        return id(self)
    def removeCloseWindowListener(self, listener):
        self.listenerCont.removeListener(listener)
    def fireCloseWindow(self):
        self.listenerCont.fire(id(self))
