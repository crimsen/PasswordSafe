'''
Created on 16.04.2015

@author: timgroger
'''

import gnupg
import os
import string
import sys
import xml.dom
from model.PasswordFileOption import PasswordFileOption

class OptionLoader(object):
    '''
    classdocs
    '''
    def __init__(self, filename, controller):
        self.maincontroller = controller
        self.gpg = gnupg.GPG()
        self.filename = filename       
        self.accounts = self.parsAccounts()
        self.accounts = self.cleanList(self.accounts) 
        

    def parsAccounts(self):
        secretKeys = self.gpg.list_keys(True)
        uids = []
        emails = []
        
        for keys in secretKeys:
            uids.append(keys['uids'])
        
        for account in uids:
            for email in account:
                if sys.hexversion < 0x3000000:
                    email = email.encode('utf-8')
                emailsplit = email.split(' ')
                emails.append(emailsplit[len(emailsplit)-1])
        return emails
    def cleanList(self, list):
        accounts = []
        for i in list:
            accounts.append(self.cleanString(i))
        return accounts
        
    def cleanString(self, string): 
        retVal = ''
        for i in string:
            if (i!='<') and (i!='>'):
                retVal+=i
        return retVal
    
    def loadOptions(self, filename, option):
        datei = open(filename, "r")
        dom = xml.dom.minidom.parse(datei)
        datei.close()

        option.files = []
        
        for elem in dom.getElementsByTagName('Options'):
            for elem1 in elem.getElementsByTagName('ActivateEmail'):
                option.email = self.liesText(elem1)
            for passwordFile in elem.getElementsByTagName('passwordfile'):
                filename = passwordFile.getAttribute('filename')
                encodeId = self.getList(passwordFile.getAttribute('encodeid'))
                encodeId.insert(0, option.getEmail())
                isDefault = self.getBoolean(passwordFile.getAttribute('isdefault'))
                needBackup = self.getBoolean(passwordFile.getAttribute('needbackup'))
                passwordFileOption = PasswordFileOption(filename, encodeId, isDefault=isDefault, needBackup=needBackup)
                option.files.append(passwordFileOption)
            self.readGuiOption(elem, option.gui)
        self.updateDefaultValues(option)
        self.controlEmailOld(option)
        
    def controlEmailOld(self, option):
        if option.emailOld == None:
            option.emailOld = option.email

    def readGuiOption(self, parent, gui):
        for element in parent.getElementsByTagName('gui'):
            gui.autolock = self.getIntAttribute(element, 'autolock', gui.autolock)

    def updateDefaultValues(self, option):
        '''
        sets default values that are not saved in the optionfile,
        but that are used implicitly
        '''
        # delete all files that are default, because we are updating
        option.files = [x for x in option.files if not x.isDefault]
                
        home = os.environ['HOME']
        filename = home+'/Documents/.PasswordSafe/' + option.getEmail() + '/safe.xml'
        passwordFileOption = PasswordFileOption(filename, [option.getEmail()], isDefault=True, needBackup=True)
        option.files.insert(0, passwordFileOption)

    
    def liesText(self, knoten):
        '''
        Return the text of the nodeType
        '''
        for k in knoten.childNodes:
            if k.nodeType == k.TEXT_NODE:
                return k.nodeValue.strip()
     
    
    def getaccounts(self):
        print(self.accounts)
        return self.accounts

    def getBoolean(self, boolstring):
        return boolstring in ['true']

    def getBoolAttribute(self, element, attributeName, defaultValue):
        retVal = defaultValue
        attributeNode = element.getAttributeNode(attributeName)
        if None != attributeNode:
            retVal = self.getBoolean(attributeNode.value)
        return retVal
    
    def getIntAttribute(self, element, attributeName, defaultValue):
        retVal = defaultValue
        attributeNode = element.getAttributeNode(attributeName)
        if None != attributeNode:
            retVal = int(attributeNode.value)
        return retVal
    
    def getList(self, liststring):
        return liststring.split()
