'''
Created on 14.06.2015

@author: timgroger
'''
import Tkinter as Tk
from gui.HistoryFrame import HistoryFrame
# from model.HistoryPasswordObject import HistoryPasswordObject as hp
# from datetime import date

class ViewHistory(object):
    '''
    classdocs
    '''


    def __init__(self, mainController, mainWindow, history):
        '''
        Constructor
        '''
        self.viewHistory = Tk.Toplevel()
        self.viewHistory.title('PasswordHistory')
        self.viewHistory.geometry('400x400')
        
        self.mainWindow = mainWindow
        self.mainController = mainController
        self.history = history
        
        self.__buildFrame(self.viewHistory)
        self.buildData(self.history)
        
        self.viewHistory.geometry('660x400')
        
    def show(self):
        self.viewHistory.mainloop()
        
    def __buildFrame(self, parent):
        self.mainFrame = Tk.Frame(master=parent)
        self.mainFrame.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        
        self.canvas = Tk.Canvas(master=self.mainFrame)
        self.window = Tk.Frame(master=self.canvas)
        self.scrollbar = Tk.Scrollbar(master = self.mainFrame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both',expand=True)
        self.canvas.create_window((0,0), window=self.window, anchor='nw')
        self.window.bind('<Configure>', self.configureCanvas)
        
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind_all('<Key-Up>', self.up)
        self.canvas.bind_all('<Key-Down>', self.down)
        self.canvas.bind_all('<Escape>', self.destroy)
        
    def destroy(self, event):
        self.viewHistory.destroy()
        
    def up(self, event):
        self.canvas.yview_scroll(-1, 'units')
    def down(self, event):
        self.canvas.yview_scroll(1, 'units')
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*event.delta, 'units')
        print event.delta
        
    def configureCanvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def buildData(self, history):
        for passOb in history:
            HistoryFrame(self.window,self.mainController, passOb).pack(side='top', fill='both', padx=5, pady=5, expand=True)
           
        
# if __name__ == '__main__':
#     
#     history = []
#     for b in range(10):
#         i = str(b)
#         a = hp('title'+i, 'username'+i, 'password1'+i, 'email1'+i, 'location1'+i, 'note1'+i, date.today(), date.today())
#         history.append(a)
#     test = ViewHistory('test', 'test', history)
#     test.show()