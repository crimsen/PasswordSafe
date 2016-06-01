'''
Created on Mar 15, 2016

@author: groegert
'''
from gui.CloseWindowEventSrc import CloseWindowEventSrc
from gui.MasterDetailsForm import MasterDetailsForm
from gui.MasterDetailsForm import MasterDetailsFormView
from gui.MasterDetailsForm import MasterDetailsFormController
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class Wizard(MasterDetailsForm):
    '''
    Wizard is a base class for top level windows to enter data in
    multiple formpages in a sequence.
    '''
    def __init__(self, context, model):
        MasterDetailsForm.__init__(self, context, model)
        
class WizardView(MasterDetailsFormView):
    def __init__(self, context, viewModel):
        MasterDetailsFormView.__init__(self, context, viewModel)
    def __buildFrame__(self, parent=None):
        self.window = tk.Toplevel()
        self.window.title('New Password')
        self.window.geometry('640x400')
        MasterDetailsFormView.__buildFrame__(self, self.window)
        self.buttonFrame = tk.Frame(master=self.window)
        self.buttonBack = tk.Button(master=self.buttonFrame, text='Back')
        self.buttonNext = tk.Button(master=self.buttonFrame, text='Next')
        self.buttonApply = tk.Button(master=self.buttonFrame, text='Save')
        self.buttonCancel = tk.Button(master=self.buttonFrame, text='Cancel')

    def __packFrame__(self):
        self.buttonFrame.pack(side='bottom', anchor='e')
        self.buttonCancel.pack(side='right', fill='both', padx=5, pady=5)
        self.updateButtonFrame()
        MasterDetailsFormView.__packFrame__(self)
        
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
        
class WizardController(MasterDetailsFormController, CloseWindowEventSrc):
    def __init__(self, view, model, context):
        CloseWindowEventSrc.__init__(self)
        MasterDetailsFormController.__init__(self, view, model, context)
        self.client = context.getClient()
        self.editingDomain = context.getEditingDomain()
        view.buttonApply.configure(command=self.pressSave)
        view.buttonCancel.configure(comman=self.pressCancel)
        view.buttonNext.configure(command=self.pressNext)
        view.buttonBack.configure(command=self.pressPrev)
        self.view.window.focus_force()
        self.view.window.protocol("WM_DELETE_WINDOW",self.closeWindow)

    def closeWindow(self):
        CloseWindowEventSrc.fireCloseWindow(self)
        self.view.close()

    def pressCancel(self):
        '''
        Destroy the widget
        '''
        self.closeWindow()
    
    def pressSave(self):
        self.closeWindow()
    def pressNext(self):
        pass
    def pressPrev(self):
        pass
