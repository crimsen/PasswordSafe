'''
Created on 12.05.2015

@author: timgroger
'''

from MasterDetailsForm import MasterDetailsForm
from MasterDetailsForm import MasterDetailsFormContext
from MasterDetailsForm import MasterDetailsFormView
from MasterDetailsForm import MasterDetailsFormController
from .PasswordForm import PasswordForm
from controller.PasswordSafeFilter import PasswordSafeFilter
from edit.DeleteSafeItemCmd import DeleteSafeItemCmd
import webbrowser
import sys
from gui.NewSafeItemWindow import NewSafeItemWindowContext
from gui.MessageWindow import MessageWindow
from gui.ChangeSafeItemWindow import ChangeSafeItemWindowContext
from gui.CertificatePage import CertificatePage
from gui.EmptyPage import EmptyPage
from gui.TreeView import TreeView
from gui.TreeView import TreeViewContext
from model.CertificateObject import CertificateObject
from model.PasswordSafeContentProvider import PasswordSafeContentProvider
from model.PasswordSafeLabelProvider import PasswordSafeLabelProvider
from model.SafeItem import SafeItem
if sys.hexversion >= 0x3000000:
    import tkinter as tk
    from tkinter import StringVar
else:
    import Tkinter as tk
    from Tkinter import StringVar
from gui.NewSafeItemWindow import NewSafeItemWindow
from gui.ChangeSafeItemWindow import ChangeSafeItemWindow
from model.PasswordObject import PasswordObject
from .PassGenWindow import PassGenWindow
from .HistoryWindow import HistoryWindow

class UnlockFrame(MasterDetailsForm):
    '''
    classdocs
    '''
    def __init__(self, context):
        MasterDetailsForm.__init__(self, context, UnlockFrameModel(context.getModel()))
        self.view = UnlockFrameView(context, self.viewModel)
        self.controller = UnlockFrameController(self.view, self.viewModel, self.context)

    def close(self):
        self.controller.cleanUp()
        self.view.close()
        
    def setTime(self, time):
        self.view.setTime(time)

class UnlockFrameContext(MasterDetailsFormContext):
    def __init__(self, parent, editingDomain):
        self.parent = parent
        self.editingDomain = editingDomain
    
    def getMainFrame(self):
        return self.parent.getmainwindow()
    def getFrame(self):
        return self.parent.getmainwindow()
    def getParent(self):
        return self.parent
    def getOption(self):
        return self.parent.getController().getOption()
    def getModel(self):
        return self.editingDomain.getModel()
    def getEditingDomain(self):
        return self.editingDomain
    def getController(self):
        return self.parent.getController()
    def getTimeControl(self):
        return self.parent.getController()
    def getClipBoard(self):
        return self.parent.getController()

class UnlockFrameModel(object):
    def __init__(self, passwordSafe):
        self.passwordSafe = passwordSafe
    
    def getSafe(self):
        return self.passwordSafe

class UnlockFrameView(MasterDetailsFormView):
    def __init__(self, context, viewModel):
        MasterDetailsFormView.__init__(self, context, viewModel)
        self.parent = context.getFrame()
        self.checkTitle = StringVar()
        self.checkUsername = StringVar()
        self.checkPassword = StringVar()
        self.checkEmail = StringVar()
        self.checkLocation = StringVar()
        self.checkNote = StringVar()
        self.__buildFrame__(self.parent)
        self.__setDefault__()

    def __buildFrame__(self, parent):
        self.formFrame = tk.Frame(master=parent)
        self.__buildMenuBar__(self.formFrame)
        self.__buildFilterFrame__(self.formFrame)
        self.treeView = TreeView(TreeViewContext(self.formFrame))
        self.treeView.setLabelProvider(PasswordSafeLabelProvider())
        self.frameOption = tk.Frame(master=self.formFrame)
        self.buttonLock = tk.Button(master=self.formFrame, text='Lock', underline=0)
        self.labelTime = tk.Label(master=self.formFrame, anchor='e')
        self.__packFrame__()

    def __packFrame__(self):
        self.frameFilter.pack(side='top', fill='x', pady=10)
        self.treeView.getFrame().pack(side='left', fill='both', padx=10, pady=10)
        self.frameOption.pack(side='top', fill='both', expand=True)
        self.labelTime.pack(side='bottom')
        self.buttonLock.pack(side='bottom', fill='both', padx=5, pady=5)
        self.formFrame.pack(fill='both', expand=True)

    def __setDefault__(self):
        self.buttonFilterTitle.select()
        self.buttonFilterUsername.select()
        self.buttonFilterPassword.select()
        self.buttonFilterEmail.select()
        self.buttonFilterLocation.select()
        self.buttonFilterNote.select()
        
    def __buildFilterFrame__(self, parent):
        self.frameFilter = tk.Frame(master=parent)
        
        self.buttonFilterTitle = tk.Checkbutton(master=self.frameFilter, variable=self.checkTitle, onvalue='title', offvalue='', text='Title', underline=0)
        self.buttonFilterUsername = tk.Checkbutton(master=self.frameFilter, variable=self.checkUsername, onvalue='username', offvalue='', text='Username', underline=0)
        self.buttonFilterPassword = tk.Checkbutton(master=self.frameFilter, variable=self.checkPassword, onvalue='password', offvalue='', text='Password', underline=1)
        self.buttonFilterEmail = tk.Checkbutton(master=self.frameFilter, variable=self.checkEmail, onvalue='email', offvalue='', text='Email', underline=0)
        self.buttonFilterLocation = tk.Checkbutton(master=self.frameFilter, variable=self.checkLocation, onvalue='location', offvalue='', text='Location', underline=1)
        self.buttonFilterNote = tk.Checkbutton(master=self.frameFilter, variable=self.checkNote, onvalue='note', offvalue='', text='Note', underline=0)
        
        self.buttonFilterTitle.pack(side='left')
        self.buttonFilterUsername.pack(side='left')
        self.buttonFilterPassword.pack(side='left')
        self.buttonFilterEmail.pack(side='left')
        self.buttonFilterLocation.pack(side='left')
        self.buttonFilterNote.pack(side='left')
        
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
        self.formFrame.destroy()

    def setTime(self, time):
        text = ''
        if None != time:
            text = 'Autolock in '+str(time)+' seconds!'
        self.labelTime.config(text=text)
        
    def setDetail(self, item):
        self.updatePages(item)
        childViewModel = item
        self.currentPage[1].setModel(childViewModel)
        self.finishCurrentPagePacked()
    def updateFromModel(self, model):
        self.treeView.setModel(model.getSafe())
    def updatePages(self, item):
        '''
        function updates the form of the right side based on
        the type of the item
        '''
        pageId = self.getPageType(item)
        page = None
        if pageId in self.pages:
            page = self.pages[pageId]
        if None == page:
            pageDescription = (pageId, pageId.createContext(self.context))
            page = self.buildFormPage(pageDescription)
            self.pages[pageId] = page
        self.setCurrentPageUnpacked(page)
    
    def getPageType(self, item):
        retVal = EmptyPage
        secretObject = item
        if isinstance(item, SafeItem):
            secretObject = item.getCurrentSecretObject()
        if type(secretObject) == PasswordObject:
            retVal = PasswordForm
        elif type(secretObject) == CertificateObject:
            retVal = CertificatePage
        return retVal
        
class UnlockFrameController(MasterDetailsFormController):
    def __init__(self, view, model, context):
        MasterDetailsFormController.__init__(self, view, model, context)
        self.detail = None
        self.timeControl = context.getTimeControl()
        self.client = context.getController()
        self.openWindows = {}
        self.filter = PasswordSafeFilter(None)

        view.checkTitle.trace('w', self.updateFilter)
        view.checkUsername.trace('w', self.updateFilter)
        view.checkPassword.trace('w', self.updateFilter)
        view.checkEmail.trace('w', self.updateFilter)
        view.checkLocation.trace('w', self.updateFilter)
        view.checkNote.trace('w', self.updateFilter)
        
        view.buttonLock.configure(command=self.pressLock)
        view.formFrame.bind('<Escape>', self.pressLock)

        if None != context:
            mainWindow = context.getMainFrame()
            mainWindow.bind('<Alt-t>', lambda e: view.buttonFilterTitle.toggle())
            mainWindow.bind('<Alt-u>', lambda e: view.buttonFilterUsername.toggle())
            mainWindow.bind('<Alt-a>', lambda e: view.buttonFilterPassword.toggle())
            mainWindow.bind('<Alt-e>', lambda e: view.buttonFilterEmail.toggle())
            mainWindow.bind('<Alt-o>', lambda e: view.buttonFilterLocation.toggle())
            mainWindow.bind('<Alt-n>', lambda e: view.buttonFilterNote.toggle())

        self.configureMenu()
        self.updateFilter()
        self.view.treeView.setContentProvider(PasswordSafeContentProvider(self.filter))
        self.view.treeView.addEventSink(self.onItemSelected)
        self.view.treeView.setModel(model.getSafe())
        self.view.treeView.setFocus()

    def configureMenu(self):
        self.view.fileMenu.add_command(label='Options', underline=0, command=self.pressOptions)
        self.view.passMenu.add_command(label='New Password', underline=0, command=self.pressNewPass)
        self.view.passMenu.add_command(label='Delete Password', underline=0, command=self.pressRemovePass)
        self.view.passMenu.add_command(label='Change Password', underline=0, command=self.pressChangePass)
        self.view.passMenu.add_command(label='View History', underline=0, command=self.pressViewHistory)
        self.view.passMenu.add_command(label='Passwordgenerator', underline=0, command=self.pressPassGen)
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
        openWindows = self.openWindows
        self.openWindows = {}
        for openWindow in openWindows.values():
            openWindow.close()

    def updateFilter(self, *args):
        self.resetTime()
        filterattribute = [self.view.checkTitle.get(), self.view.checkUsername.get(), self.view.checkPassword.get(),\
                           self.view.checkEmail.get(), self.view.checkLocation.get(), self.view.checkNote.get()]
        self.filter.setFilterattribute(filterattribute)
        self.onSafeChanged()

    def getMainWindow(self):
        retVal = None
        if None != self.client:
            retVal = self.client.getMainWindow()
        return retVal

    def pressLock(self, *args):            
        if None != self.client:
            self.client.pressLock() 

    def pressOptions(self):
        self.resetTime()
        if None != self.client:
            self.client.pressOptions()
        
    def pressRemovePass(self):
        self.resetTime()
        try:
            if None <> self.detail:
                self.context.getEditingDomain().executeCmd(DeleteSafeItemCmd(self.model.getSafe(), self.detail))
                self.onSafeChanged()
        except:
            self.showobjecterror()
            
    def pressNewPass(self):
        self.resetTime()
        context = NewSafeItemWindowContext(self, self.model.getSafe(), self.context.getEditingDomain())
        self.newpasswindow = NewSafeItemWindow(context)
        self.addWindow(self.newpasswindow)
        self.newpasswindow.show()

    def pressViewHistory(self):
        self.resetTime()
        item = self.getSafeItem(self.detail)
        if None == item:
            MessageWindow('Unsupported action', 'Selected Password doesn\'t have a history.\nOnly the latest version of a Password do have a history.')
        else:
            history = self.detail.getHistory()
            self.historyWindow = HistoryWindow(self, history)
            self.addWindow(self.historyWindow)
            self.historyWindow.show()
        
    def pressChangePass(self):
        self.resetTime()
        item = self.getSafeItem(self.detail)
        if None == item:
            MessageWindow('Unsupported action', 'Selected Password can\'t be changed.\nOnly the latest version of a Password can be changed.')
        else:
            context = ChangeSafeItemWindowContext(self, self.context.getEditingDomain(), self.detail)
            self.changePassWindow = ChangeSafeItemWindow(context)
            self.addWindow(self.changePassWindow)    
            self.changePassWindow.show()
        
    def pressPassGen(self):
        self.resetTime()
        self.passGenWindow = PassGenWindow(self)
        self.addWindow(self.passGenWindow)
        self.passGenWindow.show()
            
    def pressAbout(self):
        self.resetTime()
        if None != self.client:
            self.client.pressAbout()
            
    def showoptionerror(self):
        MessageWindow('Error 404-File not found', 'No Options found.\nPlease open Options, choose an account\nand save it.')
        
    def showobjecterror(self):
        MessageWindow('Error', 'No Object is chosen.\nPleas choose an Object!')
        
    def destroy(self):
        self.formFrame.destroy()

    def callLink(self, event):
        url = self.labelLocationLinkFill.cget('text')
        if 'http://' not in url:
            if 'https://' not in url:
                url = 'http://'+url
        webbrowser.open_new_tab(url)
    
    def resetTime(self):
        if None!= self.timeControl:
            self.timeControl.resetTime()
    
    def onSafeChanged(self):
        self.view.updateFromModel(self.model)

    def onItemSelected(self, item):
        self.detail = item
        self.view.setDetail(item)

    def copyToClipBoard(self, entry):
        if None != self.client:
            self.client.copyToClipBoard(entry)
    
    def addWindow(self, window):
        cookie = window.addCloseWindowListener(self.onCloseWindow)
        self.openWindows[cookie] = window
    def onCloseWindow(self, cookie):
        self.openWindows.pop(cookie, None)
    def getSafeItem(self, item):
        retVal = None
        if type(item) == SafeItem:
            retVal = item
        return retVal

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
