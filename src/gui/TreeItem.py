'''
Created on May 13, 2015

@author: thomas
'''

class TreeItem(object):
    '''
    represents an entry in a tree, with a name, content and childrens
    '''


    def __init__(self, name, model, optionPage, children=[]):
        '''
        Constructor
        '''
        self.name = name
        self.model = model
        self.optionPage = optionPage
        self.children = children
    
    def getName(self):
        return self.name
    
    def getModel(self):
        return self.model
    
    def getChildren(self):
        return self.children
    
    def getOptionPage(self):
        return self.optionPage