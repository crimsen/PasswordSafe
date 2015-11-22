'''
Created on 21.07.2015

@author: timgroger
'''
import Tkinter as Tk
from Tkinter import StringVar
from controller.PasswordGen import PasswordGen

class PassGenWindow(object):
    '''
    classdocs
    '''

    def __init__(self, mainController, mainWindow):
        '''
        Constructor
        '''
        
        self.mainController = mainController
        self.mainWindow = mainWindow
        self.passGen = PasswordGen()
        self.root = Tk.Toplevel()
        self.root.title('Password Generator')
        
        self.checkLowerCase = StringVar()
        self.checkUpperCase = StringVar()
        self.checkLowerSpecialCaseDE = StringVar()
        self.checkUpperSpecialCaseDE = StringVar()
        self.checkSpecialSign = StringVar()
        self.checkNumbers = StringVar()
        
        self.__buildFrame__(self.root)
        
    def __buildFrame__(self, parent):
        
        self.mainFrame = Tk.Frame(master=parent)
        self.entryGenPass = Tk.Entry(master=self.mainFrame)
        self.__buildAttributFrame__(self.mainFrame)
        
        self.buttonGen = Tk.Button(master=self.mainFrame, command=self.pressGen, text='generate Password')
        
        self.frameLength = Tk.Frame(master=self.mainFrame)
        
        self.entryLength = Tk.Entry(master=self.frameLength)
        self.labelLength = Tk.Label(master=self.frameLength, text='Length:')
        
        self.labelLength.pack(side='left')
        self.entryLength.pack(side='left')
        
        self.mainFrame.pack(side='top', expand=True)
        self.attributFrame.pack(side='top', expand=True)
        self.frameLength.pack(side='top', expand=True)
        self.entryGenPass.pack(side='top', expand=True)
        self.buttonGen.pack(side='top', anchor='e')
        
    def __buildAttributFrame__(self,parent):
        self.attributFrame = Tk.Frame(master=parent)
        self.lowerCaseButton = Tk.Checkbutton(master=self.attributFrame, variable=self.checkLowerCase, onvalue='lowerCase', offvalue='', text='Lower case')
        self.upperCaseButton = Tk.Checkbutton(master=self.attributFrame, variable=self.checkUpperCase, onvalue='upperCase', offvalue='', text='Upper case')
        self.lowerSpecialCaseButtonDE = Tk.Checkbutton(master=self.attributFrame, variable=self.checkLowerSpecialCaseDE, onvalue='specialLowerCase_DE', offvalue='', text='German special sign (lower case)')
        self.upperSpecialCaseButtonDE = Tk.Checkbutton(master=self.attributFrame, variable=self.checkUpperSpecialCaseDE, onvalue='specialUpperCase_DE', offvalue='', text='German special sign (upper case)')
        self.specialSignButton =  Tk.Checkbutton(master=self.attributFrame, variable=self.checkSpecialSign, onvalue='specialSymbols', offvalue='', text='Special sign')
        self.numbersButton = Tk.Checkbutton(master=self.attributFrame, variable=self.checkNumbers, onvalue='numbers', offvalue='', text='Numbers')
        
        self.lowerCaseButton.grid(row=0, column=0, sticky='w')
        self.upperCaseButton.grid(row=1, column=0, sticky='w')
        self.lowerSpecialCaseButtonDE.grid(row=0, column=1, sticky='w')
        self.upperSpecialCaseButtonDE.grid(row=1, column=1, sticky='w')
        self.specialSignButton.grid(row=0, column=2, sticky='w')
        self.numbersButton.grid(row=1, column=2, sticky='w')
        
    def pressGen(self):
        
        attributs = [self.checkLowerCase.get(), self.checkUpperCase.get(), self.checkLowerSpecialCaseDE.get(), self.checkUpperSpecialCaseDE.get(), self.checkSpecialSign.get(), self.checkNumbers.get()]
        length = int(self.entryLength.get())
        self.passGen.setUsedSymbols(attributs)
        self.passGen.genPassword(length)
        password = self.passGen.getGeneratedPass()
        self.entryGenPass.delete(0, 'end')
        self.entryGenPass.insert('end', password)
        
if __name__=='__main__':
    passWindow = PassGenWindow(None, None)
    passWindow.root.mainloop()
         