'''
Created on May 3, 2016

@author: groegert
'''

import sys
if sys.hexversion >= 0x3000000:
    import tkinter.ttk as tk
    from tkinter import StringVar
else:
    import ttk as tk
    from Tkinter import StringVar

class TreeView(object):
    '''
    class that represents a tree, 
    based on a model, contentprovider and labelprovider
    '''
    def __init__(self, context):
        self.view = TreeViewView(context)
        self.controller = TreeViewController(self.view, context)
    def setContentProvider(self, contentProvider):
        self.view.setContentProvider(contentProvider)
    def setLabelProvider(self, labelProvider):
        self.view.setLabelProvider(labelProvider)
    def setModel(self, model):
        self.controller.setModel(model)
    def setFocus(self):
        self.controller.setFocus()
    def getFrame(self):
        return self.view.frameMain
    def addEventSink(self, function):
        self.controller.addEventSink(function)
        
class TreeViewContext(object):
    def __init__(self, parent):
        self.parent = parent
    def getParent(self):
        return self.parent

class TreeViewView(object):
    def __init__(self, context):
        self.context = context
        self.model = None
        self.contentProvider = None
        self.labelProvider = None
        self.itemMap = {}
        self.filterEntry = StringVar()
        self.__buildFrame__(context.getParent())
    def __buildFrame__(self, parent):
        self.frameMain = tk.Frame(master=parent)
        self.__buildFilterFrame__(self.frameMain)
        self.treeBox = tk.Treeview(master=self.frameMain, show="tree", select="browse")
        self.scrollbar = tk.Scrollbar(master=self.frameMain)
        self.treeBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.treeBox.yview)

        self.frameMain.pack(side='top', fill='y')
        self.treeBox.pack(side='left', fill='y')
        self.scrollbar.pack(side='left', fill='y')
    def __buildFilterFrame__(self, parent):
        self.entryFilter = tk.Entry(master=parent, textvariable=self.filterEntry)
        self.entryFilter.pack(side='top', fill='both')
    def setContentProvider(self, contentProvider):
        self.contentProvider = contentProvider
        self.updateFromModel(self.model)
    def setLabelProvider(self, labelProvider):
        self.labelProvider = labelProvider
        self.updateFromModel(self.model)
    def updateFromModel(self, model):
        children = self.treeBox.get_children()
        if 0 != len(children):
            self.treeBox.delete(*children)
            self.itemMap = {}
        self.model = model
        if None != model and None != self.contentProvider and None != self.labelProvider:
            self.addChildItems('', model)
            children = self.treeBox.get_children()
            if 0 != len(children):
                self.treeBox.selection_set(children[0])
    def addChildItems(self, parent, model):
        children = self.contentProvider.getChildren(model)
        if None != children:
            for item in children:
                label = self.labelProvider.getLabel(item)
                itemId = id(item)
                self.itemMap[itemId] = item
                self.treeBox.insert(parent, 'end', itemId, text=label)
                self.addChildItems(itemId, item)

class TreeViewController(object):
    def __init__(self, view, context):
        self.eventSink = []
        self.model = None
        self.view = view
        self.context = context
        view.treeBox.bind("<<TreeviewSelect>>",self.itemSelected)
        view.entryFilter.bind('<Up>', self.onEntryFilterUp)
        view.entryFilter.bind('<Down>', self.onEntryFilterDown)
        view.filterEntry.trace('w', self.onFilterChanged)
    def setModel(self, model):
        self.model = model
        self.view.updateFromModel(model)
    def setFocus(self):
        self.view.entryFilter.focus_force()
    def addEventSink(self, function):
        self.eventSink.append(function)
    def itemSelected(self, event):
        itemId = int(self.view.treeBox.selection()[0])
        item = self.view.itemMap[itemId]
        for sink in self.eventSink:
            sink(item)
    def onEntryFilterUp(self, event):
        selection = self.view.treeBox.selection()
        if 0 != len(selection):
            newSelection = self.view.treeBox.prev(selection[0])
            if '' != newSelection:
                self.view.treeBox.selection_set(newSelection)
    def onEntryFilterDown(self, event):
        selection = self.view.treeBox.selection()
        if 0 != len(selection):
            newSelection = self.view.treeBox.next(selection[0])
            if '' != newSelection:
                self.view.treeBox.selection_set(newSelection)
    def onFilterChanged(self, *args):
        contentProvider = self.view.contentProvider
        if None != contentProvider and contentProvider.canFilter():
            filterString = self.view.filterEntry.get()
            contentProvider.setFilterString(filterString)
            self.view.updateFromModel(self.model)
