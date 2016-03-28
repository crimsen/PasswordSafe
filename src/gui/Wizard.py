'''
Created on Mar 15, 2016

@author: groegert
'''
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class Wizard(object):
    '''
    Wizard is a base class for top level windows to enter data in
    multiple formpages in a sequence.
    '''
    def __init__(self, context, model):
        '''
        Constructor
        '''
        self.context = context
        self.model = model
        
class WizardView(object):
    def __init__(self, context, viewModel):
        self.context = context
        self.viewModel = viewModel
        self.pages = {}
        self.currentPage = None
    def __buildFrame__(self):
        self.window = tk.Toplevel()
        self.window.title('New Password')
        self.window.geometry('640x400')
        self.formFrame = tk.Frame(master=self.window)
        self.buttonFrame = tk.Frame(master=self.window)
        self.buttonBack = tk.Button(master=self.buttonFrame, text='Back')
        self.buttonNext = tk.Button(master=self.buttonFrame, text='Next')
        self.buttonApply = tk.Button(master=self.buttonFrame, text='Save')
        self.buttonCancel = tk.Button(master=self.buttonFrame, text='Cancel')

    def __packFrame__(self):
        self.formFrame.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        self.currentPage[0].pack(fill='both', expand=True)
        self.buttonFrame.pack(side='bottom', anchor='e')
        self.buttonCancel.pack(side='right', fill='both', padx=5, pady=5)
        self.updateButtonFrame()
        
    def updateButtonFrame(self):
        '''
        modifies the buttons on the bottom according to count of pages and current page that
        the buttons display the correct labels 'back', 'next', <do something>, 'cancel'
        '''
        # unpack the all the buttons first
        self.buttonBack.pack_forget()
        self.buttonNext.pack_forget()
        self.buttonApply.pack_forget()
        # from right to left
        if 0 < len(self.pages):
            if self.canApply():
                self.buttonApply.pack(side='right', fill='both', padx=5, pady=5)
            if self.hasNextPage():
                self.buttonNext.pack(side='right', fill='both', padx=5, pady=5)
            if self.hasPrevPage():
                self.buttonBack.pack(side='right', fill='both', padx=5, pady=5)
        
    def show(self):
        #self.window.mainloop()
        pass
    def close(self):
        self.window.destroy()
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
    def canApply(self):
        '''
        should be overwritten by child to specify whether the 'apply'-button should be displayed
        '''
        return False
    def hasNextPage(self):
        '''
        should be overwritten by child to specify whether the 'next'-button should be displayed
        '''
        return False
    def hasPrevPage(self):
        '''
        should be overwritten by child to specify whether the 'prev'-button should be displayed
        '''
        return False
        
class WizardController(object):
    def __init__(self, view, model, context):
        self.view = view
        self.model = model
        self.context = context
        self.client = context.getClient()
        self.editingDomain = context.getEditingDomain()
        view.buttonApply.configure(command=self.pressSave)
        view.buttonCancel.configure(comman=self.pressCancel)
        view.buttonNext.configure(command=self.pressNext)
        view.buttonBack.configure(command=self.pressPrev)
        self.view.window.focus_force()

    def pressCancel(self):
        '''
        Destroy the widget
        '''
        self.view.close()
    
    def pressSave(self):
        self.view.close()
    def pressNext(self):
        pass
    def pressPrev(self):
        pass
