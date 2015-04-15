'''
Created on 10.04.2015

@author: crimsen
'''
import Tkinter as tk
import xml.dom.minidom
from tkMessageBox import showinfo
import gnupg
import os

class OptionWindow(object):
    '''
    classdocs
    '''
    def __init__(self, filename):
        self.optionWindow = tk.Tk()
        self.optionWindow.title('Preferences')
        self.optionWindow.geometry('400x400')
        
        self.gpg = gnupg.GPG()
        self.filename = filename
        
        self.accounts = self.parsAccounts()
        
        self.__buildFrames()
        
        self.__loadGpgBox(self.accounts)
        
    def __buildFrames(self):
        self.frameMain = tk.Frame(master=self.optionWindow)
        self.gpgBox = tk.Listbox(master=self.frameMain, width=30)
        self.label = tk.Label(master=self.frameMain, text='Please choose your Account', font='Arial 18 bold')
        self.buttonSave = tk.Button(master=self.frameMain, text='Save', command=self.pressSave)
        self.buttonCancel = tk.Button(master=self.frameMain, text='Cancel', command=self.pressCancel) 
        
        self.frameMain.pack(side='top', fill='both', expand=True)
        self.label.pack(side='top', padx=5, pady=5, anchor='w')
        self.gpgBox.pack(side='left', padx=5, pady=5, fill='both', anchor='w')
        self.buttonSave.pack(side='right', anchor='se', padx=5, pady=5)
        self.buttonCancel.pack(side='right', anchor='se', padx=5, pady=5)
        
    def __showKeys(self):
        
        pass
    
    def pressCancel(self):
        self.optionWindow.destroy()
    
    def pressSave(self):
        emaillist = self.gpgBox.curselection()
        emailindex = emaillist[0]
        email = self.gpgBox.get(emailindex)
        print (email)
        self.writeEmailOption(email, self.filename)
    
    def __loadGpgBox(self, accounts):
        for email in accounts:
            self.gpgBox.insert('end', self.cleanString(str(email)))
    
    def parsAccounts(self):
        secretKeys = self.gpg.list_keys(True)
        uids = []
        emails = []
        
        for keys in secretKeys:
            uids.append(keys['uids'])
        
        for account in uids:
            for email in account:
                emailsplit = email.encode('utf-8').split(' ')
                emails.append(emailsplit[len(emailsplit)-1])
        return emails
           
    def show(self):
        self.optionWindow.mainloop()
        
    def cleanString(self, string):
        
        retVal = ''
        
        for i in string:
            if (i!='<') and (i!='>'):
                retVal+=i
        return retVal
    
    def writeEmailOption(self, email, filename):
        
        implement = xml.dom.getDOMImplementation()
        doc = implement.createDocument(None, 'Options', None)
        
        emailElem = doc.createElement('ActivateEmail')
        emailTextElem = doc.createTextNode(str(email))
        emailElem.appendChild(emailTextElem)
        
        doc.documentElement.appendChild(emailElem)
        
        datei = open(filename, 'w')
        doc.writexml(datei, '\n', ' ')
        datei.close()
        