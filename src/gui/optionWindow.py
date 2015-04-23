'''
Created on 10.04.2015

@author: crimsen
'''
import Tkinter as tk
from tkMessageBox import showerror
import webbrowser

class OptionWindow(object):
    '''
    classdocs
    '''
    def __init__(self, accounts, controller):
        self.maincontroller = controller
        self.accounts = accounts
        self.optionWindow = tk.Tk()
        self.optionWindow.title('Preferences')
        self.optionWindow.geometry('400x400') 
        self.__buildFrames()
        self.__loadGpgBox(self.accounts)
        self.optionWindow.attributes('-topmost', True)
        
    def __buildFrames(self):
        self.frameMain = tk.Frame(master=self.optionWindow)
        self.frameInfo = tk.Frame(master=self.frameMain)
        self.gpgBox = tk.Listbox(master=self.frameMain, width=30)
        self.label = tk.Label(master=self.frameMain, text='Please choose your Account', font='Arial 18 bold')
        self.buttonSave = tk.Button(master=self.frameInfo, text='Save', command=self.pressSave)
        self.buttonCancel = tk.Button(master=self.frameInfo, text='Cancel', command=self.pressCancel) 
    
        self.labelInfo = tk.Label(master=self.frameInfo, text='No Account there?\nThen follow this instruction:')
        self.labelLink = tk.Label(master=self.frameInfo, text='GPG Link', fg='blue', cursor='hand2')
        self.labelInfo.pack(side='top', fill='both', padx=5, pady=5)
        self.labelLink.pack(side='top', fill='both', padx=5, pady=5)
        
        self.labelLink.bind('<1>', self.callLink)
        
        self.frameMain.pack(side='top', fill='both', expand=True)
        self.label.pack(side='top', padx=5, pady=5, anchor='w')
        self.gpgBox.pack(side='left', padx=5, pady=5, fill='both', anchor='w')
        self.frameInfo.pack(side='left', fill='both')
        self.buttonSave.pack(side='right', anchor='se', padx=5, pady=5)
        self.buttonCancel.pack(side='right', anchor='se', padx=5, pady=5)
    
    def callLink(self, event):
        webbrowser.open_new_tab('http://www.dewinter.com/gnupg_howto/english/GPGMiniHowto-3.html#ss3.1')
    
    def pressCancel(self):
        self.optionWindow.destroy()
    
    def pressSave(self):
        try:
            emaillist = self.gpgBox.curselection()
            emailindex = emaillist[0]
            email = self.gpgBox.get(emailindex)
            print (email)
            self.maincontroller.pressoptionsave(email)
            
            self.optionWindow.destroy()
        except:
            showerror('No Account', 'Please choose an account')
    
    def __loadGpgBox(self, accounts):
        for email in accounts:
            self.gpgBox.insert('end', str(email))

    def show(self):
        self.optionWindow.mainloop()

        