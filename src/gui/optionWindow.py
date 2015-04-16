'''
Created on 10.04.2015

@author: crimsen
'''
import Tkinter as tk

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
        
    def pressCancel(self):
        self.optionWindow.destroy()
    
    def pressSave(self):
        emaillist = self.gpgBox.curselection()
        emailindex = emaillist[0]
        email = self.gpgBox.get(emailindex)
        print (email)
        self.maincontroller.pressoptionsave(email)
    
    def __loadGpgBox(self, accounts):
        for email in accounts:
            self.gpgBox.insert('end', str(email))

    def show(self):
        self.optionWindow.mainloop()

        