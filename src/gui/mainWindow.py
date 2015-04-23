'''
Created on 15.04.2015

@author: crimsen
'''
import Tkinter as tk
from tkMessageBox import showerror
from Tkinter import StringVar

class MainWindow(object):
    '''
    classdocs
    '''

    
    def __init__(self, controller):
            
        self.mainWindow = tk.Tk()
        self.mainWindow.title('Passwordsafe')
        self.mainWindow.geometry('900x500')
        
        self.filterEntry = StringVar()
        self.checkTitle = StringVar()
        self.checkUsername = StringVar()
        self.checkPassword = StringVar()
        self.checkEmail = StringVar()
        self.checkLocation = StringVar()
        self.checkNote = StringVar()
        
        self.filterEntry.trace('w', self.updatefilter)
        self.checkTitle.trace('w', self.updatefilter)
        self.checkUsername.trace('w', self.updatefilter)
        self.checkPassword.trace('w', self.updatefilter)
        self.checkEmail.trace('w', self.updatefilter)
        self.checkLocation.trace('w', self.updatefilter)
        self.checkNote.trace('w', self.updatefilter)
        
        self.maincontroller = controller
        
        self.lockframe = None
        self.unlockframe = None
        
        self.showlockframe()
        
    def __initUnlockFrame__(self, parent):
        '''
        Constructor
        '''
        
        self.unlockframe = tk.Frame(master=parent)
        self.unlockframe.pack(fill='both', expand=True)
        self.__buildFilterFrame__(self.unlockframe)
        self.__buildTitleBoxFrame__(self.unlockframe)
        self.__buildFrameData__(self.unlockframe)
        self.__buildFramePic__(self.unlockframe)
        self.__buildMenuBar__(self.unlockframe)
        self.__setDefault__()
        
        #self.unlockframe.bind('<Key-Backspace>', self.presslock())
        
    def __setDefault__(self):
        self.buttonFilterTitle.select()
        self.buttonFilterUsername.select()
        self.buttonFilterPassword.select()
        self.buttonFilterEmail.select()
        self.buttonFilterLocation.select()
        self.buttonFilterNote.select()
        
    def __buildFilterFrame__(self, parent):
        self.frameFilter = tk.Frame(master=parent)
        self.frameFilter.pack(side='top', fill='x', padx=5)
        
        self.entryFilter = tk.Entry(master=self.frameFilter, textvariable=self.filterEntry)
        self.buttonFilterTitle = tk.Checkbutton(master=self.frameFilter, variable=self.checkTitle, onvalue='title', offvalue='', text='Title')
        self.buttonFilterUsername = tk.Checkbutton(master=self.frameFilter, variable=self.checkUsername, onvalue='username', offvalue='', text='Username')
        self.buttonFilterPassword = tk.Checkbutton(master=self.frameFilter, variable=self.checkPassword, onvalue='password', offvalue='', text='Password')
        self.buttonFilterEmail = tk.Checkbutton(master=self.frameFilter, variable=self.checkEmail, onvalue='email', offvalue='', text='Email')
        self.buttonFilterLocation = tk.Checkbutton(master=self.frameFilter, variable=self.checkLocation, onvalue='location', offvalue='', text='Location')
        self.buttonFilterNote = tk.Checkbutton(master=self.frameFilter, variable=self.checkNote, onvalue='note', offvalue='', text='Note')
        
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
        self.frameTitleBox.pack(side='left', fill='both', padx=10, pady=10)
        self.titleBox = tk.Listbox(master=self.frameTitleBox, selectmode='single', width=30)
        self.scrollbar = tk.Scrollbar(master=self.frameTitleBox)
        self.titleBox.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='left', fill='y')
        self.titleBox.delete(0, 'end')           
        self.titleBox.bind('<<ListboxSelect>>', self.selectedTitle)
        self.titleBox.bind('<Up>', self.setTitleBoxIndexUp)
        self.titleBox.bind('<Down>', self.setTitleBoxIndexDown)
        self.titleBox.focus_force()

    def __buildFrameData__(self, parent):
        '''
        Buil the frame in the middle
        Show from the selected passwordobject the title, the username, the password and the email
        '''
        
        self.frameData = tk.Frame(master=parent)
        self.frameData.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.framePassword = tk.Frame(master=self.frameData)
        
        self.labelTitle = tk.Label(master=self.frameData, text='Titel', anchor='w', font='Arial 20 bold')
        self.labelUsername = tk.Label(master=self.frameData, text='Username', anchor='w', font='Arial 20 bold')
        self.labelPassword = tk.Label(master=self.frameData, text='Passwort', anchor='w', font='Arial 20 bold')
        self.labelEMail = tk.Label(master=self.frameData, text='E-Mail', anchor='w', font='Arial 20 bold')    
        
        self.labelTitleFill = tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16')
        self.labelUsernameFill= tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16')
        self.labelPasswordFill = tk.Entry(master=self.framePassword, bd=2, justify='center', relief='raised', font='Arial 16', state='readonly', show='*')
        self.buttonPasswordCopy = tk.Button(master=self.framePassword, text='Copy')
        self.labelEMailFill = tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16') 
        
        self.labelTitle.pack(side='top', padx=5, pady=5, fill='both')
        self.labelTitleFill.pack(side='top', padx=5, pady=5, fill='both')
        self.labelUsername.pack(side='top', padx=5, pady=5, fill='both')
        self.labelUsernameFill.pack(side='top', padx=5, pady=5, fill='both')
        self.labelPassword.pack(side='top', padx=5, pady=5, fill='both')
        self.framePassword.pack(side='top', fill='both')
        self.labelPasswordFill.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        self.buttonPasswordCopy.pack(side='right', padx=5, pady=5)
        self.labelEMail.pack(side='top', padx=5, pady=5, fill='both')
        self.labelEMailFill.pack(side='top', padx=5, pady=5, fill='both')  
        
        self.buttonPasswordCopy.bind('<1>', self.pressCopy)
        self.labelPasswordFill.bind('<Control-c>', self.pressCopy)
        
    def __buildFramePic__(self, parent):
        '''
        Build the frame right
        Show from the selected passwordobject the location and the note
        '''
        
        self.framePic = tk.Frame(master=parent)
        self.framePic.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.labelNote = tk.Label(master=self.framePic, text='Bemerkung', anchor='w', font='Arial 20 bold')
        self.labelNoteFill = tk.Label(master=self.framePic, text='', bg='white', justify='left', relief='raised', font='Arial')
        self.labelLocationLink = tk.Label(master=self.framePic, text='Location / URL', anchor='w', font='Arial 20 bold')
        self.labelLocationLinkFill = tk.Label(master=self.framePic, text='', justify='left', relief='raised', font='Arial 16')
        self.buttonLock = tk.Button(master=self.framePic, text='Lock', command=self.presslock)
        self.labelTime = tk.Label(master=self.framePic, anchor='e')
        
        self.labelLocationLink.pack(side='top', fill='both', padx=5, pady=5)
        self.labelLocationLinkFill.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNote.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNoteFill.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        self.labelTime.pack(side='bottom')
        self.buttonLock.pack(side='bottom', fill='both', padx=5, pady=5)    
        
    def __buildMenuBar__(self, parent):
        '''
        Build the MenuBar
        '''
        
        self.menuBar = tk.Menu(master=parent)
        
        self.fileMenu = tk.Menu(master=self.menuBar, tearoff=0)
        self.fileMenu.add_command(label='Options', command=self.pressoptions)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        
        self.passMenu = tk.Menu(master=self.menuBar, tearoff=0)      
        self.passMenu.add_command(label='New Password', command=self.pressnewpass)
        self.passMenu.add_command(label='Delete Password', command=self.pressremovepass)
        self.passMenu.add_command(label='Change Password', command=self.presschangepass)
        self.menuBar.add_cascade(label='Password', menu=self.passMenu)
        
        self.mainWindow.config(menu=self.menuBar) 
        
    def __initLockFrame__(self, parent):
        '''
        Constructor
        '''
        
        self.lockframe = tk.Frame(master=parent)
        self.lockframe.pack(fill='both', expand=True)
        self.__buildLockFrame(self.lockframe)
        self.__buildMenuBarLock__(self.lockframe)

    def __buildLockFrame(self, parent):
        self.frameLock = tk.Frame(master=parent)
#         self.labelFunny = tk.Label(master=self.frameLock,fg='red', text='YOU\nSHALL\nNOT\nPASS!', font='Arial 72 bold')
        self.framePassphrase = tk.Frame(master=self.frameLock)
        self.labelPassphrase = tk.Label(master=self.framePassphrase, text='Please insert your Passphrase:')
        self.entryPassphrase = tk.Entry(master=self.framePassphrase, justify='center', show='*')
        self.labelFalse = tk.Label(master=self.framePassphrase, text='', fg='red')
        self.buttonUnlock = tk.Button(master=self.frameLock, text='Unlock')
        self.buttonUnlock.bind('<1>', self.pressunlock)
        self.entryPassphrase.bind('<Return>', self.pressunlock)
        
        
        
        self.frameLock.pack(side='top', fill='both', expand=True)
#         self.labelFunny.pack(expand=True)
        self.framePassphrase.place(relx=0.4, rely=0.4)
        self.labelPassphrase.pack(side='top', padx=5, pady=5, fill='both')
        self.entryPassphrase.pack(side='top', fill='both', padx=5, pady=5)
        self.labelFalse.pack(side='top', fill='both', padx=5, pady=5)
        self.buttonUnlock.pack(side='bottom', anchor='se')   
        
    def __buildMenuBarLock__(self, parent):
        '''
        Build the MenuBar if the window is locked
        '''
        
        self.menuBarLocked = tk.Menu(master=parent)
        
        self.fileMenu = tk.Menu(master=self.menuBarLocked, tearoff=0)
        self.fileMenu.add_command(label='Options', command=self.pressoptions)
        self.menuBarLocked.add_cascade(label='File', menu=self.fileMenu)
        
        self.mainWindow.config(menu=self.menuBarLocked) 
        
    def insertTitleBox(self, passSafe):
        '''
        Reloaded the TitleBox if some Objects will be removed or changed
        '''
        self.titleBox.delete(0, 'end')
        
        for passOb in passSafe:
            self.titleBox.insert('end', str(passOb.getTitle()))
        self.titleBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.titleBox.yview)
    
    def selectedTitle(self, event):
        try:
            index = self.getTitleBoxIndex()    
            self.maincontroller.loadPassOb(int(index))
        except:
            pass
        
    def getTitleBoxIndex(self):

        index = self.titleBox.curselection()
        index = index[0]
            
        return int(index)
    
    def setTitleBoxIndexUp(self, event):
        try:
            index = self.getTitleBoxIndex()
            if index != 0:
                self.titleBox.select_clear(0, 'end')
                self.titleBox.select_set(index-1)
                self.maincontroller.loadPassOb(int(index-1))
        except:
            pass
        
    def setTitleBoxIndexDown(self, event):
        try:
            index = self.getTitleBoxIndex()
            if index != len(self.titleBox.get(0, 'end')):
                self.titleBox.select_clear(0, 'end')
                self.titleBox.select_set(index+1)
                self.maincontroller.loadPassOb(int(index+1))
        except:
            pass
        
    def setfills(self, title, username, password, email, location, note):
        self.labelTitleFill.config(text=str(title))
        self.labelUsernameFill.config(text=str(username))
        self.labelPasswordFill.config(state='normal')
        self.labelPasswordFill.delete(0, 'end')
        self.labelPasswordFill.insert('end', str(password))
        self.labelPasswordFill.config(state='readonly')
        self.labelEMailFill.config(text=str(email))
        self.labelLocationLinkFill.config(text=str(location))
        self.labelNoteFill.config(text=str(note))
            
    def getlockframe(self):
        return self.lockframe
    
    def getunlockframe(self):
        return self.unlockframe
    
    def getmainwindow(self):
        return self.mainWindow
    
    def setlockframe(self):
        self.__initLockFrame__(self.mainWindow)
        
    def setunlockframe(self):
        self.__initUnlockFrame__(self.mainWindow)
        
    def showunlockframe(self):
        if self.lockframe != None:
            self.lockframe.destroy()
        self.__initUnlockFrame__(self.mainWindow)
        
    def showlockframe(self):
        if self.unlockframe != None:
            self.unlockframe.destroy()
        self.__initLockFrame__(self.mainWindow)
        
    def showoptionerror(self):
        showerror('Error 404-File not found', 'No Options found.\nPlease open Options, choose an account\nand save it.')
        
    def showobjecterror(self):
        showerror('Error', 'No Object is chosen.\nPleas choose an Object!')
    
    def pressoptions(self):
        self.maincontroller.pressoptions()
    
    def presslock(self):
        self.maincontroller.pressmainLock()
            
    def pressunlock(self, event):
        passphrase = self.entryPassphrase.get()
        self.maincontroller.pressmainUnlock(passphrase)
        
    def pressnewpass(self):
        self.maincontroller.pressnewpass()
        
    def presschangepass(self):
        try:
            index = self.getTitleBoxIndex()
            self.maincontroller.presschangepass(index)    
        except:
            self.showobjecterror()
            
    def pressremovepass(self):
        try:
            index = self.getTitleBoxIndex()
            self.maincontroller.pressremovepass(index)
        except:
            self.showobjecterror()
            
    def pressCopy(self, event):
        entry = self.labelPasswordFill.get()
        self.maincontroller.pressCopy(entry)   
            
    def setlabelpassphrase(self):
        self.labelFalse.config(text='Your passphrase is wrong!')
        
    def setTime(self, time):
        self.labelTime.config(text='Autolock in '+str(time)+' seconds!') 
    
    def updatefilter(self, *args):
        filterstring = self.filterEntry.get()
        filterattribute = [self.checkTitle.get(), self.checkUsername.get(), self.checkPassword.get(),\
                           self.checkEmail.get(), self.checkLocation.get(), self.checkNote.get()]
        self.maincontroller.updatefilter(filterstring, filterattribute)
        
    def show(self):
        self.mainWindow.mainloop()   