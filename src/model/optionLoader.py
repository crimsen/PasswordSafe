'''
Created on 16.04.2015

@author: timgroger
'''

import gnupg
import xml.dom

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
                emailsplit = email.encode('utf-8').split(' ')
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
    
    def loadOptions(self, filename):
        datei = open(filename, "r")
        dom = xml.dom.minidom.parse(datei)
        datei.close()
        
        for elem in dom.getElementsByTagName('Options'):
            for elem1 in elem.getElementsByTagName('ActivateEmail'):
                self.email = self.liesText(elem1)
     
    
    def liesText(self, knoten):
        '''
        Return the text of the nodeType
        '''
        for k in knoten.childNodes:
            if k.nodeType == k.TEXT_NODE:
                return k.nodeValue.strip()
     
    
    def writeEmailOption(self, email, filename):
        
        implement = xml.dom.getDOMImplementation()
        doc = implement.createDocument(None, 'Options', None)
        
        emailElem = doc.createElement('ActivateEmail')
        emailTextElem = doc.createTextNode(str(email))
        emailElem.appendChild(emailTextElem)
        
        doc.documentElement.appendChild(emailElem)
        
        datei = open(filename, 'w')
        doc.writexml(datei, '\n', ' ')
        datei.close()
        
    def getaccounts(self):
        print self.accounts
        return self.accounts
    
    def getemail(self):
        self.loadOptions(self.filename)
        print str(self.email)
        return self.email