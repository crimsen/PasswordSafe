'''
Created on 21.07.2015

@author: timgroger
'''

from random import randint

class PasswordGen(object):
    '''
    classdocs
    '''

    def __init__(self, model):
        
        self.passwordSymbols = model
        self.generatedPass = ''
        self.usedSymbols = []
        
    def setUsedSymbols(self, entrys):
        
        self.usedSymbols = []
        
        for entry in entrys:
            if entry == 'lowerCase':
                self.usedSymbols += self.appendSymbol(self.passwordSymbols.getLowLetter())
            if entry == 'upperCase':
                self.usedSymbols += self.appendSymbol(self.passwordSymbols.getUpLetter())
            if entry == 'specialUpperCase_DE':
                self.usedSymbols += self.appendSymbol(self.passwordSymbols.getSpecialUpLetter_DE())
            if entry == 'specialLowerCase_DE':
                self.usedSymbols += self.appendSymbol(self.passwordSymbols.getSpecialLowLetter_DE())
            if entry == 'specialSymbols':
                self.usedSymbols += self.appendSymbol(self.passwordSymbols.getSpecialSymbols())
            if entry == 'numbers':
                self.usedSymbols += self.appendSymbol(self.passwordSymbols.getNumbers())
    
    def appendSymbol(self, list):
        retVal = []
        for symbol in list:
            retVal.append(symbol)
        return retVal
    
    def genPassword(self, length):
        self.generatedPass = ''
        for i in range(length):
            rand = randint(0, len(self.usedSymbols)-1)
            self.generatedPass += self.usedSymbols[rand]
    
    def getGeneratedPass(self):
        return self.generatedPass
    
if __name__ == '__main__':
    passGen = PasswordGen()
    a = 'lowerCase'
    b = 'upperCase'
    c = 'specialUpperCase_DE'
    d = 'specialLowerCase_DE'
    e = 'specialSymbols'
    
    test = [a, b]
    
    passGen.setUsedSymbols(test)
    passGen.genPassword(8)
    
    print(passGen.getGeneratedPass())     
        