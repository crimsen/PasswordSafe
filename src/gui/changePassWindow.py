'''
Created on 16.04.2015

@author: crimsen
'''
import gui.PasswordForm
from model.passObject import PasswordObject
import sys
from edit.SetSecretObjectCmd import SetSecretObjectCmd
from gui.CertificatePage import CertificatePageContext
from gui.PasswordForm import PasswordFormContext
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class ChangePassWindow(object):
    #Build a new Window for a new PasswordObject
    def __init__(self, context):
        self.view = ChangePasswordWindowView(context)
        self.model = context.getPasswordItem().clone()
        self.model.getCurrentSecretObject().createDate = None
        self.controller = ChangePasswordWindowController(self.view, self.model, context)

    def show(self):
        self.view.show()
        
    def close(self):
        self.view.close()
    
class ChangePasswordWindowContext(object):
    def __init__(self, client, editingDomain, passwordItem):
        self.client = client
        self.editingDomain = editingDomain
        self.passwordItem = passwordItem
    def getClient(self):
        return self.client
    def getEditingDomain(self):
        return self.editingDomain
    def getPasswordItem(self):
        return self.passwordItem
        
class ChangePasswordWindowView(object):
    
    class PasswordFormContext(PasswordFormContext):
        def __init__(self, parentContext):
            PasswordFormContext.__init__(self, parentContext.client.context)
    class CertificatePageContext(CertificatePageContext):
        def __init__(self, parentContext):
            CertificatePageContext.__init__(self, parentContext.client.context)
        
    def __init__(self, context):
        self.context = context
        self.__buildFrame__()
        
    def __buildFrame__(self):
        self.window = tk.Toplevel()
        self.window.title('Change Password')
        self.window.geometry('640x400')
        parent = self.window
        self.form = gui.PasswordForm.PasswordForm(parent, ChangePasswordWindowView.PasswordFormContext(self.context))
        self.form.setMode('edit')
        
        buttonFrame = tk.Frame(master=parent)
        self.buttonSave = tk.Button(master=buttonFrame, text='Save')
        self.buttonCancel = tk.Button(master=buttonFrame, text='Cancel')
        
        self.form.getFrame().pack(side='top', fill='both', padx=5, pady=5, expand=True)
        buttonFrame.pack(side='bottom', anchor='e')
        self.buttonCancel.pack(side='right', fill='both', padx=5, pady=5)
        self.buttonSave.pack(side='right', fill='both', padx=5, pady=5)

    def updateFromModel(self, passwordObject):
        self.form.setModel(passwordObject)

    def show(self):
        self.window.mainloop()
        
    def close(self):
        self.window.destroy()
        
class ChangePasswordWindowController(object):
    def __init__(self, view, model, context):
        self.view = view
        self.model = model
        self.client = context.getClient()
        self.editingDomain = context.getEditingDomain()
        self.origModel = context.getPasswordItem()
        view.buttonSave.configure(command=self.pressSave)
        view.buttonCancel.configure(comman=self.pressCancel)
        view.updateFromModel(model)
        #view.form.setContext(self.client.getContext())
        self.view.window.focus_force()

    def pressCancel(self):
        '''
        Destroy the widget
        '''
        self.view.close()
    
    def pressSave(self):
        '''
        Set a new passwordobject
        And destroy the widget
        '''
        self.view.form.apply()
        if None != self.editingDomain:
            self.editingDomain.executeCmd(SetSecretObjectCmd(self.origModel, self.model))
            if None != self.client:
                self.client.onSafeChanged()
        self.view.close()

    def copyToClipBoard(self, entry):
        if None != self.client:
            self.client.copyToClipBoard(entry)

if __name__=='__main__':
    test = ChangePassWindow(None)
    test.show()
