'''
Created on 12.05.2015

@author: timgroger
'''

import Tkinter as tk
import webbrowser
from Tkinter import StringVar
from tkMessageBox import showerror

class UnlockFrame(object):
    '''
    classdocs
    '''


    def __init__(self, mainWindow, mainController):
        '''
        Constructor
        '''
        self.filterEntry = StringVar()
        self.checkTitle = StringVar()
        self.checkUsername = StringVar()
        self.checkPassword = StringVar()
        self.checkEmail = StringVar()
        self.checkLocation = StringVar()
        self.checkNote = StringVar()
        self.mainWindow = mainWindow
        self.mainWindowFrame = self.mainWindow.getmainwindow()
        self.mainController = mainController
        
        self.unlockframe = tk.Frame(master=self.mainWindowFrame)
        self.unlockframe.pack(fill='both', expand=True)
        self.__buildFilterFrame__(self.unlockframe)
        self.__buildTitleBoxFrame__(self.unlockframe)
        self.__buildFrameData__(self.unlockframe)
        self.__buildFramePic__(self.unlockframe)
        self.__buildMenuBar__(self.unlockframe)
        self.__setDefault__()
        
        self.filterEntry.trace('w', self.updatefilter)
        self.checkTitle.trace('w', self.updatefilter)
        self.checkUsername.trace('w', self.updatefilter)
        self.checkPassword.trace('w', self.updatefilter)
        self.checkEmail.trace('w', self.updatefilter)
        self.checkLocation.trace('w', self.updatefilter)
        self.checkNote.trace('w', self.updatefilter)
        
        self.unlockframe.bind('<Escape>', self.presslock)
        self.titleBox.bind('<Escape>', self.presslock)
        self.frameData.bind('<Escape>', self.presslock)
        self.framePic.bind('<Escape>', self.presslock)
        self.labelPasswordFill.bind('<Escape>', self.presslock)

        
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
        
        self.mainWindowFrame.bind('<Alt-t>', lambda e: self.buttonFilterTitle.toggle())
        self.mainWindowFrame.bind('<Alt-u>', lambda e: self.buttonFilterUsername.toggle())
        self.mainWindowFrame.bind('<Alt-a>', lambda e: self.buttonFilterPassword.toggle())
        self.mainWindowFrame.bind('<Alt-e>', lambda e: self.buttonFilterEmail.toggle())
        self.mainWindowFrame.bind('<Alt-o>', lambda e: self.buttonFilterLocation.toggle())
        self.mainWindowFrame.bind('<Alt-n>', lambda e: self.buttonFilterNote.toggle())
        
        self.entryFilter.bind('<Up>', self.setTitleBoxIndexUp)
        self.entryFilter.bind('<Down>', self.setTitleBoxIndexDown)
        self.entryFilter.focus_force()
        
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
        self.buttonPasswordCopy = tk.Button(master=self.framePassword, text='Copy', underline=0)
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
        self.mainWindowFrame.bind('<Alt-c>', self.pressCopy)
        
    def __buildFramePic__(self, parent):
        '''
        Build the frame right
        Show from the selected passwordobject the location and the note
        '''
        
        self.framePic = tk.Frame(master=parent)
        self.framePic.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.labelNote = tk.Label(master=self.framePic, text='Bemerkung', anchor='w', font='Arial 20 bold')
        self.labelNoteFill = tk.Text(master=self.framePic, bg='white', relief='raised', font='Arial', height=16)
        self.labelLocationLink = tk.Label(master=self.framePic, text='Location / URL', anchor='w', font='Arial 20 bold')
        self.labelLocationLinkFill = tk.Label(master=self.framePic, text='', justify='left', relief='raised', font='Arial 16', fg='blue', cursor='hand2')
        self.buttonLock = tk.Button(master=self.framePic, text='Lock', underline=0)
        self.labelTime = tk.Label(master=self.framePic, anchor='e')
        
        self.labelLocationLink.pack(side='top', fill='both', padx=5, pady=5)
        self.labelLocationLinkFill.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNote.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNoteFill.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        self.labelTime.pack(side='bottom')
        self.buttonLock.pack(side='bottom', fill='both', padx=5, pady=5)  
        
        self.mainWindowFrame.bind('<Alt-l>', self.presslock)
        self.buttonLock.bind('<1>', self.presslock)
        self.buttonLock.bind('<Return>', self.presslock)  
        self.labelLocationLinkFill.bind('<1>', self.callLink)
        
    def __buildMenuBar__(self, parent):
        '''
        Build the MenuBar
        '''
        
        self.menuBar = tk.Menu(master=parent)
        
        self.fileMenu = tk.Menu(master=self.menuBar, tearoff=0)
        self.fileMenu.add_command(label='Options', underline=0, command=self.pressoptions)
        self.menuBar.add_cascade(label='File', underline=0, menu=self.fileMenu)
        
        self.passMenu = tk.Menu(master=self.menuBar, tearoff=0)      
        self.passMenu.add_command(label='New Password', underline=0, command=self.pressnewpass)
        self.passMenu.add_command(label='Delete Password', underline=0, command=self.pressremovepass)
        self.passMenu.add_command(label='Change Password', underline=0, command=self.presschangepass)
        self.passMenu.add_command(label='View History', underline=0, command=self.pressViewHistory)
        self.menuBar.add_cascade(label='Password', underline=0, menu=self.passMenu)
        
        self.menuBar.add_command(label='About', underline=1, command=self.pressAbout)
        
        self.mainWindowFrame.config(menu=self.menuBar)
        
    def hide(self):
        self.mainWindowFrame.unbind('<Alt-t>')
        self.mainWindowFrame.unbind('<Alt-u>')
        self.mainWindowFrame.unbind('<Alt-a>')
        self.mainWindowFrame.unbind('<Alt-e>')
        self.mainWindowFrame.unbind('<Alt-o>')
        self.mainWindowFrame.unbind('<Alt-n>')
        self.mainWindowFrame.unbind('<Alt-l>')
        self.mainWindowFrame.unbind('<Alt-c>')

    def insertTitleBox(self, passSafe):
        '''
        Reloaded the TitleBox if some Objects will be removed or changed
        '''
        self.titleBox.delete(0, 'end')
        
        for passOb in passSafe:
            self.titleBox.insert('end', passOb.getTitle())
        self.titleBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.titleBox.yview)
    
    def selectedTitle(self, event):
        try:
            index = self.getTitleBoxIndex()    
            self.mainController.loadPassOb(int(index))
        except:
            pass
        
    def callLink(self, event):
        url = self.labelLocationLinkFill.cget('text')
        if 'http://' not in url:
            if 'https://' not in url:
                url = 'http://'+url
        webbrowser.open_new_tab(url)
        
    def setTitleBoxIndex(self, index):
        self.titleBox.select_clear(0, 'end')
        self.titleBox.select_set(index)
        self.mainController.loadPassOb(index)

    def getTitleBoxIndex(self):

        index = self.titleBox.curselection()
        index = index[0]
            
        return int(index)
    
    def setTitleBoxIndexUp(self, event):
        try:
            index = self.getTitleBoxIndex()
        except:
            index=len(self.titleBox.get(0, 'end'))-1
        if index != 0:
            self.setTitleBoxIndex(index-1)

    def setTitleBoxIndexDown(self, event):
        try:
            index = self.getTitleBoxIndex()
        except:
            index=0
        if index != (len(self.titleBox.get(0, 'end'))-1):
            self.setTitleBoxIndex(index+1)
        
    def setfills(self, title, username, password, email, location, note):
        self.labelTitleFill.config(text=title)
        self.labelUsernameFill.config(text=username)
        self.labelPasswordFill.config(state='normal')
        self.labelPasswordFill.delete(0, 'end')
        self.labelPasswordFill.insert('end', password)
        self.labelPasswordFill.config(state='readonly')
        self.labelEMailFill.config(text=email)
        self.labelLocationLinkFill.config(text=location)
        self.labelNoteFill.config(state='normal')
        self.labelNoteFill.delete(1.0, 'end')
        self.labelNoteFill.insert('end', note)
        self.labelNoteFill.config(state='disabled')
        
    def updatefilter(self, *args):
        filterstring = self.filterEntry.get()
        filterattribute = [self.checkTitle.get(), self.checkUsername.get(), self.checkPassword.get(),\
                           self.checkEmail.get(), self.checkLocation.get(), self.checkNote.get()]
        self.mainController.updatefilter(filterstring, filterattribute)
        
    def presslock(self, event):
        self.mainWindow.presslock() 

    def pressoptions(self):
        self.mainWindow.pressoptions()
        
    def pressCopy(self, event):
        entry = self.labelPasswordFill.get()
        self.mainController.pressCopy(entry)
        
    def pressremovepass(self):
        try:
            index = self.getTitleBoxIndex()
            self.mainController.pressremovepass(index)
        except:
            self.showobjecterror()
            
    def pressnewpass(self):
        self.mainController.pressnewpass()
        
    def pressViewHistory(self):
        try:
            index = self.getTitleBoxIndex()
            self.mainController.pressViewHistory(index)
        except:
            self.showobjecterror()
        
    def presschangepass(self):
        try:
            index = self.getTitleBoxIndex()
            self.mainController.presschangepass(index)    
        except:
            self.showobjecterror()
            
    def pressAbout(self):
        self.mainController.pressAbout()
            
    def setTime(self, time):
        text = ''
        if None != time:
            text = 'Autolock in '+str(time)+' seconds!'
        self.labelTime.config(text=text)

    def showoptionerror(self):
        showerror('Error 404-File not found', 'No Options found.\nPlease open Options, choose an account\nand save it.')
        
    def showobjecterror(self):
        showerror('Error', 'No Object is chosen.\nPleas choose an Object!')
        
    def destroy(self):
        self.unlockframe.destroy()
