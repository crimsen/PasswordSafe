'''
Created on 21.07.2015

@author: timgroger
'''
import Tkinter as Tk
from Tkinter import StringVar, IntVar
from controller.PasswordGen import PasswordGen
from model.PasswordSymbols import PasswordSymbols

class PassGenWindow(object):
    def __init__(self, client):
        self.view = PassGenWindowView()
        self.model = PasswordSymbols()
        self.passGen = PasswordGen(self.model)
        self.controller = PassGenWindowController(self.view, self.model, client, self.passGen)
    
    def show(self):
        self.view.show()
    
    def close(self):
        self.view.close()
        
class PassGenWindowView(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.window = Tk.Toplevel()
        self.window.title('Password Generator')
        
        self.checkLowerCase = StringVar()
        self.checkUpperCase = StringVar()
        self.checkLowerSpecialCaseDE = StringVar()
        self.checkUpperSpecialCaseDE = StringVar()
        self.checkSpecialSign = StringVar()
        self.checkNumbers = StringVar()
        
        self.frameLengthAdvanced = None
        self.frameLengthEasy = None
        
        self.__buildFrame__(self.window)
        
    def __buildFrame__(self, parent):
        
        self.mainFrame = Tk.Frame(master=parent)
        self.frameGenPass = Tk.Frame(master=self.mainFrame)
        
        self.entryGenPass = Tk.Entry(master=self.frameGenPass)
        self.buttonCopy = Tk.Button(master=self.frameGenPass, text='Copy')
        self.labelGenPass = Tk.Label(master=self.frameGenPass, text='Password: ')
        
        self.__buildAttributFrame__(self.mainFrame)
        
        self.buttonGen = Tk.Button(master=self.mainFrame, text='generate Password')
        
        
        
        self.mainFrame.pack(side='top', expand=True)
        self.attributFrame.pack(side='top', padx=5, pady=5, expand=True)
        self.__buildLengthFrame__(self.mainFrame)
        self.frameGenPass.pack(side='top', padx=5, pady=5, expand=True)
        self.labelGenPass.pack(side='left', expand=True)
        self.entryGenPass.pack(side='left', expand=True)
        self.buttonCopy.pack(side='left', expand=True)
        self.buttonGen.pack(side='top', padx=5, pady=5, anchor='e')
        
    def __buildLengthFrame__(self, parent):
        self.frameLength = Tk.Frame(master=parent)
        self.checkLength = Tk.Checkbutton(master=self.frameLength, text='Advanced', onvalue=1, offvalue=0)
        self.labelLength = Tk.Label(master=self.frameLength, text='Length:')
        self.labelLength.pack(side='left')
        self.checkLength.pack(side='left')
        self.frameLength.pack(side='top', padx=5, pady=5, anchor='w', expand=True)
        self.__buildLengthFrameEasy__()
    
    def __buildLengthFrameEasy__(self):            
        self.frameLengthEasy = Tk.Frame(master=self.frameLength)
        self.scaleLength = Tk.Scale(master=self.frameLengthEasy, orient='horizontal', length=100, sliderlength=30, from_=1, to=30)
        self.frameLengthEasy.pack(side='left')
        self.scaleLength.pack(side='left')
    
    def __buildLengthFrameAdvanced__(self):    
        self.frameLengthAdvanced = Tk.Frame(master=self.frameLength)
        self.entryLength = Tk.Entry(master=self.frameLengthAdvanced, justify='right', width=10)
        self.frameLengthAdvanced.pack(side='left')
        self.entryLength.pack(side='left')
        

        
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
        
    def show(self):
        self.window.mainloop()
        
    def close(self):
        self.window.destroy()
        
class PassGenWindowController(object):
    
    def __init__(self, view, model, client, passGen):
        self.defaultLength = 8
        
        self.view = view
        self.model = model
        self.client = client
        self.passGen = passGen
        self.view.buttonGen.configure(command=self.pressGen)
        self.view.buttonCopy.config(command=self.copyToClipBoard)
        self.checkLowerCase = self.view.checkLowerCase
        self.checkUpperCase = self.view.checkUpperCase
        self.checkLowerSpecialCaseDE = self.view.checkLowerSpecialCaseDE
        self.checkUpperSpecialCaseDE = self.view.checkUpperSpecialCaseDE
        self.checkSpecialSign = self.view.checkSpecialSign
        self.checkNumbers = self.view.checkNumbers
        self.entryGenPass = self.view.entryGenPass
        
        self.checkLength = self.view.checkLength
        
        self.varCheckLength = IntVar()
        self.varLength = IntVar()
        self.view.scaleLength.config(variable=self.varLength)
        self.varLength.set(self.defaultLength)
        self.entryLength = self.varLength
        
        self.checkLength.config(variable=self.varCheckLength)
        self.varCheckLength.trace('w', self.controlCheckLength)
        
        self.checkLowerCase.trace('w', self.resetTime)
        self.checkUpperCase.trace('w', self.resetTime)
        self.checkLowerSpecialCaseDE.trace('w', self.resetTime)
        self.checkUpperSpecialCaseDE.trace('w', self.resetTime)
        self.checkSpecialSign.trace('w', self.resetTime)
        self.checkNumbers.trace('w', self.resetTime)
#        self.entryGenPass.trace('w', self.resetTime)
#        self.entryLength.trace('w', self.resetTime)
    
        
    def pressGen(self):
        self.resetTime()
        attributs = [self.checkLowerCase.get(), self.checkUpperCase.get(), self.checkLowerSpecialCaseDE.get(), self.checkUpperSpecialCaseDE.get(), self.checkSpecialSign.get(), self.checkNumbers.get()]
        length = int(self.entryLength.get())
        self.passGen.setUsedSymbols(attributs)
        self.passGen.genPassword(length)
        password = self.passGen.getGeneratedPass()
        self.entryGenPass.delete(0, 'end')
        self.entryGenPass.insert('end', password)
        
    def copyToClipBoard(self):
        genPass = self.entryGenPass.get()
        if None != self.client:
            self.client.copyToClipBoard(genPass) 
            
    def controlCheckLength(self, *args):
        
        if 0 != self.varCheckLength.get():
            self.showAdvanced()
        else:
            self.showEasy()
            
            
    def hideAdvanced(self):
        if None != self.view.frameLengthAdvanced:
            self.view.frameLengthAdvanced.destroy()
            self.view.frameLengthAdvanced = None
        
    def hideEasy(self):
        if None != self.view.frameLengthEasy:
            self.view.frameLengthEasy.destroy()
            self.view.frameLengthEasy = None
        
    def showAdvanced(self):
        self.hideEasy()
        if None == self.view.frameLengthAdvanced:
            self.view.__buildLengthFrameAdvanced__()
            self.entryLength = self.view.entryLength
            self.entryLength.delete(0, 'end')
            self.entryLength.insert('end', self.defaultLength)
        
    def showEasy(self):
        self.hideAdvanced()
        if None == self.view.frameLengthEasy:
            self.view.__buildLengthFrameEasy__()
            self.view.scaleLength.config(variable = self.varLength)
            self.varLength.set(self.defaultLength)
            self.entryLength = self.varLength
    
    def resetTime(self, *args):
        self.client.resetTime()
    
    def close(self):
        self.view.close()
        
if __name__=='__main__':
    passWindow = PassGenWindow(None)
    passWindow.show()
         