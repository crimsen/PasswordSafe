# coding=utf-8
'''
Created on 21.07.2015

@author: timgroger
'''

class PasswordSymbols(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.lowLetter = [u'a', u'b' , u'c', u'd', u'e', u'f', u'g', u'h', u'i', u'j', u'k', u'l', u'm', u'n', u'o', u'p', u'q', u'r', u's', u't', u'u', u'v', u'w', u'x', u'y', u'z']
        self.upLetter = [u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'I', u'J', u'K', u'L', u'M', u'N', u'O', u'P', u'Q', u'R', u'S', u'T', u'U', u'V', u'W', u'X', u'Y', u'Z']
        self.specialLowLetter_DE = [u'ä', u'ö', u'ü', u'ß']
        self.specialUpLetter_DE = [u'Ä', u'Ö', u'Ü']
        self.specialSymbols = [u'_', u'[', u']', u'^', u'!', u'<', u'>', u'=', u'&', u'\\', u'/', u'{', u'}', u'*', u'?', u'(', u')', u'-', u':', u'@', u'#', u'$', u'|', u'~', u'+', u'%']
        self.numbers = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9']
        
    def getLowLetter(self):
        return self.lowLetter
    
    def getUpLetter(self):
        return self.upLetter
    
    def getSpecialLowLetter_DE(self):
        return self.specialLowLetter_DE
    
    def getSpecialUpLetter_DE(self):
        return self.specialUpLetter_DE
    
    def getSpecialSymbols(self):
        return self.specialSymbols
    
    def getNumbers(self):
        return self.numbers
        