'''
Created on Mar 4, 2016

@author: groegert
'''
from gui.EmptyPage import EmptyPage
from gui.EmptyPage import EmptyPageContext
from gui.EmptyPage import EmptyPageController
from gui.EmptyPage import EmptyPageView
from model.SafeItem import SafeItem
import sys
import os
if sys.hexversion >= 0x3000000:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as filedialog
    from tkinter import StringVar
else:
    import Tkinter as tk
    import ttk as ttk
    import tkFileDialog as filedialog
    from Tkinter import StringVar

class CertificatePage(EmptyPage):
    @staticmethod
    def createContext(parentContext):
        return CertificatePageContext(parentContext)
    def __init__(self, parent, context):
        self.view = CertificatePageView(parent)
        self.controller = CertificatePageController(self.view, context)
    def getFrame(self):
        return self.view.frame
    def setMode(self, mode):
        self.controller.setMode(mode)
    def setModel(self, model):
        self.controller.setModel(model)
        self.view.updateFromModel(model)

class CertificatePageContext(EmptyPageContext):
    def __init__(self, parentContext):
        option = None
        if None != parentContext:
            option = parentContext.getOption()
        EmptyPageContext.__init__(self, option)
        self.parentContext = parentContext
        self.mode = 'normal'
    def getTimeControl(self):
        retVal = None
        if None != self.parentContext:
            retVal = self.parentContext.getTimeControl()
        return retVal
    def getClipBoard(self):
        retVal = None
        if None != self.parentContext:
            retVal = self.parentContext.getClipBoard()
        return retVal
    def getPasswordFiles(self):
        retVal = []
        if None != self.option:
            retVal = self.option.getFiles()
        return retVal
    def getMode(self):
        return self.mode

class CertificatePageView(EmptyPageView):
    def __init__(self, parent):
        self.comboFilePacked = False
        self.varTitle = StringVar()
        self.varSecretKeyFileName = StringVar()
        self.varPublicKeyFileName = StringVar()
        self.varPassword = StringVar()
        self.__buildframe__(parent)
    def __buildframe__(self, parent):
        self.frame = tk.Frame(master=parent)
        self.comboFile = ttk.Combobox(master=self.frame, state='readonly')
        self.showComboFile()
        frameLeft = tk.Frame(master=self.frame)
        self.labelTitle = tk.Label(master=frameLeft, text='Titel', anchor='w', font='Arial 20 bold')
        self.entryTitle = tk.Entry(master=frameLeft, textvariable=self.varTitle)
        self.labelSecretKey = tk.Label(master=frameLeft, text='Secret Key', anchor='w', font='Arial 20 bold')
        frameSecretKey = tk.Frame(master=frameLeft)
        self.entrySecretKey = tk.Entry(master=frameSecretKey, state='readonly', textvariable=self.varSecretKeyFileName)
        self.buttonLoadSecretKey = tk.Button(master=frameSecretKey, text='Load')
        self.buttonSaveSecretKey = tk.Button(master=frameSecretKey, text='Save')
        self.labelPublicKey = tk.Label(master=frameLeft, text='Public Key', anchor='w', font='Arial 20 bold')
        framePublicKey = tk.Frame(master=frameLeft)
        self.entryPublicKey = tk.Entry(master=framePublicKey, state='readonly', textvariable=self.varPublicKeyFileName)
        self.buttonLoadPublicKey = tk.Button(master=framePublicKey, text='Load')
        self.buttonSavePublicKey = tk.Button(master=framePublicKey, text='Save')
        self.labelPassword = tk.Label(master=frameLeft, text='Password', anchor='w', font='Arial 20 bold')
        framePassword = tk.Frame(master=frameLeft)
        self.entryPassword = tk.Entry(master=framePassword, textvariable=self.varPassword)
        self.buttonPasswordCopy = tk.Button(master=framePassword, text='Copy', underline=0)
        frameRight = tk.Frame(master=self.frame)
        self.labelNote = tk.Label(master=frameRight, text='Note', anchor='w', font='Arial 20 bold')
        self.textNote = tk.Text(master=frameRight, height=3, bd=2, relief='flat')

        self.labelTitle.pack(side='top', padx=5, pady=5, fill='both')
        self.entryTitle.pack(side='top', padx=5, pady=5, fill='both')
        self.labelSecretKey.pack(side='top', padx=5, pady=5, fill='both')
        self.entrySecretKey.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        self.buttonSaveSecretKey.pack(side='left', padx=5, pady=5)
        frameSecretKey.pack(side='top', fill='both')
        self.labelPublicKey.pack(side='top', padx=5, pady=5, fill='both')
        self.entryPublicKey.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        self.buttonSavePublicKey.pack(side='left', padx=5, pady=5)
        framePublicKey.pack(side='top', fill='both')
        self.labelPassword.pack(side='top', padx=5, pady=5, fill='both')
        self.entryPassword.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        self.buttonPasswordCopy.pack(side='left', padx=5, pady=5)
        framePassword.pack(side='top', fill='both')
        frameLeft.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.labelNote.pack(side='top', fill='both', padx=5, pady=5)
        self.textNote.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        frameRight.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.frame.pack(side='top', fill='both', expand=True)

    def setMode(self, mode):
        self.mode = mode
        if 'edit' != mode:
            self.buttonLoadSecretKey.pack_forget()
            self.buttonSaveSecretKey.pack(side='left', padx=5, pady=5)
            self.buttonLoadPublicKey.pack_forget()
            self.buttonSavePublicKey.pack(side='left', padx=5, pady=5)
            self.buttonPasswordCopy.pack(side='left', padx=5, pady=5)
            self.comboFile['state'] = 'disabled'
            self.entryTitle.configure(state='readonly')
            self.entryPassword.configure(state='readonly', show='*')
            self.textNote.configure(state='disabled')
        else:
            self.buttonSaveSecretKey.pack_forget()
            self.buttonLoadSecretKey.pack(side='left', padx=5, pady=5)
            self.buttonSavePublicKey.pack_forget()
            self.buttonLoadPublicKey.pack(side='left', padx=5, pady=5)
            self.buttonPasswordCopy.pack_forget()
            self.comboFile['state'] = 'readonly'
            self.entryTitle.configure(state='normal')
            self.entryPassword.configure(state='normal', show='')
            self.textNote.configure(state='normal')

    def showComboFile(self):
        if not self.comboFilePacked:
            self.comboFile.pack(side='top', padx=5, pady=5, fill='x')
            self.comboFilePacked = True

    def hideComboFile(self):
        if self.comboFilePacked:
            self.comboFile.pack_forget()
            self.comboFilePacked = False

    def updateFromModel(self, model):
        secretObject = SafeItem.getSecretObject(model)
        self.updateTitle(secretObject)
        self.updatePassword(secretObject)
        self.updateNote(secretObject)
        self.updateFile(model)
        self.updateSecretKeyFileName(secretObject)
        self.updateSecretKey(secretObject)
        self.updatePublicKeyFileName(secretObject)
        self.updatePublicKey(secretObject)
    
    def updateTitle(self, secretObj):
        self.updateVar(self.varTitle, secretObj.getTitle())

    def updatePassword(self, secretObj):
        self.updateVar(self.varPassword, secretObj.getPassword())
    
    def updateNote(self, secretObj):
        note = secretObj.getNote()
        if None == note:
            note = ''
        if 'edit' != self.mode:
            self.textNote.configure(state='normal')
        self.textNote.delete(1.0, 'end')
        self.textNote.insert('end', note)
        if 'edit' != self.mode:
            self.textNote.configure(state='disabled')

    def updateFile(self, safeItem):
        fileOption = None
        if type(safeItem) == SafeItem:
            fileOption = safeItem.getPasswordFile()
        fileName = ""
        if None == fileOption:
            fileName = "Default"
        else:
            fileName = fileOption.getLabel()
        self.comboFile.set(fileName)

    def updateSecretKeyFileName(self, certificateObject):
        self.updateVar(self.varSecretKeyFileName, certificateObject.getSecretKeyFileName())
    def updateSecretKey(self, certificateObject):
        pass
    def updatePublicKeyFileName(self, certificateObject):
        self.updateVar(self.varPublicKeyFileName, certificateObject.getPublicKeyFileName())
    def updatePublicKey(self, certificateObject):
        pass

    def updateVar(self, var, text):
        if None == text:
            text = ''
        var.set(text)

    def updateModel(self, model):
        certificateObject = SafeItem.getSecretObject(model) 
        certificateObject.setTitle(self.varTitle.get())
        certificateObject.setPassword(self.varPassword.get())
        certificateObject.setNote(self.textNote.get('1.0', 'end'))
        certificateObject.setSecretKeyFileName(self.varSecretKeyFileName.get())
        certificateObject.setPublicKeyFileName(self.varPublicKeyFileName.get())

class CertificatePageController(EmptyPageController):
    def __init__(self, view, context):
        EmptyPageController.__init__(self, view, context)
        self.passwordFiles = [] #stores possible values for combo passwordfile
        view.buttonLoadSecretKey.bind('<1>', self.pressLoadSecretKey)
        view.buttonSaveSecretKey.bind('<1>', self.pressSaveSecretKey)
        view.buttonLoadPublicKey.bind('<1>', self.pressLoadPublicKey)
        view.buttonSavePublicKey.bind('<1>', self.pressSavePublicKey)
        view.buttonPasswordCopy.bind('<1>', self.pressCopy)
        view.varTitle.trace('w', self.resetTime)
        view.varPassword.trace('w', self.resetTime)
        view.textNote.bind('<KeyPress>', self.resetTime)
        self.setMode(context.getMode())
        self.updateFromContext(context)

    def apply(self):
        self.view.updateModel(self.model)
        if type(self.model) == SafeItem:
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

    def setMode(self, mode):
        self.view.setMode(mode)

    def pressCopy(self, event):
        clipBoard = self.context.getClipBoard()
        if None != clipBoard and None != self.model:
            entry = SafeItem.getSecretObject(self.model).getPassword()
            if None != entry:
                clipBoard.copyToClipBoard(entry)

    def pressLoadSecretKey(self, event):
        fileName = self.view.varSecretKeyFileName.get()
        certificateObject = SafeItem.getSecretObject(self.model)
        (fileName, key) = self.loadKey(fileName)
        if None != fileName:
            certificateObject.setSecretKey(key)
            self.view.varSecretKeyFileName.set(os.path.basename(fileName))

    def pressSaveSecretKey(self, event):
        fileName = self.view.varSecretKeyFileName.get()
        certificateObject = SafeItem.getSecretObject(self.model)
        self.saveKey(fileName, certificateObject.getSecretKey())

    def pressLoadPublicKey(self, event):
        fileName = self.view.varPublicKeyFileName.get()
        certificateObject = SafeItem.getSecretObject(self.model)
        (fileName, key) = self.loadKey(fileName)
        if None != fileName:
            certificateObject.setPublicKey(key)
            self.view.varPublicKeyFileName.set(os.path.basename(fileName))

    def pressSavePublicKey(self, event):
        fileName = self.view.varPublicKeyFileName.get()
        certificateObject = SafeItem.getSecretObject(self.model)
        self.saveKey(fileName, certificateObject.getPublicKey())

    def loadKey(self, fileName):
        retVal = (None, None)
        fileName = filedialog.askopenfilename(initialfile=fileName)
        if 0 != len(fileName):
            fileStream = open(fileName, "rb")
            key = fileStream.read().decode('utf-8')
            fileStream.close()
            retVal = (fileName, key)
        return retVal;
        
    def saveKey(self, fileName, key):
        fileName = filedialog.asksaveasfilename(initialfile=fileName)
        if 0 != len(fileName):
            fileStream = open(fileName, "wb")
            fileStream.write(key)
            fileStream.close()
        
    def resetTime(self, event, *args):
        timeControl = self.context.getTimeControl()
        if None != timeControl:
            timeControl.resetTime()

if __name__=='__main__':
    window = tk.Tk()
    window.title('CertificatePage')
    context = CertificatePageContext(None)
    certificatePage = CertificatePage(window, context)
    certificatePage.getFrame().pack()
    window.mainloop()
