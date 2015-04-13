'''
Created on 27.03.2015

@author: crimsen
'''
import Tkinter as tk
import os
import xml.dom.minidom
from gui.newSafeWindow import NewSafeWindow
from model.passSafe import PasswordSafe
from gui.changeSafeWindow import ChangeSafeWindow
from gui.optionWindow import OptionWindow
from tkMessageBox import showerror


class MainWindow():
    #Set and build the layout of the mainWindow

    def __init__(self):
        
        self.mainWindow = tk.Tk()
        self.mainWindow.title('Passwordsafe')
        self.mainWindow.geometry('900x500')
        
        self.__searchSafeFiles()
        self.__lockWidget()
                
    def __buildTitleBox(self):
        '''
        Build the TitleBox
        Show all passwordobjects
        '''
        
        self.titleBox = tk.Listbox(master=self.framePassSafe, selectmode='single', width=30)
        self.titleBox.pack(side='left', fill='both', padx=5 ,pady=5)
        
        self.titleBox.delete(0, 'end')
        
        for i in self.passSafe.getSafe():
            self.titleBox.insert('end', str(i.getTitle()))
            
        self.titleBox.bind('<Button-1>', self.selectedTitle)

    def __buildFrameData(self):
        '''
        Buil the frame in the middle
        Show from the selected passwordobject the title, the username, the password and the email
        '''
        
        self.frameData = tk.Frame(master=self.framePassSafe)
        self.frameData.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.labelTitle = tk.Label(master=self.frameData, text='Titel', anchor='w', font='Arial 20 bold')
        self.labelUsername = tk.Label(master=self.frameData, text='Username', anchor='w', font='Arial 20 bold')
        self.labelPassword = tk.Label(master=self.frameData, text='Passwort', anchor='w', font='Arial 20 bold')
        self.labelEMail = tk.Label(master=self.frameData, text='E-Mail', anchor='w', font='Arial 20 bold')
        
        self.labelTitleFill = tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16')
        self.labelUsernameFill= tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16')
        self.labelPasswordFill = tk.Entry(master=self.frameData, bd=2, justify='center', relief='raised', font='Arial 16')
        self.labelEMailFill = tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16') 
        
        self.labelTitle.pack(side='top', padx=5, pady=5, fill='both')
        self.labelTitleFill.pack(side='top', padx=5, pady=5, fill='both')
        self.labelUsername.pack(side='top', padx=5, pady=5, fill='both')
        self.labelUsernameFill.pack(side='top', padx=5, pady=5, fill='both')
        self.labelPassword.pack(side='top', padx=5, pady=5, fill='both')
        self.labelPasswordFill.pack(side='top', padx=5, pady=5, fill='both')
        self.labelEMail.pack(side='top', padx=5, pady=5, fill='both')
        self.labelEMailFill.pack(side='top', padx=5, pady=5, fill='both')  
        
    def __buildFramePic(self):
        '''
        Build the frame right
        Show from the selected passwordobject the location and the note
        '''
        
        self.framePic = tk.Frame(master=self.framePassSafe)
        self.framePic.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.labelNote = tk.Label(master=self.framePic, text='Bemerkung', anchor='w', font='Arial 20 bold')
        self.labelNoteFill = tk.Label(master=self.framePic, text='', bg='white', justify='left', relief='raised', font='Arial')
        self.labelLocationLink = tk.Label(master=self.framePic, text='Location / URL', anchor='w', font='Arial 20 bold')
        self.labelLocationLinkFill = tk.Label(master=self.framePic, text='', justify='left', relief='raised', font='Arial 16')
        self.buttonLock = tk.Button(master=self.framePic, text='Lock', command=self.__pressLock)
        
        self.labelLocationLink.pack(side='top', fill='both', padx=5, pady=5)
        self.labelLocationLinkFill.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNote.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNoteFill.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        self.buttonLock.pack(side='bottom', fill='both', padx=5, pady=5)
        
    def __buildMenuBar(self):
        '''
        Build the MenuBar
        '''
        
        self.menuBar = tk.Menu(master=self.framePassSafe)
        
        self.fileMenu = tk.Menu(master=self.menuBar, tearoff=0)
        self.fileMenu.add_command(label='Options', command=self.optionWindow)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        
        self.passMenu = tk.Menu(master=self.menuBar, tearoff=0)      
        self.passMenu.add_command(label='New Password', command=self.newWindow)
        self.passMenu.add_command(label='Delete Password', command=self.removePassOb)
        self.passMenu.add_command(label='Change Password', command=self.changePassOb)
        self.menuBar.add_cascade(label='Password', menu=self.passMenu)
        
        self.mainWindow.config(menu=self.menuBar)
        
    def __buildMenuBarLock(self):
        '''
        Build the MenuBar if the window is locked
        '''
        
        self.menuBarLocked = tk.Menu(master=self.frameLock)
        
        self.fileMenu = tk.Menu(master=self.menuBarLocked, tearoff=0)
        self.fileMenu.add_command(label='Options', command=self.optionWindow)
        self.menuBarLocked.add_cascade(label='File', menu=self.fileMenu)
        
        self.mainWindow.config(menu=self.menuBarLocked)
        
    def optionWindow(self):
        
        optWindow = OptionWindow(filename=self.optionfile)
        optWindow.show()
            
    def insertTitleBox(self):
        '''
        Reloaded the TitleBox if some Objects will be removed or changed
        '''
        self.titleBox.delete(0, 'end')
        
        for passOb in self.passSafe.getSafe():
            self.titleBox.insert('end', str(passOb.getTitle()))
            
#        i = self.titleBox.size()
#        title = self.passSafe.getSafeIndex(i).getTitle()
#        self.titleBox.insert(i, str(title))  

    def deleteTitleBox(self):
        self.titleBox.delete(0, 'end')
                  
    def newWindow(self):
        '''
        Create a new window to create a new passwordobject
        '''
        
        passWindow = NewSafeWindow(self.passSafe, self)
        passWindow.show()
        
    def selectedTitle(self, event):
        '''
        Look which passwordobject is selected to show it
        '''
        
        try:
            index = 0
            index = self.titleBox.curselection()
            index = index[0]
            
        
            title = self.controlNone(self.passSafe.getSafe()[index].getTitle())
            username = self.controlNone(self.passSafe.getSafe()[index].getUsername())
            password = self.controlNone(self.passSafe.getSafe()[index].getPassword())
            email = self.controlNone(self.passSafe.getSafe()[index].getEmail())
            location = self.controlNone(self.passSafe.getSafe()[index].getLocation())
            note = self.controlNone(self.passSafe.getSafe()[index].getNote())
            self.loadData(title=str(title), username=str(username), password=str(password), email=str(email), location=str(location), note=str(note)) 
        except:
            pass
        
        
    def lock(self):
        self.framePic.destroy()
        self.frameData.destroy()
        self.menuBar.destroy()
        self.titleBox.destroy()
          
          
    def __lockWidget(self):
        self.frameLock = tk.Frame(master=self.mainWindow)
        self.__buildMenuBarLock()
        self.labelFunny = tk.Label(master=self.frameLock,fg='red', text='YOU\nSHALL\nNOT\nPASS!', font='Arial 72 bold')
#         self.framePassphrase = tk.Frame(master=self.frameLock, bg='green')
#         self.labelPassphrase = tk.Label(master=self.framePassphrase, text='Please insert your Passphrase:')
#         self.entryPassphrase = tk.Entry(master=self.framePassphrase, justify='center')
#         self.labelFalse = tk.Label(master=self.framePassphrase, text='')
        self.buttonUnlock = tk.Button(master=self.frameLock, text='Unlock', command=self.__pressUnlock)
        
        
        
        self.frameLock.pack(side='top', fill='both', expand=True)
        self.labelFunny.pack(expand=True)
#         self.framePassphrase.place(relx=0.4, rely=0.4)
#         self.labelPassphrase.pack(side='top', padx=5, pady=5, fill='both')
#         self.entryPassphrase.pack(side='top', fill='both', padx=5, pady=5)
#         self.labelFalse.pack(side='top', fill='both', padx=5, pady=5)
        self.buttonUnlock.pack(side='bottom', anchor='se') 
    
    def __pressLock(self):
        self.deleteTitleBox()
        self.titleBox.destroy()     
        self.framePassSafe.destroy()
        self.passSafe.close()
        self.passSafe = None
        self.__lockWidget()
    
    def __pressUnlock(self):
        try:
            self.loadOptions()
            self.frameLock.destroy()
            self.__unlockWidget()
        except:
            showerror('ERROR', 'You haven\'t an optionfile.\nPleas go in Options and save it.')
    def removePassOb(self):
        '''
        Remove the selected passwordobject
        '''
        
        selected = self.titleBox.curselection()
        
        if selected == ():
            index = 0
            print('index existiert nicht')
        else:
            index = self.titleBox.curselection()
            index = index[0]
            print('done')
            self.passSafe.removePassOb(index)
            self.insertTitleBox()
            
    def changePassOb(self):
        '''
        Create a new window to change the selected passwordobject
        '''
        
        selected = self.titleBox.curselection()
        
        if selected == ():
            index = 0
            print('nichts')
        else:
            print('hier wird was')
            index = self.titleBox.curselection()[0]
            passOb = self.passSafe.getSafe()[index]
            title = passOb.getTitle()
            username = passOb.getUsername()
            password = passOb.getPassword()
            email = passOb.getEmail()
            location = passOb.getLocation()
            
            passWindow = ChangeSafeWindow(self.passSafe, self, index, title, username, password, email, location)
            passWindow.show()    
       
    def loadData(self, title='', username='', password='', email='', location='', note=''):
        '''
        Reload the frames to show the title, the password, the email, the location and the note
        '''
        self.labelTitleFill.config(text=str(title))
        self.labelUsernameFill.config(text=str(username))
        self.labelPasswordFill.config(state='normal')
        self.labelPasswordFill.delete(0, 'end')
        self.labelPasswordFill.insert(0, password)
        self.labelPasswordFill.config(state='readonly')
        self.labelEMailFill.config(text=str(email))
        self.labelLocationLinkFill.config(text=str(location))
        self.labelNoteFill.config(text=str(note))
        
    def controlNone(self, attr):
        
        if attr == 'None':
            retVal = ''
        else:
            retVal = attr
            
        return retVal
        
    def __unlockWidget(self):
        
        self.passSafe = PasswordSafe(self.safefile, self.account)
        self.__passSafeWidget()
        self.loadData()
        
    def __passSafeWidget(self):
        
        self.framePassSafe = tk.Frame(master=self.mainWindow)      
        self.__buildMenuBar()
        self.__buildTitleBox()
        self.__buildFrameData()    
        self.__buildFramePic()
        self.framePassSafe.pack(fill='both', expand=True)    
        
    
    def __searchSafeFiles(self):
        home = os.environ['HOME']
        self.safefile = home+'/Documents/.PasswordSafe/safe.xml'
        self.optionfile = home+'/Documents/.PasswordSafe/option.xml'
        self.dirfile = os.path.dirname(self.safefile)
        if not os.path.exists(self.dirfile):
            os.makedirs(self.dirfile)
        print(str(self.dirfile))
        
    def loadOptions(self):
        
      
        datei = open(self.optionfile, "r")
        dom = xml.dom.minidom.parse(datei)
        datei.close()
        
        for elem in dom.getElementsByTagName('Options'):
            for elem1 in elem.getElementsByTagName('ActivateEmail'):
                self.account = self.liesText(elem1)
     
    
    def liesText(self, knoten):
        '''
        Return the text of the nodeType
        '''
        for k in knoten.childNodes:
            if k.nodeType == k.TEXT_NODE:
                return k.nodeValue.strip()
        
    def show(self):
        self.mainWindow.mainloop()       
        