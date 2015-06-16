'''
Created on 14.06.2015

@author: timgroger
'''

import Tkinter as Tk
# from model.HistoryPasswordObject import HistoryPasswordObject
# import datetime

class HistoryFrame(Tk.Frame):
    '''
    classdocs
    '''


    def __init__(self, parent,mainController, passOb):
        '''
        Constructor
        '''
        self.parent = parent
        self.passOb = passOb
        self.mainController = mainController
        Tk.Frame.__init__(self, master=self.parent)
        self.__buildFrame__(self.parent, self.passOb)
        
    def __buildFrame__(self, parent, passOb):
        self.endDate = passOb.getEndDate().isoformat()
        self.createDate = passOb.getCreateDate().isoformat()
        self.title = passOb.getTitle()
        self.username = passOb.getUsername()
        self.password = passOb.getPassword()
        self.email = passOb.getEmail()
        self.location = passOb.getLocation()
        self.note = passOb.getNote()
        
        self.data = [self.createDate, self.title, self.username, self.password, self.email, self.location, self.note]
        
        self.mainFrame = Tk.Frame(master=parent, relief='groove', bd=2)
        
        self.labelEndDate = Tk.Label(master=self.mainFrame, text='EndDate', anchor='w')
        self.labelCreateDate = Tk.Label(master=self.mainFrame, text='CreateDate', anchor='w')
        self.labelTitle = Tk.Label(master=self.mainFrame, text='Title', anchor='w')
        self.labelUsername = Tk.Label(master=self.mainFrame, text='Username', anchor='w')
        self.labelPassword  = Tk.Label(master=self.mainFrame, text='Password', anchor='w')
        self.labelEmail = Tk.Label(master=self.mainFrame, text='E-Mail', anchor='w')
        self.labelLocation = Tk.Label(master=self.mainFrame, text='Location', anchor='w')
        self.labelNote = Tk.Label(master=self.mainFrame, text='Note', anchor='w')
        
        self.labelEndDateFill = Tk.Label(master=self.mainFrame, text=self.endDate)
        self.textCreateDate = Tk.Text(master=self.mainFrame, width=10, height=3)
        self.textTitle = Tk.Text(master=self.mainFrame, width=10, height=3)
        self.textUsername = Tk.Text(master=self.mainFrame, width=10, height=3)
        
        self.framePassword = Tk.Frame(master=self.mainFrame)
        self.entryPassword = Tk.Entry(master=self.framePassword, width=10, state='readonly', show='*')
        self.buttonPassword = Tk.Button(master=self.framePassword, text='Copy')
        self.entryPassword.pack(side='top', fill='both', anchor='w')
        self.buttonPassword.pack(side='top', fill='both')
        
        self.textEmail = Tk.Text(master=self.mainFrame, width=10, height=3)
        self.textLocation = Tk.Text(master=self.mainFrame, width=10, height=3)
        self.textNote = Tk.Text(master=self.mainFrame, width=10, height=3)
        
        self.entryPassword.bind('<Control-c>', self.pressCopy)
        self.buttonPassword.bind('<1>', self.pressCopy)
        
        
        self.mainFrame.pack(side='top', padx=5, pady=5)
        
        self.line1 = [self.labelEndDate, self.labelEndDateFill]
        self.line2 = [self.labelCreateDate, self.labelTitle, self.labelUsername,
                       self.labelPassword, self.labelEmail, self.labelLocation, self.labelNote]
        self.line3 = [self.textCreateDate, self.textTitle, self.textUsername, 
                      self.framePassword, self.textEmail,  self.textLocation, self.textNote]
        self.line4 = [self.textCreateDate, self.textTitle, self.textUsername, 
                      self.entryPassword, self.textEmail,  self.textLocation, self.textNote]
        
        self.__buildTable__(self.line1, 0)
        self.__buildTable__(self.line2, 1)
        self.__buildTable__(self.line3, 2)
        
        self.__insertData__(self.line4, self.data)
    
    def pressCopy(self, event):
        entry = self.entryPassword.get()
        self.mainController.pressCopy(entry)
    
    def __buildTable__(self, line, row):
        i=0
        for object in line:
            object.grid(column=i, row=row, padx=5, pady=5)
            i+=1
            
    def __insertData__(self, line, data):
        i = 0
        for object in line:
            object.config(state='normal')
            object.insert('end', data[i])
            try:
                object.config(state='readonly')
            except:
                object.config(state='disabled')
            i+=1
            
# if __name__ == '__main__':
#     root = Tk.Tk()
#     passOb = HistoryPasswordObject('Title', 'username', 'password', 'email', 'location', 'note', datetime.date.today(), datetime.date.today())
#     frame = HistoryFrame(root, passOb)
#     frame.pack(side='top')
#     root.mainloop()
        