'''
Created on 10.04.2015

@author: crimsen
'''
from OptionTree import OptionTree
import Tkinter as tk
from tkMessageBox import showerror

class OptionWindow(object):
    '''
    classdocs
    '''
    def __init__(self, option, controller):
        self.option = option
        self.maincontroller = controller
        self.optionWindow = tk.Toplevel()
        self.optionWindow.title('Preferences')
        self.__buildFrames()
        self.optionWindow.attributes('-topmost', True)
        self.optionPages={}

    def __buildFrames(self):
        self.currentPage = None
        self.frameMain = tk.Frame(master=self.optionWindow)
        self.tree = OptionTree(self.frameMain, self.option)
        self.frameOption = tk.Frame(master=self.frameMain)
        self.buttonSave = tk.Button(master=self.frameMain, text='Save', command=self.pressSave)
        self.buttonCancel = tk.Button(master=self.frameMain, text='Cancel', command=self.pressCancel) 
    
        self.frameMain.pack(side='top', fill='both', expand=True)
        self.tree.frameMain.pack(side='left', fill='y')
        self.frameOption.pack(side='top', fill='both', expand=True)
        self.buttonSave.pack(side='right', anchor='se', padx=5, pady=5)
        self.buttonCancel.pack(side='right', anchor='se', padx=5, pady=5)
        
        self.tree.addEventSink(self.itemSelected)
    
    def apply(self):
        '''
        apply the values of all pages that had been displayed.
        '''
        for page in self.optionPages.values():
            page[1].apply()

    def pressCancel(self):
        self.optionWindow.destroy()
    
    def pressSave(self):
        # TODO: here we should first validate all pages and in case of an invalid setting we should display an error
        try:
            self.apply()
            print(self.option.email)
            self.maincontroller.controlOptionSave()
            self.optionWindow.destroy()
        except:
            showerror('Incorrect Setting', 'Any setting is incorrect. Check if you did choose an account.')
            
    def close(self):
        self.optionWindow.destroy()
    
    def show(self):
        self.optionWindow.mainloop()

#http://stackoverflow.com/questions/16514617/python-tkinter-notebook-widget
    def itemSelected(self, itemId):
        optionPage = None
        if itemId in self.optionPages:
            optionPage = self.optionPages[itemId]
        if None == optionPage:
            optionPage = self.buildOptionPage(self.tree.getOptionPageDescription(itemId))
            self.optionPages[itemId] = optionPage
        if None != self.currentPage:
            self.currentPage[0].pack_forget()
        self.currentPage = optionPage
        optionPage[0].pack(fill='both', expand=True)

    def buildOptionPage(self, pageDescription):
        (pageType, model) = pageDescription
        visibilityFrame = tk.Frame(master=self.frameOption)
        visibilityFrame.pack(fill='both', expand=True)
        optionPage = pageType(visibilityFrame, model)
        return (visibilityFrame, optionPage)
