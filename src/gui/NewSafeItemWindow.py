'''
Created on 28.03.2015

@author: crimsen
'''
from gui.PasswordForm import PasswordForm
from gui.PasswordForm import PasswordFormContext
import sys
from edit.AddSafeItemCmd import AddSafeItemCmd
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class NewSafeItemWindow(object):
    '''
    NewSafeItemWindow is a top level window to create new safe items.
    First it collects all data that are needed for a new safe item:
    - the type of the secret item
    - the file where the save item has to be stored
    - the data in the secret item
    All this data is stored in NewSafeItemWindowOption.
    When there is a lock in between the NewSafeItemWindow can be completely
    restored from NewSafeItemWindowOption.
    '''
    def __init__(self, context):
        self.context = context
        self.view = NewSafeItemWindowView(context)
        self.model = context.master.createPasswordItem()
        self.controller = NewSafeItemWindowController(self.view, self.model, context)

    def show(self):
        self.view.show()
    
    def close(self):
        self.view.close()

class NewSafeItemWindowContext(object):
    def __init__(self, client, master, editingDomain):
        self.client = client
        self.master = master
        self.editingDomain = editingDomain
    def getClient(self):
        return self.client
    def getEditingDomain(self):
        return self.editingDomain
        
class NewSafeItemWindowView(object):
        
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
        self.form = PasswordForm(parent, NewSafeItemWindowView.PasswordFormContext(self.context))
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
        
class NewSafeItemWindowController(object):
    def __init__(self, view, model, context):
        self.view = view
        self.model = model
        self.client = context.getClient()
        self.editingDomain = context.getEditingDomain()
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
        self.view.form.validate()
        if None != self.editingDomain:
            self.editingDomain.executeCmd(AddSafeItemCmd(self.editingDomain.getModel(), self.model))
            if None != self.client:
                self.client.onSafeChanged()
        self.view.close()
    
if __name__=='__main__':
    test = NewSafeItemWindow(None)
    test.show()
