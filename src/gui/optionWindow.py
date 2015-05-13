'''
Created on 10.04.2015

@author: crimsen
'''
from AccountPage import AccountPage
import Tkinter as tk
from tkMessageBox import showerror

class OptionWindow(object):
    '''
    classdocs
    '''
    def __init__(self, option, controller):
        self.option = option
        self.maincontroller = controller
        self.optionWindow = tk.Tk()
        self.optionWindow.title('Preferences')
        self.optionWindow.geometry('400x400') 
        self.__buildFrames()
        self.optionWindow.attributes('-topmost', True)
        
    def __buildFrames(self):
        self.frameMain = tk.Frame(master=self.optionWindow)
        self.accountPage = AccountPage(self.frameMain, self.option)
        self.buttonSave = tk.Button(master=self.frameMain, text='Save', command=self.pressSave)
        self.buttonCancel = tk.Button(master=self.frameMain, text='Cancel', command=self.pressCancel) 
    
        self.frameMain.pack(side='top', fill='both', expand=True)
        self.accountPage.frameMain.pack(side='top', fill='both')
        self.buttonSave.pack(side='right', anchor='se', padx=5, pady=5)
        self.buttonCancel.pack(side='right', anchor='se', padx=5, pady=5)
    
    def pressCancel(self):
        self.optionWindow.destroy()
    
    def pressSave(self):
        # TODO: here we should first validate all pages and in case of an invalid setting we should display an error
        try:
            self.accountPage.writeToOption()
            print(self.option.email)
            self.maincontroller.pressOptionSave()
            self.optionWindow.destroy()
        except:
            showerror('Incorrect Setting', 'Any setting is incorrect. Check if you did choose an account.')
    
    def show(self):
        self.optionWindow.mainloop()

        