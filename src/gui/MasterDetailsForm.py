'''
Created on Mar 29, 2016

@author: groegert
'''
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class MasterDetailsForm(object):
    '''
    classdocs
    '''
    def __init__(self, context, viewModel=None):
        '''
        Constructor
        '''
        self.context = context
        self.viewModel = viewModel
        #create the view
        #create the controller

class MasterDetailsFormContext(object):
    '''
    class covers all functions and objects that are needed
    by MasterDetailsForm*-classes from the frame
    '''
    def __init__(self):
        pass

class MasterDetailsFormView(object):
    def __init__(self, context, viewModel):
        self.context = context
        self.viewModel = viewModel        
        self.pages = {}
        self.currentPage = None
        self.lastPage = None
    def __buildFrame__(self, parent):
        '''
        function builds all the visible elements for this master detail
        '''
        self.formFrame = tk.Frame(master=parent)
    def __packFrame__(self):
        self.finishCurrentPagePacked()
        self.formFrame.pack(side='top', fill='both', padx=5, pady=5, expand=True)
    def setCurrentPageUnpacked(self, page):
        '''
        do not influence UI
        update variables only
        '''
        self.lastPage = self.currentPage # safe the current page for later packing
        self.currentPage = page
    def finishCurrentPagePacked(self):
        '''
        ensures the correct form is packed
        '''
        if self.lastPage == self.currentPage:
            self.lastPage = None
        else:
            if None != self.lastPage:
                self.lastPage[0].pack_forget()
                self.lastPage = None
            self.currentPage[0].pack(fill='both', expand=True)
    def addPage(self, page):
        self.pages.append(page)
    def buildFormPage(self, pageDescription):
        (pageType, context) = pageDescription
        visibilityFrame = tk.Frame(master=self.formFrame)
        formPage = pageType(visibilityFrame, context)
        return (visibilityFrame, formPage)

class MasterDetailsFormController(object):
    def __init__(self, view, model, context):
        self.view = view
        self.model = model
        self.context = context
