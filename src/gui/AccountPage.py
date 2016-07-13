'''
Created on 09.05.2015

@author: groegert
'''

from controller.Encryption import Encryption
from gui.EmptyPage import EmptyPage
from gui.EmptyPage import EmptyPageContext
from gui.EmptyPage import EmptyPageController
from gui.EmptyPage import EmptyPageView
import logging
import sys
import webbrowser
if sys.hexversion >= 0x3000000:
    import tkinter as tk
else:
    import Tkinter as tk

class AccountPage(EmptyPage):
    '''
    classdocs
    '''


    def __init__(self, parent, context):
        '''
        Constructor
        '''
        self.view = AccountPageView(parent)
        self.controller = AccountPageController(self.view, context)
    def setModel(self, model):
        self.controller.setModel(model)
        self.view.updateFromModel(model)
 
class AccountPageContext(EmptyPageContext):
    def __init__(self, option):
        EmptyPageContext.__init__(self, option)

class AccountPageView(EmptyPageView):
    def __init__(self, parent):
        self.__buildFrame__(parent)
    def __buildFrame__(self, parent):
        self.frame = tk.Frame(master=parent)
        self.frameInfo = tk.Frame(master=self.frame)
        self.gpgBox = tk.Listbox(master=self.frame, width=30)
        self.label = tk.Label(master=self.frame, text='Please choose your Account', font='Arial 18 bold')

        self.labelInfo = tk.Label(master=self.frameInfo, text='No Account there?\nThen follow this instruction:')
        self.labelLink = tk.Label(master=self.frameInfo, text='GPG Link', fg='blue', cursor='hand2')
        self.labelInfo.pack(side='top', padx=5, pady=5)
        self.labelLink.pack(side='top', padx=5, pady=5)
        
        
        self.frame.pack(side='top', fill='both', expand=True)
        self.label.pack(side='top', padx=5, pady=5, anchor='w')
        self.gpgBox.pack(side='left', fill='y', padx=5, pady=5, anchor='w')
        self.frameInfo.pack(side='top', fill='both', expand=True)
    def updateModel(self, model):
        emaillist = self.gpgBox.curselection()
        emailindex = emaillist[0]
        email = self.gpgBox.get(emailindex)
        emailOld = model.getEmailOld()
        model.email = email
        model.emailOld = emailOld
    def updateFromModel(self, model):
        try:
            accounts = self.gpgBox.get(0, 'end')
            if None != model.getEmail():
                currentIndex = accounts.index(model.getEmail())
                self.gpgBox.selection_set(currentIndex)
        except:
            logging.error(sys.exc_info())


class AccountPageController(EmptyPageController):
    def __init__(self, view, context):
        EmptyPageController.__init__(self, view, context)
        self.view.labelLink.bind('<1>', self.callLink)
        self.updateFromContext(context)
    def apply(self):
        self.view.updateModel(self.model)

    def callLink(self, event):
        webbrowser.open_new_tab('http://www.dewinter.com/gnupg_howto/english/GPGMiniHowto-3.html#ss3.1')

    def updateFromContext(self, context):
        accounts = self.getUsableAccounts()
        self.loadGpgBox(accounts)
        
    def getUsableAccounts(self):
        retVal = []
        encryption = Encryption(self.context)
        retVal = encryption.getSecretKeys()
        return retVal

    def loadGpgBox(self, accounts):
        self.view.gpgBox.delete(0, 'end')
        for email in accounts:
            self.view.gpgBox.insert('end', email)

