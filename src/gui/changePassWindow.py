'''
Created on 16.04.2015

@author: crimsen
'''
import Tkinter as tk

class ChangePassWindow():
    
    def __init__(self, controller, index, title='', username='', password='', email='', location='', note=''):
        self.newPassWindow = tk.Tk()
        self.newPassWindow.title('Change Password')
        self.newPassWindow.geometry('400x320')
        
        self.__buildFrameData(str(title), str(username), str(password), str(email))
        self.__buildFramePic(str(location), str(note))
        
        self.buttonSave.config(text='Change')
        self.index = index
        self.maincontroller = controller
            
    def __buildFrameData(self, title='', username='', password='', email=''):
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
        
        self.entryTitle.insert('end', title)
        self.entryUsername.insert('end', username)
        self.entryPassword.insert('end', password)
        self.entryEMail.insert('end', email)
        
        self.labelTitle.pack(side='top', fill='both', padx=5, pady=5)
        self.entryTitle.pack(side='top', fill='both', padx=5, pady=5)
        self.labelUsername.pack(side='top', fill='both', padx=5, pady=5)
        self.entryUsername.pack(side='top', fill='both', padx=5, pady=5)
        self.labelPassword.pack(side='top', fill='both', padx=5, pady=5)
        self.entryPassword.pack(side='top', fill='both', padx=5, pady=5)
        self.labelEMail.pack(side='top', fill='both', padx=5, pady=5)
        self.entryEMail.pack(side='top', fill='both', padx=5, pady=5)
        
    def __buildFramePic(self, location='', note=''):
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
        
        self.entryLocation.insert('end', location)
        self.textNote.insert('end', note)
        
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
        
        title = self.entryTitle.get()
        username = self.entryUsername.get()
        password = self.entryPassword.get()
        email = self.entryEMail.get()
        location = self.entryLocation.get()
        note = self.textNote.get('1.0', 'end')
        
        self.maincontroller.presschangepasssave(self.index, title, username, password, email, location, note)
                
        print('title: '+ str(title))
        print('username: '+str(username))
        print('password: '+str(password))
        print('email: '+str(email))
        print('location: '+str(location))
        print('note: '+str(note))
                
        self.close() 
        
    def show(self):
        self.newPassWindow.mainloop()
        
    def close(self):
        self.newPassWindow.destroy() 