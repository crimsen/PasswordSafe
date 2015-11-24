'''
Created on 24.11.2015

@author: crimsen
'''
import Tkinter as tk

class HistoryWindow(object):
    '''
    classdocs
    '''


    def __init__(self, client, history):
        '''
        Constructor
        '''
        self.view = HistoryWindowView()
        self.controller = HistoryWindowController(self.view, client, history)
    
    def show(self):
        self.view.show()
        
    def close(self):
        self.controller.close()
        
class HistoryWindowModel(tk.Frame):
    
    def __init__(self, parent, passOb):
        self.parent = parent
        self.passOb = passOb
        self.controller = None
        
        tk.Frame.__init__(self, master=self.parent)
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
        
        self.data = [self.createDate, self.title, self.username,
                     self.password, self.email, self.location, self.note]
        
        self.historyFrame = tk.Frame(master=parent, relief='groove', bd=2)
        
        self.labelEndDate = tk.Label(master=self.historyFrame, text='EndDate', anchor='w')
        self.labelCreateDate = tk.Label(master=self.historyFrame, text='CreateDate', anchor='w')
        self.labelTitle = tk.Label(master=self.historyFrame, text='Title', anchor='w')
        self.labelUsername = tk.Label(master=self.historyFrame, text='Username', anchor='w')
        self.labelPassword  = tk.Label(master=self.historyFrame, text='Password', anchor='w')
        self.labelEmail = tk.Label(master=self.historyFrame, text='E-Mail', anchor='w')
        self.labelLocation = tk.Label(master=self.historyFrame, text='Location', anchor='w')
        self.labelNote = tk.Label(master=self.historyFrame, text='Note', anchor='w')
        
        self.labelEndDateFill = tk.Label(master=self.historyFrame, text=self.endDate)
        self.textCreateDate = tk.Text(master=self.historyFrame, width=10, height=3)
        self.textTitle = tk.Text(master=self.historyFrame, width=10, height=3)
        self.textUsername = tk.Text(master=self.historyFrame, width=10, height=3)
        
        self.framePassword = tk.Frame(master=self.historyFrame)
        self.entryPassword = tk.Entry(master=self.framePassword, width=10, state='readonly', show='*')
        self.buttonPassword = tk.Button(master=self.framePassword, text='Copy')
        self.entryPassword.pack(side='top', fill='both', anchor='w')
        self.buttonPassword.pack(side='top', fill='both')
        
        self.textEmail = tk.Text(master=self.historyFrame, width=10, height=3)
        self.textLocation = tk.Text(master=self.historyFrame, width=10, height=3)
        self.textNote = tk.Text(master=self.historyFrame, width=10, height=3)
        
        self.entryPassword.bind('<Control-c>', self.pressCopy)
        self.buttonPassword.bind('<1>', self.pressCopy)
        
        self.historyFrame.pack(side='top', padx=5, pady=5)
        
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
        if None != self.controller:
            entry = self.entryPassword.get()
            self.controller.copyToClipBoard(entry)
            
    def setController(self, controller):
        self.controller = controller
        
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
        
class HistoryWindowView(object):
    
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title('Passwordhistory')
        
        self.historyList = []
        self.controller = None
        
        self.__buildFrame(self.window)
        self.window.geometry('660x400')
    
    def __buildFrame(self, parent):
        self.mainFrame = tk.Frame(master=parent)
        self.mainFrame.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        self.canvas = tk.Canvas(master=self.mainFrame)
        self.windowFrame = tk.Frame(master=self.canvas)
        self.scrollbar = tk.Scrollbar(master=self.mainFrame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((0,0), window=self.windowFrame, anchor='nw')
        self.windowFrame.bind('<Configure>', self.configureCanvas)
        
    def configureCanvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def buildData(self, history):
        for passOb in history:
            self.historyList.append(HistoryWindowModel(self.windowFrame, passOb))
        for historyOb in self.historyList:    
            historyOb.pack(side='top', fill='both', padx=5, pady=5, expand=True)
    
    def setController(self, controller):
        for historyOb in self.historyList:
            historyOb.setController(controller)
    
    def show(self):
        self.window.mainloop()
        
    def close(self):
        self.window.destroy()
        
class HistoryWindowController(object):
    
    def __init__(self, view, client, history):
        self.view = view
        self.client = client
        self.history = history
        self.canvas = self.view.canvas
        
        self.view.buildData(self.history)
        
        self.historyList = self.view.historyList
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind_all('<Key-Up>', self.up)
        self.canvas.bind_all('<Key-Down>', self.down)
        self.canvas.bind_all('<Escape>', self.close)
        
        self.view.setController(self)
        
        
    def up(self, event):
        self.canvas.yview_scroll(-1, 'units')
    
    def down(self, event):
        self.canvas.yview_scroll(1, 'units')
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*event.delta, 'units')
    
    def close(self, *args):
        self.cleanUp()
        self.view.close()
    
    def cleanUp(self):
        self.canvas.unbind_all('<MouseWheel>')
        self.canvas.unbind_all('<Key-Up>')
        self.canvas.unbind_all('<Key-Down>')
        self.canvas.unbind_all('<Escape>')
        
        for historyOb in self.historyList:
            historyOb.entryPassword.unbind('<Control-c>')
            historyOb.buttonPassword.unbind('<1>')
    
    def copyToClipBoard(self, entry):
        if None != self.client:
            self.client.copyToClipBoard(entry)