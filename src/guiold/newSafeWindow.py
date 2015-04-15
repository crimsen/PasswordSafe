'''
Created on 28.03.2015

@author: crimsen
'''
import Tkinter as tk

class NewSafeWindow(object):
    #Build a new Window for a new PasswordObject


    def __init__(self, passwordsafe, test, title='', username='', password='', email='', location='', note=''):
        
        self.newPassWindow = tk.Tk()
        self.newPassWindow.title('New Password')
        self.newPassWindow.geometry('400x320')
        
        self.__buildFrameData()
        self.__buildFramePic()
        
        self.gui = test
        
        self.passSafe = passwordsafe
        
    def __buildFrameData(self):
        '''
        Build the frame left with the title, the username, the password and the emal
        The user has to fill the entrys
        '''
        
        self.frameData = tk.Frame(master=self.newPassWindow)
        self.frameData.pack(side='left', fill='both', padx=5, pady=5, expand=True)
        
        self.labelTitle = tk.Label(master=self.frameData, text='Titel', anchor='w', font='Arial 18 bold')
        self.labelUsername = tk.Label(master=self.frameData, text='Username', anchor='w', font='Arial 18 bold')
        self.labelPassword = tk.Label(master=self.frameData, text='Passwort', anchor='w', font='Arial 18 bold')
        self.labelEMail = tk.Label(master=self.frameData, text='E-Mail', anchor='w', font='Arial 18 bold')
        
        self.entryTitle = tk.Entry(master=self.frameData)
        self.entryUsername = tk.Entry(master=self.frameData)
        self.entryPassword = tk.Entry(master=self.frameData)
        self.entryEMail = tk.Entry(master=self.frameData)
        
        self.labelTitle.pack(side='top', fill='both', padx=5, pady=5)
        self.entryTitle.pack(side='top', fill='both', padx=5, pady=5)
        self.labelUsername.pack(side='top', fill='both', padx=5, pady=5)
        self.entryUsername.pack(side='top', fill='both', padx=5, pady=5)
        self.labelPassword.pack(side='top', fill='both', padx=5, pady=5)
        self.entryPassword.pack(side='top', fill='both', padx=5, pady=5)
        self.labelEMail.pack(side='top', fill='both', padx=5, pady=5)
        self.entryEMail.pack(side='top', fill='both', padx=5, pady=5)
        
    def __buildFramePic(self):
        '''
        Build the fram right with the location and the note
        The user has to fill the entrys
        '''
        
        self.framePic = tk.Frame(master=self.newPassWindow)
        self.framePic.pack(side='left', fill='both', padx=5, pady=5, expand=True)
        
        self.labelLocation = tk.Label(master=self.framePic, text='Location / URL', anchor='w', font='Arial 18 bold')
        self.entryLocation = tk.Entry(master=self.framePic)
        self.labelNote = tk.Label(master=self.framePic, text='Note', anchor='w', font='Arial 18 bold')
        self.textNote = tk.Text(master=self.framePic, height=3, bd=2, relief='flat')
        self.buttonSave = tk.Button(master=self.framePic, text='Save', command=self.pressSave)
        self.buttonCancel = tk.Button(master=self.framePic, text='Cancel', command=self.pressCancel)
        
        self.labelLocation.pack(side='top', fill='both', padx=5, pady=5)
        self.entryLocation.pack(side='top', fill='both', padx=5, pady=5)
        self.labelNote.pack(side='top', fill='both', padx=5, pady=5)
        self.textNote.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        self.buttonSave.pack(side='top', fill='both', padx=5, pady=5)
        self.buttonCancel.pack(side='top', fill='both', padx=5, pady=5)
    
    def pressCancel(self):
        '''
        Destroy the widget
        '''
        self.close()
    
    def pressSave(self):
        '''
        Set a new passwordobject
        And destroy the widget
        '''
        
        etitle = self.entryTitle.get()
        eusername = self.entryUsername.get()
        epassword = self.entryPassword.get()
        eemail = self.entryEMail.get()
        elocation = self.entryLocation.get()
        enote = self.textNote.get('1.0', 'end')
        
        self.passSafe.newPassObject(title=etitle, username=eusername, password=epassword, email=eemail, location=elocation, note=enote)
        
        print('title: '+ str(etitle))
        print('username: '+str(eusername))
        print('password: '+str(epassword))
        print('email: '+str(eemail))
        print('location: '+str(elocation))
        print('note: '+str(enote))
        
        self.gui.insertTitleBox()
                
        self.close()
        
   
    def show(self):
        self.newPassWindow.mainloop()
        
    def close(self):
        self.newPassWindow.destroy()
