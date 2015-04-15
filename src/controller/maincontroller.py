'''
Created on 15.04.2015

@author: crimsen
'''
from gui.mainWindow import MainWindow
import os


class MainController(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__searchFiles__()
        self.__initGUI__()
        
        
    def __searchFiles__(self):
        '''
        Search Safe and Option-File
        If not exist create path
        '''
        home = os.environ['HOME']
        
        self.safefile = home+'/Documents/.PasswordSafe/safe.xml'
        self.optionfile = home+'/Documents/.PasswordSafe/option.xml'
        
        self.dirfile = os.path.dirname(self.safefile)
        if not os.path.exists(self.dirfile):
            os.makedirs(self.dirfile)
        print(str(self.dirfile))  
       
    
    def __initGUI__(self):
        
        self.mainWindow = MainWindow()
        
    def show(self):
        
        self.mainWindow.show()
if __name__=='__main__':
    App= MainController()
    App.show()