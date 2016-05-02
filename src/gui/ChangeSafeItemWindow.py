'''
Created on 16.04.2015

@author: crimsen
'''
from edit.SetSecretObjectCmd import SetSecretObjectCmd
from gui.CertificatePage import CertificatePage
from gui.CertificatePage import CertificatePageContext
from gui.PasswordForm import PasswordForm
from gui.PasswordForm import PasswordFormContext
from model.passObject import PasswordObject
import sys
from model.SecretObjectEnum import SecretObjectEnum
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class ChangeSafeItemWindow(object):
    #Build a new Window for a new PasswordObject
    def __init__(self, context):
        viewModel = context.getSafeItem().clone()
        viewModel.getCurrentSecretObject().createDate = None
        self.view = ChangeSafeItemWindowView(context)
        self.controller = ChangeSafeItemWindowController(self.view, viewModel, context)

    def show(self):
        self.view.show()
        
    def close(self):
        self.view.close()
    
class ChangeSafeItemWindowContext(object):
    def __init__(self, client, editingDomain, safeItem):
        self.client = client
        self.editingDomain = editingDomain
        self.safeItem = safeItem
    def getClient(self):
        return self.client
    def getEditingDomain(self):
        return self.editingDomain
    def getSafeItem(self):
        return self.safeItem
        
class ChangeSafeItemWindowView(object):
    
    class PasswordFormContext(PasswordFormContext):
        def __init__(self, parentContext):
            PasswordFormContext.__init__(self, parentContext.client.context)
            self.mode = 'edit'
    class CertificatePageContext(CertificatePageContext):
        def __init__(self, parentContext):
            CertificatePageContext.__init__(self, parentContext.client.context)
            self.mode = 'edit'
        
    def __init__(self, context):
        self.context = context
        self.__buildFrame__()
        
    def __buildFrame__(self):
        self.window = tk.Toplevel()
        self.window.geometry('640x400')
        parent = self.window
        itemType = self.getSafeItemType()
        if SecretObjectEnum.password == itemType:
            self.window.title('Change Password')
            self.form = PasswordForm(parent, ChangeSafeItemWindowView.PasswordFormContext(self.context))
        elif SecretObjectEnum.smime == itemType:
            self.window.title('Change SMime')
            self.form = CertificatePage(parent, ChangeSafeItemWindowView.CertificatePageContext(self.context))
        else:
            self.window.title('Change Unknown Type')
            self.form = None
        
        buttonFrame = tk.Frame(master=parent)
        self.buttonSave = tk.Button(master=buttonFrame, text='Save')
        self.buttonCancel = tk.Button(master=buttonFrame, text='Cancel')
        
        self.form.getFrame().pack(side='top', fill='both', padx=5, pady=5, expand=True)
        buttonFrame.pack(side='bottom', anchor='e')
        self.buttonCancel.pack(side='right', fill='both', padx=5, pady=5)
        self.buttonSave.pack(side='right', fill='both', padx=5, pady=5)
    def updateFromModel(self, safeItem):
        self.form.setModel(safeItem)
    def show(self):
        pass
    def close(self):
        self.window.destroy()
    def getSafeItemType(self):
        return self.context.getSafeItem().getType()
        
class ChangeSafeItemWindowController(object):
    def __init__(self, view, model, context):
        self.view = view
        self.model = model
        self.client = context.getClient()
        self.editingDomain = context.getEditingDomain()
        self.origModel = context.getSafeItem()
        view.buttonSave.configure(command=self.pressSave)
        view.buttonCancel.configure(comman=self.pressCancel)
        view.updateFromModel(model)
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
    test = ChangeSafeItemWindow(None)
    test.show()
