'''
Created on Jul 14, 2015

@author: groegert
'''

from EmptyPage import EmptyPage
import webbrowser
import sys
if sys.hexversion >= 0x3000000:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import StringVar
else:
    import Tkinter as tk
    import ttk as ttk
    from Tkinter import StringVar

class PasswordForm(EmptyPage):

    @staticmethod
    def createContext(parentContext):
        return PasswordFormContext(parentContext)

    def __init__(self, parent, context):
        self.view = PasswordFormView(parent)
        self.controller = PasswordFormController(self.view, context)

    def apply(self):
        self.controller.validate()

    def getFrame(self):
        return self.view.frame;

    def validate(self):
        #TODO: deprecated, use apply
        self.apply()
        
    def setTimeControl(self, timeControl):
        #TODO: deprecated, use context.getTimeControl()
        self.controller.setTimeControl(timeControl)

    def setClient(self, client):
        #TODO: deprecated, use context.getClient() / context.getClipBoard()
        self.controller.setClient(client)

    def setContext(self, context):
        self.controller.setContext(context)

    def setMode(self, mode):
        self.view.setMode(mode)
        self.controller.setMode(mode)
        
    def setModel(self, model):
        self.controller.setModel(model)
        self.view.updateFromModel(model)

class PasswordFormContext(object):
    def __init__(self, parentContext):
        self.parentContext = parentContext
    def getTimeControl(self):
        return self.parentContext.getTimeControl()
    def getClipBoard(self):
        return self.parentContext.getClipBoard()
    def getPasswordFiles(self):
        return self.parentContext.getOption().getFiles()

class PasswordFormView(object):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        self.comboFilePacked = False
        self.model = None
        self.varTitle = StringVar()
        self.varUsername = StringVar()
        self.varPassword = StringVar()
        self.varEmail = StringVar()
        self.varLocation = StringVar()
        self.mode = 'normal'
        self.__buildFrame__(parent)
        self.setMode(self.mode)
        
    def __buildFrame__(self, parent):
        self.frame = tk.Frame(master=parent)
        
        self.comboFile = ttk.Combobox(master=self.frame, state='readonly')
        self.showComboFile()
        frameLeft = tk.Frame(master=self.frame)
        self.labelTitle = tk.Label(master=frameLeft, text='Titel', anchor='w', font='Arial 20 bold')
        self.entryTitle = tk.Entry(master=frameLeft, textvariable=self.varTitle)
        self.labelUsername = tk.Label(master=frameLeft, text='Username', anchor='w', font='Arial 20 bold')
        self.entryUsername = tk.Entry(master=frameLeft, textvariable=self.varUsername)
        self.labelPassword = tk.Label(master=frameLeft, text='Password', anchor='w', font='Arial 20 bold')
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
        self.frame.pack(side='top', fill='both', expand=True)
       
    def setMode(self, mode):
        self.mode = mode
        if 'edit' != mode:
            self.buttonPasswordCopy.pack(side='left', padx=5, pady=5)
            self.comboFile['state'] = 'disabled'
            self.entryTitle.configure(state='readonly')
            self.entryUsername.configure(state='readonly')
            self.entryPassword.configure(state='readonly', show='*')
            self.entryEMail.configure(state='readonly')
            self.entryLocation.configure(state='readonly')
            self.textNote.configure(state='disabled')
        else:
            self.buttonPasswordCopy.pack_forget()
            self.comboFile['state'] = 'readonly'
            self.entryTitle.configure(state='normal')
            self.entryUsername.configure(state='normal')
            self.entryPassword.configure(state='normal', show='')
            self.entryEMail.configure(state='normal')
            self.entryLocation.configure(state='normal')
            self.textNote.configure(state='normal')

    def showComboFile(self):
        if not self.comboFilePacked:
            self.comboFile.pack(side='top', padx=5, pady=5, fill='x')
            self.comboFilePacked = True

    def hideComboFile(self):
        if self.comboFilePacked:
            self.comboFile.pack_forget()
            self.comboFilePacked = False

    def updateFromModel(self, passwordObject):
        self.model = passwordObject
        self.updateTitle(passwordObject.getCurrentSecretObject())
        self.updateUsername(passwordObject.getCurrentSecretObject())
        self.updatePassword(passwordObject.getCurrentSecretObject())
        self.updateEmail(passwordObject.getCurrentSecretObject())
        self.updateLocation(passwordObject.getCurrentSecretObject())
        self.updateNote(passwordObject.getCurrentSecretObject())
        self.updateFile(passwordObject)
    
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
        if 'edit' != self.mode:
            self.textNote.configure(state='normal')
        self.textNote.delete(1.0, 'end')
        self.textNote.insert('end', note)
        if 'edit' != self.mode:
            self.textNote.configure(state='disabled')

    def updateFile(self, passwordObj):
        fileOption = passwordObj.getPasswordFile()
        fileName = ""
        if None == fileOption:
            fileName = "Default"
        else:
            fileName = fileOption.getLabel()
        self.comboFile.set(fileName)

    def updateVar(self, var, text):
        if None == text:
            text = ''
        var.set(text)

    def updateModel(self):
        self.model.getCurrentSecretObject().setTitle(self.varTitle.get())
        self.model.getCurrentSecretObject().setUsername(self.varUsername.get())
        self.model.getCurrentSecretObject().setPassword(self.varPassword.get())
        self.model.getCurrentSecretObject().setEmail(self.varEmail.get())
        self.model.getCurrentSecretObject().setLocation(self.varLocation.get())
        self.model.getCurrentSecretObject().setNote(self.textNote.get('1.0', 'end'))

class PasswordFormController(object):
    def __init__(self, view, context):
        self.model = None
        self.view = view
        self.context = context
        self.timeControl = context.getTimeControl()
        self.clipBoard = context.getClipBoard()
        self.passwordFiles = [] #stores possible values for combo passwordfile
        view.buttonPasswordCopy.bind('<1>', self.pressCopy)
        view.varTitle.trace('w', self.resetTime)
        view.varUsername.trace('w', self.resetTime)
        view.varPassword.trace('w', self.resetTime)
        view.varEmail.trace('w', self.resetTime)
        view.varLocation.trace('w', self.resetTime)
        view.textNote.bind('<KeyPress>', self.resetTime)
        self.setMode('normal')
        self.updateFromContext(self.context)

    def setModel(self, model):
        self.model = model

    def setMode(self, mode):
        if 'edit' != mode:
            self.view.entryLocation.bind('<1>', self.callLink)
            self.view.entryLocation.configure(fg='blue')
        else:
            self.view.entryLocation.unbind('<1>')
            self.view.entryLocation.configure(fg='black')

    def callLink(self, event):
        if None != self.model:
            link = self.model.getCurrentSecretObject().getLocation()
            if None != link and "" != link:
                webbrowser.open_new_tab(link)

    def pressCopy(self, event):
        if None != self.clipBoard and None != self.model:
            entry = self.model.getCurrentSecretObject().getPassword()
            if None != entry:
                self.clipBoard.copyToClipBoard(entry)

    def resetTime(self, event, *args):
        if None != self.timeControl:
            self.timeControl.resetTime()
    
    def setTimeControl(self, timeControl):
        # TODO: deprecated, use context.getTimeControl()
        self.timeControl = timeControl
    
    def setClient(self, client):
        # TODO: deprecated, use conext.getClipBoard()
        self.clipBoard = client
    
    def validate(self):
        self.view.updateModel()
        passwordFileIdx = self.view.comboFile.current()
        if passwordFileIdx >= 0 and passwordFileIdx < len(self.passwordFiles):
            self.model.setPasswordFile(self.passwordFiles[passwordFileIdx])

    def updateFromContext(self, context):
        #we need to keep the passwordFiles because in combobox only the labels are stored 
        self.passwordFiles = context.getPasswordFiles()
        if len(self.passwordFiles) <= 1:
            self.view.hideComboFile()
        else:
            self.view.showComboFile()
            passwordFileLabels = [ passwordFile.getLabel() for passwordFile in self.passwordFiles ]
            self.view.comboFile['values'] = passwordFileLabels

if __name__=='__main__':
    window = tk.Tk()
    window.title('PasswordForm')
    passwordForm = PasswordForm(window)
    passwordForm.getFrame().pack()
    window.mainloop()

