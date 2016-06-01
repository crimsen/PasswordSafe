'''
Created on 10.04.2015

@author: crimsen
'''
from gui.MasterDetailsForm import MasterDetailsForm
from gui.MasterDetailsForm import MasterDetailsFormContext
from gui.MasterDetailsForm import MasterDetailsFormController
from gui.MasterDetailsForm import MasterDetailsFormView
from gui.MessageWindow import MessageWindow
from gui.OptionTree import OptionTree
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class OptionWindow(MasterDetailsForm):
    '''
    classdocs
    '''
    def __init__(self, option, controller):
        context = OptionWindowContext(controller)
        MasterDetailsForm.__init__(self, context, option)
        self.viewModel.itemId = 0
        self.view = OptionWindowView(self.context, self.viewModel)
        self.controller = OptionWindowController(self.view, self.viewModel, self.context)
        
    def show(self):
        # TODO: eliminate
        self.view.show()

class OptionWindowContext(MasterDetailsFormContext):
    def __init__(self, controller):
        MasterDetailsFormContext.__init__(self)
        self.controller = controller
    def getMainController(self):
        return self.controller

class OptionWindowView(MasterDetailsFormView):
    def __init__(self, context, viewModel):
        MasterDetailsFormView.__init__(self, context, viewModel)
        self.__buildFrame__(None)
    def __buildFrame__(self, parent):
        self.optionWindow = tk.Toplevel()
        self.optionWindow.title('Preferences')
        self.frameMain = tk.Frame(master=self.optionWindow)
        self.tree = OptionTree(self.frameMain, self.viewModel)
        MasterDetailsFormView.__buildFrame__(self, self.frameMain)
        self.formFrame = tk.Frame(master=self.frameMain)
        self.buttonSave = tk.Button(master=self.frameMain, text='Save')
        self.buttonCancel = tk.Button(master=self.frameMain, text='Cancel')
        self.__packFrame__() 
    
    def __packFrame__(self):
        self.frameMain.pack(side='top', fill='both', expand=True)
        self.tree.frameMain.pack(side='left', fill='y')
        MasterDetailsFormView.__packFrame__(self)
        self.buttonSave.pack(side='right', anchor='se', padx=5, pady=5)
        self.buttonCancel.pack(side='right', anchor='se', padx=5, pady=5)

    def show(self):
        pass
    def close(self):
        self.optionWindow.destroy()
    
    def updateFromModel(self):
        self.updatePages()
        childViewModel = self.getChildModel()
        self.currentPage[1].setModel(childViewModel)
        self.finishCurrentPagePacked()
    def updatePages(self):
        pageId = self.viewModel.itemId
        page = None
        if pageId in self.pages:
            page = self.pages[pageId]
        if None == page:
            pageDescription = (None, None)
            pageDescription = self.tree.getOptionPageDescription(pageId)
            page = self.buildFormPage(pageDescription)
            self.pages[pageId] = page
        self.setCurrentPageUnpacked(page)
    def getChildModel(self):
        retVal = self.tree.getModel(self.viewModel.itemId)
        return retVal

class OptionWindowController(MasterDetailsFormController):
    def __init__(self, view, model, context):
        MasterDetailsFormController.__init__(self, view, model, context)
        view.buttonSave.configure(command=self.pressSave)
        view.buttonCancel.configure(command=self.pressCancel)
        view.tree.addEventSink(self.itemSelected)
    def apply(self):
        '''
        apply the values of all pages that had been displayed.
        '''
        for page in self.view.pages.values():
            page[1].apply()

    def pressCancel(self):
        self.view.close()
    
    def pressSave(self):
        # TODO: here we should first validate all pages and in case of an invalid setting we should display an error
        try:
            self.apply()
            self.context.getMainController().controlOptionSave()
            self.view.optionWindow.destroy()
        except:
            MessageWindow('Incorrect Setting', 'Any setting is incorrect. Check if you did choose an account.')
            
#http://stackoverflow.com/questions/16514617/python-tkinter-notebook-widget
    def itemSelected(self, itemId):
        self.model.itemId = itemId
        self.view.updateFromModel()
