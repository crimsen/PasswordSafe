'''
Created on Jul 14, 2015

@author: groegert
'''

import Tkinter as tk
from Tkinter import StringVar
from docutils.nodes import note

class PasswordForm(object):
    def __init__(self, parent):
        self.view = PasswordFormView(parent)
        self.controller = PasswordFormController(self.view, None)

    def getFrame(self):
        return self.view.frame;

    def validate(self):
        self.view.updateModel()
        
    def setTimeControl(self, timeControl):
        self.controller.setTimeControl(timeControl)

    def setMode(self, mode):
        self.view.setMode(mode)

class PasswordFormView(object):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        self.model = None
        self.varTitle = StringVar()
        self.varUsername = StringVar()
        self.varPassword = StringVar()
        self.varEmail = StringVar()
        self.varLocation = StringVar()
        self.__buildFrame__(parent)
        
    def __buildFrame__(self, parent):
        self.frame = tk.Frame(master=parent)
        
        frameLeft = tk.Frame(master=self.frame)
        self.labelTitle = tk.Label(master=frameLeft, text='Titel', anchor='w', font='Arial 20 bold')
        self.entryTitle = tk.Entry(master=frameLeft, textvariable=self.varTitle)
        self.labelUsername = tk.Label(master=frameLeft, text='Username', anchor='w', font='Arial 20 bold')
        self.entryUsername = tk.Entry(master=frameLeft, textvariable=self.varUsername)
        self.labelPassword = tk.Label(master=frameLeft, text='Passwort', anchor='w', font='Arial 20 bold')
        framePassword = tk.Frame(master=frameLeft)
        self.entryPassword = tk.Entry(master=framePassword, textvariable=self.varPassword)
        self.buttonPasswordCopy = tk.Button(master=framePassword, text='Copy', underline=0)
        self.labelEMail = tk.Label(master=frameLeft, text='E-Mail', anchor='w', font='Arial 20 bold')    
        self.entryEMail = tk.Entry(master=frameLeft, textvariable=self.varEmail)
        self.labelTitle.pack(side='top', padx=5, pady=5, fill='both')
        self.entryTitle.pack(side='top', padx=5, pady=5, fill='both')
        self.labelUsername.pack(side='top', padx=5, pady=5, fill='both')
        self.entryUsername.pack(side='top', padx=5, pady=5, fill='both')
        self.labelPassword.pack(side='top', padx=5, pady=5, fill='both')
        self.entryPassword.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        self.buttonPasswordCopy.pack(side='left', padx=5, pady=5)
        framePassword.pack(side='top', fill='both')
        self.labelEMail.pack(side='top', padx=5, pady=5, fill='both')
        self.entryEMail.pack(side='top', padx=5, pady=5, fill='both')  
        frameLeft.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        frameRight = tk.Frame(master=self.frame)
        self.labelLocation = tk.Label(master=frameRight, text='Location / URL', anchor='w', font='Arial 20 bold')
        self.entryLocation = tk.Entry(master=frameRight, textvariable=self.varLocation)
        self.labelNote = tk.Label(master=frameRight, text='Note', anchor='w', font='Arial 20 bold')
        self.textNote = tk.Text(master=frameRight, height=3, bd=2, relief='flat')
        self.labelLocation.pack(side='top', fill='both', padx=5, pady=5)
        self.entryLocation.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNote.pack(side='top', fill='both', padx=5, pady=5)
        self.textNote.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        frameRight.pack(side='left', fill='both', expand=True, padx=5, pady=5)
       
    def setMode(self, mode):
        if 'edit' != mode:
            self.buttonPasswordCopy.pack(side='left', padx=5, pady=5)
        else:
            self.buttonPasswordCopy.pack_forget()

    def updateFromModel(self, passwordObject):
        self.model = passwordObject
        self.updateTitle(passwordObject)
        self.updateUsername(passwordObject)
        self.updatePassword(passwordObject)
        self.updateEmail(passwordObject)
        self.updateLocation(passwordObject)
        self.updateNote(passwordObject)
    
    def updateTitle(self, passwordObj):
        self.updateVar(self.varTitle, passwordObj.getTitle())

    def updateUsername(self, passwordObj):
        self.updateVar(self.varUsername, passwordObj.getUsername())
    
    def updatePassword(self, passwordObj):
        self.updateVar(self.varPassword, passwordObj.getPassword())
    
    def updateEmail(self, passwordObj):
        self.updateVar(self.varEmail, passwordObj.getEmail())
    
    def updateLocation(self, passwordObj):
        self.updateVar(self.varLocation, passwordObj.getLocation())

    def updateNote(self, passwordObj):
        note = passwordObj.getNote()
        if None == note:
            note = ''
        self.textNote.delete(1.0, 'end')
        self.textNote.insert('end', note)

    def updateVar(self, var, text):
        if None == text:
            text = ''
        var.set(text)

    def updateModel(self):
        self.model.setTitle(self.varTitle.get())
        self.model.setUsername(self.varUsername.get())
        self.model.setPassword(self.varPassword.get())
        self.model.setEmail(self.varEmail.get())
        self.model.setLocation(self.varLocation.get())
        self.model.setNote(self.textNote.get('1.0', 'end'))

class PasswordFormController(object):
    def __init__(self, view, model):
        self.timeControl = None
        self.view = view
        self.model = model
        view.buttonPasswordCopy.bind('<1>', self.pressCopy)
        view.varTitle.trace('w', self.resetTime)
        view.varUsername.trace('w', self.resetTime)
        view.varPassword.trace('w', self.resetTime)
        view.varEmail.trace('w', self.resetTime)
        view.varLocation.trace('w', self.resetTime)
        view.textNote.bind('<KeyPress>', self.resetTime)

    def pressCopy(self):
        pass

    def resetTime(self, event, *args):
        if None != self.timeControl:
            self.timeControl.resetTime()
    
    def setTimeControl(self, timeControl):
        self.timeControl = timeControl

if __name__=='__main__':
    window = tk.Tk()
    window.title('PasswordForm')
    passwordForm = PasswordForm(window)
    passwordForm.getFrame().pack()
    window.mainloop()

