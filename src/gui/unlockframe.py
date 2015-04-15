'''
Created on 15.04.2015

@author: crimsen
'''
from Tkinter import Frame
import Tkinter as tk

class UnlockFrame(Frame):
    '''
    classdocs
    '''


    def __init__(self, parent, mainwindow):
        '''
        Constructor
        '''
        
        self.mainwindow = mainwindow
        Frame.__init__(self, parent)
        self.parent = parent
        self.__buildTitleBoxFrame__(self.parent)
        self.__buildFrameData__(self.parent)
        self.__buildFramePic__(self.parent)
        self.__buildMenuBar__(self.parent)
        
        
    def __buildTitleBoxFrame__(self, parent):
        '''
        Build the TitleBox
        Show all passwordobjects
        '''
        
        self.titleBox = tk.Listbox(master=parent, selectmode='single', width=30)
        self.titleBox.pack(side='left', fill='both', padx=5 ,pady=5)
        
        self.titleBox.delete(0, 'end')
        
#         for i in self.passSafe.getSafe():
#             self.titleBox.insert('end', str(i.getTitle()))
#             
#         self.titleBox.bind('<Button-1>', self.selectedTitle)

    def __buildFrameData__(self, parent):
        '''
        Buil the frame in the middle
        Show from the selected passwordobject the title, the username, the password and the email
        '''
        
        self.frameData = tk.Frame(master=parent)
        self.frameData.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.labelTitle = tk.Label(master=self.frameData, text='Titel', anchor='w', font='Arial 20 bold')
        self.labelUsername = tk.Label(master=self.frameData, text='Username', anchor='w', font='Arial 20 bold')
        self.labelPassword = tk.Label(master=self.frameData, text='Passwort', anchor='w', font='Arial 20 bold')
        self.labelEMail = tk.Label(master=self.frameData, text='E-Mail', anchor='w', font='Arial 20 bold')
        
        self.labelTitleFill = tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16')
        self.labelUsernameFill= tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16')
        self.labelPasswordFill = tk.Entry(master=self.frameData, bd=2, justify='center', relief='raised', font='Arial 16', state='readonly')
        self.labelEMailFill = tk.Label(master=self.frameData, text='', relief='raised', font='Arial 16') 
        
        self.labelTitle.pack(side='top', padx=5, pady=5, fill='both')
        self.labelTitleFill.pack(side='top', padx=5, pady=5, fill='both')
        self.labelUsername.pack(side='top', padx=5, pady=5, fill='both')
        self.labelUsernameFill.pack(side='top', padx=5, pady=5, fill='both')
        self.labelPassword.pack(side='top', padx=5, pady=5, fill='both')
        self.labelPasswordFill.pack(side='top', padx=5, pady=5, fill='both')
        self.labelEMail.pack(side='top', padx=5, pady=5, fill='both')
        self.labelEMailFill.pack(side='top', padx=5, pady=5, fill='both')  
        
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
        self.buttonLock = tk.Button(master=self.framePic, text='Lock', command=self.onExit)
        
        self.labelLocationLink.pack(side='top', fill='both', padx=5, pady=5)
        self.labelLocationLinkFill.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNote.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNoteFill.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        self.buttonLock.pack(side='bottom', fill='both', padx=5, pady=5)    
        
    def __buildMenuBar__(self, parent):
        '''
        Build the MenuBar
        '''
        
        self.menuBar = tk.Menu(master=parent)
        
        self.fileMenu = tk.Menu(master=self.menuBar, tearoff=0)
        self.fileMenu.add_command(label='Options')
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        
        self.passMenu = tk.Menu(master=self.menuBar, tearoff=0)      
        self.passMenu.add_command(label='New Password')
        self.passMenu.add_command(label='Delete Password')
        self.passMenu.add_command(label='Change Password')
        self.menuBar.add_cascade(label='Password', menu=self.passMenu)
        
        self.parent.config(menu=self.menuBar)    