'''
Created on 28.03.2015

@author: crimsen
'''
import gui.PasswordForm
from gui.PasswordForm import PasswordFormContext
import sys
from edit.AddSafeItemCmd import AddSafeItemCmd
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk
from model.passObject import PasswordObject

class NewPassWindow(object):
    #Build a new Window for a new PasswordObject
    def __init__(self, context):
        self.context = context
        self.view = NewPasswordWindowView(context)
        self.model = context.master.createPasswordItem()
        self.controller = NewPasswordWindowController(self.view, self.model, context)

    def setTimeControl(self, timeControl):
        #TODO: deprecated, use context
        self.controller.setTimeControl(timeControl)

    def show(self):
        self.view.show()
    
    def close(self):
        self.view.close()

class NewPasswordWindowContext(object):
    def __init__(self, client, master, editingDomain):
        self.client = client
        self.master = master
        self.editingDomain = editingDomain
        
    def getClient(self):
        return self.client
    def getEditingDomain(self):
        return self.editingDomain
        
class NewPasswordWindowView(object):
        
    class PasswordFormContext(PasswordFormContext):
        def __init__(self, parentContext):
            PasswordFormContext.__init__(self, parentContext.client.context)

    def __init__(self, context):
        self.context = context
        self.__buildFrame__()
        
    def __buildFrame__(self):
        self.window = tk.Toplevel()
        self.window.title('New Password')
        self.window.geometry('640x400')
        parent = self.window
        self.form = gui.PasswordForm.PasswordForm(parent, NewPasswordWindowView.PasswordFormContext(self.context))
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
        
class NewPasswordWindowController(object):
    def __init__(self, view, model, context):
        self.view = view
        self.model = model
        self.client = context.getClient()
        self.editingDomain = context.getEditingDomain()
        view.buttonSave.configure(command=self.pressSave)
        view.buttonCancel.configure(comman=self.pressCancel)
        view.updateFromModel(model)
        #view.form.setClient(self)
        #view.form.setContext(self.client.getContext())
        self.view.window.focus_force()

    def setTimeControl(self, timeControl):
        self.view.form.setTimeControl(timeControl)

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
        self.view.form.validate()
        if None != self.editingDomain:
            self.editingDomain.executeCmd(AddSafeItemCmd(self.editingDomain.getModel(), self.model))
            if None != self.client:
                self.client.onSafeChanged()
        self.view.close()
    
    def copyToClipBoard(self, entry):
        if None != self.client:
            self.client.copyToClipBoard(entry)

if __name__=='__main__':
    test = NewPassWindow(None)
    test.show()
