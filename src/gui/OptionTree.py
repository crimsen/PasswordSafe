'''
Created on May 12, 2015

@author: thomas
'''
import ttk as tk
from TreeItem import TreeItem
from AccountPage import AccountPage
from FilesPage import FilesPage

class OptionTree(object):
    '''
    represents the tree on the left side of the option window
    it is a seperate object (not just a tk.Tree) because because it covers
    also building the tree and intelligent access
    '''

    def __init__(self, parent, option):
        '''
        Constructor
        '''
        self.option = option
        self.eventSink = []
        self.__buildFrame__(parent)
        self.updateWindow()
        
    def __buildFrame__(self, parent):
        self.frameMain = tk.Frame(master=parent)
        self.treeBox = tk.Treeview(master=self.frameMain, show="tree", select="browse")
        self.frameMain.pack(side='top', fill='y')
        self.treeBox.pack(side='left', fill='y')
        self.treeBox.bind("<<TreeviewSelect>>",self.itemSelected)

    def addEventSink(self, function):
        self.eventSink.append(function)

    def readFromOption(self):
        '''
        reads values from the option object and sets the ui according to the values
        '''
        self.content = []
        self.content.append(TreeItem("Account",self.option, AccountPage))
        #self.content.append(TreeItem("Files",self.option, FilesPage))
        self.loadTreeBox()

    def updateWindow(self):
        '''
        prepares the window with possible settings and updates the ui
        '''
        self.readFromOption()
        self.treeBox.selection_set(id(self.content[0]))

    def loadTreeBox(self):
        self.addChildItems('', self.content)
    
    def addChildItems(self, parent, children=[]):
        for item in children:
            itemId = id(item)
            self.treeBox.insert(parent, 'end', itemId, text=item.getName())
            self.addChildItems(itemId, item.getChildren())

    def itemSelected(self, event):
        itemId = int(self.treeBox.selection()[0])
        for sink in self.eventSink:
            sink(itemId)
    
    def getOptionPageDescription(self, itemId):
        retVal = None
        item = findItem(itemId, self.content)
        if None != item:
            retVal = (item.getOptionPage(), item.getModel())
        return retVal

def findItem(itemId, items):
    retVal = None
    for item in items:
        if itemId == id(item):
            retVal = item
            break
        retVal = findItem(itemId, item.children)
        if None != retVal:
            break
    return retVal
