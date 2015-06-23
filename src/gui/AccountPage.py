'''
Created on 09.05.2015

@author: thomas
'''

import Tkinter as tk
import webbrowser
import gnupg
import re
import sys

class AccountPage(object):
    '''
    classdocs
    '''


    def __init__(self, parent, option):
        '''
        Constructor
        '''
        self.option = option
        self.__buildFrame__(parent)
        self.updateWindow()
    
    def __buildFrame__(self, parent):
        self.frameMain = tk.Frame(master=parent)
        self.frameInfo = tk.Frame(master=self.frameMain)
        self.gpgBox = tk.Listbox(master=self.frameMain, width=30)
        self.label = tk.Label(master=self.frameMain, text='Please choose your Account', font='Arial 18 bold')

        self.labelInfo = tk.Label(master=self.frameInfo, text='No Account there?\nThen follow this instruction:')
        self.labelLink = tk.Label(master=self.frameInfo, text='GPG Link', fg='blue', cursor='hand2')
        self.labelInfo.pack(side='top', padx=5, pady=5)
        self.labelLink.pack(side='top', padx=5, pady=5)
        
        self.labelLink.bind('<1>', self.callLink)
        
        self.frameMain.pack(side='top', fill='both', expand=True)
        self.label.pack(side='top', padx=5, pady=5, anchor='w')
        self.gpgBox.pack(side='left', fill='y', padx=5, pady=5, anchor='w')
        self.frameInfo.pack(side='top', fill='both', expand=True)

    def apply(self):
        self.writeToOption()

    def writeToOption(self):
        '''
        writes the settings made by the user in the ui into the option object
        '''
        emaillist = self.gpgBox.curselection()
        emailindex = emaillist[0]
        email = self.gpgBox.get(emailindex)
        self.option.email = email

    def readFromOption(self):
        '''
        reads values from the option object and sets the ui according to the values
        '''
        try:
            accounts = self.gpgBox.get(0, 'end')
            currentIndex = accounts.index(self.option.getEmail())
            self.gpgBox.selection_set(currentIndex)
        except:
            print sys.exc_info()

    def updateWindow(self):
        '''
        prepares the window with possible settings and updates the ui
        '''
        accounts = self.getUsableAccounts()
        self.loadGpgBox(accounts)
        self.readFromOption()

    def callLink(self, event):
        webbrowser.open_new_tab('http://www.dewinter.com/gnupg_howto/english/GPGMiniHowto-3.html#ss3.1')

    def getUsableAccounts(self):
        secretKeys = gnupg.GPG().list_keys(True)
        uids = []
        emails = []
        
        for keys in secretKeys:
            uids += keys['uids']
        
        for account in uids:
            emails.append(re.sub(r'.*<(.*)>',r'\1', account))
        return emails

    def loadGpgBox(self, accounts):
        self.gpgBox.delete(0, 'end')
        for email in accounts:
            self.gpgBox.insert('end', email)

