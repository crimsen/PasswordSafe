'''
Created on 12.05.2015

@author: timgroger
'''

from PasswordForm import PasswordForm
from controller.filter import PassSafeFilter
import Tkinter as tk
import webbrowser
from Tkinter import StringVar
from tkMessageBox import showerror
from gui.newPassWindow import NewPassWindow
from gui.changePassWindow import ChangePassWindow
from gui.ViewHistory import ViewHistory
from model.passObject import PasswordObject

class UnlockFrame(object):
    '''
    classdocs
    '''
    def __init__(self, mainWindow, model):
        '''
        Constructor
        '''
        self.mainWindow = mainWindow
        self.mainWindowFrame = self.mainWindow.getmainwindow()
        self.mainController = mainWindow.maincontroller
        self.model = UnlockFrameModel(model)
        self.view = UnlockFrameView(mainWindow.getmainwindow())
        self.controller = UnlockFrameController(self.view, self.model, self.mainController)

    def close(self):
        self.controller.cleanUp()
        self.view.close()
        
    def setTime(self, time):
        self.view.setTime(time)

class UnlockFrameModel(object):
    def __init__(self, passwordSafe):
        self.passwordSafe = passwordSafe
    
    def getSafe(self):
        return self.passwordSafe

class UnlockFrameView(object):
    def __init__(self, parent):
        self.parent = parent
        self.filterEntry = StringVar()
        self.checkTitle = StringVar()
        self.checkUsername = StringVar()
        self.checkPassword = StringVar()
        self.checkEmail = StringVar()
        self.checkLocation = StringVar()
        self.checkNote = StringVar()
        self.__buildFrame__(parent)
        self.unlockframe.pack(fill='both', expand=True)
        self.__setDefault__()

    def __buildFrame__(self, parent):
        self.unlockframe = tk.Frame(master=parent)
        self.__buildMenuBar__(self.unlockframe)
        self.__buildFilterFrame__(self.unlockframe)
        self.__buildTitleBoxFrame__(self.unlockframe)
        self.passwordForm = PasswordForm(self.unlockframe)
        self.passwordForm.setMode('readonly')
        self.buttonLock = tk.Button(master=self.unlockframe, text='Lock', underline=0)
        self.labelTime = tk.Label(master=self.unlockframe, anchor='e')

        self.frameFilter.pack(side='top', fill='x', padx=5)
        self.frameTitleBox.pack(side='left', fill='both', padx=10, pady=10)
        self.passwordForm.getFrame().pack(side='top', fill='both', expand=True, padx=5, pady=5)
        self.labelTime.pack(side='bottom')
        self.buttonLock.pack(side='bottom', fill='both', padx=5, pady=5)  

    def __setDefault__(self):
        self.buttonFilterTitle.select()
        self.buttonFilterUsername.select()
        self.buttonFilterPassword.select()
        self.buttonFilterEmail.select()
        self.buttonFilterLocation.select()
        self.buttonFilterNote.select()
        
    def __buildFilterFrame__(self, parent):
        self.frameFilter = tk.Frame(master=parent)
        
        self.entryFilter = tk.Entry(master=self.frameFilter, textvariable=self.filterEntry)
        self.buttonFilterTitle = tk.Checkbutton(master=self.frameFilter, variable=self.checkTitle, onvalue='title', offvalue='', text='Title', underline=0)
        self.buttonFilterUsername = tk.Checkbutton(master=self.frameFilter, variable=self.checkUsername, onvalue='username', offvalue='', text='Username', underline=0)
        self.buttonFilterPassword = tk.Checkbutton(master=self.frameFilter, variable=self.checkPassword, onvalue='password', offvalue='', text='Password', underline=1)
        self.buttonFilterEmail = tk.Checkbutton(master=self.frameFilter, variable=self.checkEmail, onvalue='email', offvalue='', text='Email', underline=0)
        self.buttonFilterLocation = tk.Checkbutton(master=self.frameFilter, variable=self.checkLocation, onvalue='location', offvalue='', text='Location', underline=1)
        self.buttonFilterNote = tk.Checkbutton(master=self.frameFilter, variable=self.checkNote, onvalue='note', offvalue='', text='Note', underline=0)
        
        self.entryFilter.pack(side='left', padx=5)
        self.buttonFilterTitle.pack(side='left')
        self.buttonFilterUsername.pack(side='left')
        self.buttonFilterPassword.pack(side='left')
        self.buttonFilterEmail.pack(side='left')
        self.buttonFilterLocation.pack(side='left')
        self.buttonFilterNote.pack(side='left')
        
    def __buildTitleBoxFrame__(self, parent):
        '''
        Build the TitleBox
        Show all passwordobjects
        '''
        self.frameTitleBox = tk.Frame(master=parent)
        self.titleBox = tk.Listbox(master=self.frameTitleBox, selectmode='single', width=30)
        self.scrollbar = tk.Scrollbar(master=self.frameTitleBox)
        self.titleBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.titleBox.yview)
        self.titleBox.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='left', fill='y')

    def __buildMenuBar__(self, parent):
        '''
        Build the MenuBar
        '''
        
        self.menuBar = tk.Menu(master=parent)
        
        self.fileMenu = tk.Menu(master=self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='File', underline=0, menu=self.fileMenu)
        
        self.passMenu = tk.Menu(master=self.menuBar, tearoff=0)      
        self.menuBar.add_cascade(label='Password', underline=0, menu=self.passMenu)
        
        self.parent.config(menu=self.menuBar)

    def close(self):
        self.unlockframe.destroy()

    def updateTitleBox(self, passSafe):
        '''
        Reloaded the TitleBox if some Objects will be removed or changed
        '''
        self.titleBox.delete(0, 'end')
        for passOb in passSafe:
            self.titleBox.insert('end', passOb.getTitle())
    
    def getTitleBoxIndex(self):
        index = self.titleBox.curselection()
        index = index[0]
        return int(index)
    
    def setTitleBoxIndex(self, index):
        self.titleBox.select_clear(0, 'end')
        self.titleBox.select_set(index)

    def updateFromModel(self, model, index=-1):
        password = None
        if None != model.getSafe():
            if -1 != index:
                password = model.getSafe()[index]
        if None == password:
            password = PasswordObject()
        self.passwordForm.setModel(password)

    def setTime(self, time):
        text = ''
        if None != time:
            text = 'Autolock in '+str(time)+' seconds!'
        self.labelTime.config(text=text)
        
class UnlockFrameController(object):
    def __init__(self, view, model, client):
        self.timeControl = None
        self.view = view
        self.model = model
        self.client = client
        self.filter = PassSafeFilter(model.getSafe())

        view.filterEntry.trace('w', self.updateFilter)
        view.checkTitle.trace('w', self.updateFilter)
        view.checkUsername.trace('w', self.updateFilter)
        view.checkPassword.trace('w', self.updateFilter)
        view.checkEmail.trace('w', self.updateFilter)
        view.checkLocation.trace('w', self.updateFilter)
        view.checkNote.trace('w', self.updateFilter)
        
        view.buttonLock.configure(command=self.pressLock)
        view.unlockframe.bind('<Escape>', self.pressLock)
        view.titleBox.bind('<Escape>', self.pressLock)
#        self.frameData.bind('<Escape>', self.presslock)
#        self.framePic.bind('<Escape>', self.presslock)
#        self.labelPasswordFill.bind('<Escape>', self.presslock)
        view.titleBox.bind('<<ListboxSelect>>', self.selectedTitle)
        view.titleBox.bind('<Up>', self.setTitleBoxIndexUp)
        view.titleBox.bind('<Down>', self.setTitleBoxIndexDown)
        view.entryFilter.bind('<Up>', self.setTitleBoxIndexUp)
        view.entryFilter.bind('<Down>', self.setTitleBoxIndexDown)

        if None != client:
            mainWindow = client.getMainWindow()
            mainWindow.bind('<Alt-t>', lambda e: view.buttonFilterTitle.toggle())
            mainWindow.bind('<Alt-u>', lambda e: view.buttonFilterUsername.toggle())
            mainWindow.bind('<Alt-a>', lambda e: view.buttonFilterPassword.toggle())
            mainWindow.bind('<Alt-e>', lambda e: view.buttonFilterEmail.toggle())
            mainWindow.bind('<Alt-o>', lambda e: view.buttonFilterLocation.toggle())
            mainWindow.bind('<Alt-n>', lambda e: view.buttonFilterNote.toggle())

        self.configureMenu()
        self.updateFilter()
        view.updateFromModel(self.filter)
        view.passwordForm.setClient(self)
        view.entryFilter.focus_force()

#        self.buttonPasswordCopy.bind('<1>', self.pressCopy)
#        self.labelPasswordFill.bind('<Control-c>', self.pressCopy)
#        self.mainWindowFrame.bind('<Alt-c>', self.pressCopy)
#        self.mainWindowFrame.bind('<Alt-l>', self.presslock)
#        self.buttonLock.bind('<1>', self.presslock)
#        self.buttonLock.bind('<Return>', self.presslock)  
#        self.labelLocationLinkFill.bind('<1>', self.callLink)

    def configureMenu(self):
        self.view.fileMenu.add_command(label='Options', underline=0, command=self.pressOptions)
        self.view.passMenu.add_command(label='New Password', underline=0, command=self.pressNewPass)
        self.view.passMenu.add_command(label='Delete Password', underline=0, command=self.pressRemovePass)
        self.view.passMenu.add_command(label='Change Password', underline=0, command=self.pressChangePass)
        self.view.passMenu.add_command(label='View History', underline=0, command=self.pressViewHistory)
        self.view.menuBar.add_command(label='About', underline=1, command=self.pressAbout)

    def cleanUp(self):
        mainWindow = self.getMainWindow()
        if None != mainWindow:
            mainWindow.unbind('<Alt-t>')
            mainWindow.unbind('<Alt-u>')
            mainWindow.unbind('<Alt-a>')
            mainWindow.unbind('<Alt-e>')
            mainWindow.unbind('<Alt-o>')
            mainWindow.unbind('<Alt-n>')
#            mainWindow.unbind('<Alt-l>')
#            mainWindow.unbind('<Alt-c>')

    def updateFilter(self, *args):
        filterstring = self.view.filterEntry.get()
        filterattribute = [self.view.checkTitle.get(), self.view.checkUsername.get(), self.view.checkPassword.get(),\
                           self.view.checkEmail.get(), self.view.checkLocation.get(), self.view.checkNote.get()]
        self.filter.setFilterstring(filterstring)
        self.filter.setFilterattribute(filterattribute)
        self.filter.doFilter()
        self.view.updateTitleBox(self.filter.getSafe())

    def getMainWindow(self):
        retVal = None
        if None != self.client:
            retVal = self.client.getMainWindow()
        return retVal

    def setCurrent(self, index):
        password = None
        if -1 == index and 0 != len(self.filter.getSafe()):
            index = 0
        if -1 != index:
            self.view.setTitleBoxIndex(index)
            password = self.filter.getSafe()[index]
        self.view.passwordForm.setModel(password)
        
    def setTitleBoxIndexUp(self, event):
        try:
            index = self.view.getTitleBoxIndex()
        except:
            index = len(self.view.titleBox.get(0, 'end')) - 1
        if index != 0:
            self.setCurrent(index - 1)

    def setTitleBoxIndexDown(self, event):
        try:
            index = self.view.getTitleBoxIndex()
        except:
            index = 0
        if index != (len(self.view.titleBox.get(0, 'end')) - 1):
            self.setCurrent(index + 1)

    def selectedTitle(self, event):
        index = self.view.getTitleBoxIndex()
        self.setCurrent(index)    
        
    def pressLock(self, *args):
        if None != self.client:
            self.client.pressLock() 

    def pressOptions(self):
        if None != self.client:
            self.client.pressOptions()
        
    def pressRemovePass(self):
        try:
            index = self.view.getTitleBoxIndex()
            passObFilter = self.filter.getSafe()[index]
            self.model.getSafe().removePassOb(passObFilter)
            self.filter.doFilter()
            self.view.updateTitleBox(self.filter.getSafe())
            if index >= len(self.filter.getSafe()) :
                index = len(self.filter.getSafe()) - 1
            self.setCurrent(index)
            self.resetTime()
        except:
            self.showobjecterror()
            
    def pressNewPass(self):
        self.resetTime()
        self.newpasswindow = NewPassWindow(self)
        self.newpasswindow.setTimeControl(self.timeControl)
        self.newpasswindow.show()

    def pressViewHistory(self):
        self.resetTime()
        index = self.view.getTitleBoxIndex()
        history = self.filter.getSafe()[index].getHistory()
        mainWindow = self.client.getMainWindow()
        self.historyWindow = ViewHistory(self, mainWindow, history)
        self.historyWindow.show()
        
    def pressChangePass(self):
        self.resetTime()
        index = self.view.getTitleBoxIndex()
        passObFilter = self.filter.getSafe()[index]
        self.changePassWindow = ChangePassWindow(self, passObFilter)
        self.changePassWindow.setTimeControl(self.timeControl)    
        self.changePassWindow.show()
            
    def pressAbout(self):
        if None != self.client:
            self.client.pressAbout()
            
    def showoptionerror(self):
        showerror('Error 404-File not found', 'No Options found.\nPlease open Options, choose an account\nand save it.')
        
    def showobjecterror(self):
        showerror('Error', 'No Object is chosen.\nPleas choose an Object!')
        
    def destroy(self):
        self.unlockframe.destroy()

    def callLink(self, event):
        url = self.labelLocationLinkFill.cget('text')
        if 'http://' not in url:
            if 'https://' not in url:
                url = 'http://'+url
        webbrowser.open_new_tab(url)
    
    def resetTime(self):
        if None!= self.timeControl:
            self.timeControl.resetTime()
    
    def addPasswordObject(self, password):
        self.model.getSafe().addPasswordObject(password)
        self.filter.doFilter()
        self.view.updateTitleBox(self.filter.getSafe())

    def changePasswordObject(self, origPasswordObject, passwordObject):
        self.model.getSafe().changePasswordObject(origPasswordObject, passwordObject)
        self.filter.doFilter()
        self.view.updateTitleBox(self.filter.getSafe())
    
    def copyToClipBoard(self,entry):
        if None != self.client:
            self.client.copyToClipBoard(entry)

class Test(object):
    def __init__(self):
        self.mainWindow = tk.Tk()
        
    def run(self):
        tk.mainloop()
    
    def getmainwindow(self):
        return self.mainWindow

if __name__=='__main__':
    parent = Test()
    test = UnlockFrame(parent, None)
    parent.run()
