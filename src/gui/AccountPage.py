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
        self.encryptionIds = []
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
        email = self.encryptionIds[emailindex].id
        emailOld = model.getEmailOld()
        model.email = email
        model.emailOld = emailOld
    def updateFromModel(self, model):
        try:
            if None != model.getEmail():
                currentIndex = self.getIndexOfEncryptionId(self.encryptionIds, model.getEmail())
                if None != currentIndex:
                    self.gpgBox.selection_set(currentIndex)
        except:
            logging.error(sys.exc_info())
    def getIndexOfEncryptionId(self, encryptionIds, myid):
        g = ( i for i, e in enumerate( encryptionIds ) if e.id == myid )
        retVal = next( g )
        return retVal


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
        encryptionIds = self.getUsableEncryptionIds(context)
        self.loadGpgBox(encryptionIds)
        
    def getUsableEncryptionIds(self, context):
        encryption = Encryption(context)
        self.encryptionIds = encryption.getEncryptionIds()
        return self.encryptionIds

    def loadGpgBox(self, encryptionIds):
        self.view.encryptionIds = encryptionIds
        self.view.gpgBox.delete(0, 'end')
        for encryptionId in encryptionIds:
            self.view.gpgBox.insert('end', encryptionId.label)

