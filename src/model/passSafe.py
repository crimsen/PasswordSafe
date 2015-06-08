'''
Created on 28.03.2015

@author: crimsen
'''
import xml.dom.minidom
import StringIO as StringStream
import gnupg
import os
from datetime import datetime
import shutil
from model.passObject import PasswordObject



class PasswordSafe(object):
    
    def __init__(self, filename, account, controller):
        self.passwordSafe = []
        self.filename = filename
        self.account = account
        self.maincontroller = controller
        self.gpg = gnupg.GPG()
                 
    def newPassObject(self, title='', username='', password='', email='', location='', note=''):
        '''
        Create a new passwordobject
        And save it in RAM
        '''
        passOb = PasswordObject(title, username, password, email, location, note)
        self.passwordSafe.append(passOb)
        self.passsafesort()
        
        self.write(self.filename, self.account)
        self.backupsafe()
        
    def loadPassObject(self, title, username, password, email, location, note):
        '''
        Load a Passobject from XML file
        '''
        
        passOb = PasswordObject(title, username, password, email, location, note)
        self.passwordSafe.append(passOb)
        self.passsafesort()
        
    
    def load(self, passphrase):
        '''
        Load the xml-file
        Save the passwordobjects in RAM
        '''
        

        datei = open(self.filename, "rb")
        decrypt_data = self.gpg.decrypt_file(datei, passphrase=str(passphrase),always_trust=True)
        decrypt = decrypt_data.data
        dom = xml.dom.minidom.parseString(decrypt)
        datei.close()
    
        for elem in dom.getElementsByTagName('Safes'):
            for elem1 in elem.getElementsByTagName('Safe'):
                # set default values to prevent None-types
                title = ''
                username = ''
                password = ''
                email = ''
                location = ''
                note = ''
                for knotenName in elem1.getElementsByTagName('Title'):
                    title = self.liesText(knotenName)
                for knotenName in elem1.getElementsByTagName('Username'):
                    username = self.liesText(knotenName)
                for knotenName in elem1.getElementsByTagName('Password'):
                    password = self.liesText(knotenName)
                for knotenName in elem1.getElementsByTagName('EMail'):
                    email = self.liesText(knotenName)
                for knotenName in elem1.getElementsByTagName('URL'):
                    location = self.liesText(knotenName)
                for knotenName in elem1.getElementsByTagName('Note'):
                    note = self.liesText(knotenName)
                self.loadPassObject(title, username, password, email, location, note) 
        
        
               
    def write(self, filename, account):
        '''
        Write the xml-file
        '''
        
        implement = xml.dom.getDOMImplementation()
        doc = implement.createDocument(None, 'Safes', None)
        
        for i in self.passwordSafe:
            
            safeElem = doc.createElement('Safe')
        
            titleElem = doc.createElement('Title')
            safeElem.appendChild(titleElem)
            titleTextElem = doc.createTextNode(i.getTitle())
            titleElem.appendChild(titleTextElem)
        
            usernameElem = doc.createElement('Username')
            safeElem.appendChild(usernameElem)
            usernameTextElem = doc.createTextNode(i.getUsername())
            usernameElem.appendChild(usernameTextElem)
        
            passwordElem = doc.createElement('Password')
            safeElem.appendChild(passwordElem)
            passwordTextElem = doc.createTextNode(i.getPassword())
            passwordElem.appendChild(passwordTextElem)
        
            emailElem = doc.createElement('EMail')
            safeElem.appendChild(emailElem)
            emailTextElem = doc.createTextNode(i.getEmail())
            emailElem.appendChild(emailTextElem)
        
            locationElem = doc.createElement('URL')
            safeElem.appendChild(locationElem)
            locationTextElem = doc.createTextNode(i.getLocation())
            locationElem.appendChild(locationTextElem)
        
            noteElem = doc.createElement('Note')
            safeElem.appendChild(noteElem)
            noteTextElem = doc.createTextNode(i.getNote())
            noteElem.appendChild(noteTextElem)
        
            doc.documentElement.appendChild(safeElem)
        
        
        datei = open(filename, 'w')
        noneencrypt = StringStream.StringIO()
        doc.writexml(noneencrypt, '\n', ' ')
        s = noneencrypt.getvalue()
        encrypt = self.gpg.encrypt(s, str(account), always_trust=True)
        datei.write(str(encrypt))
        datei.close()
        
        self.passsafesort()
        
    def changePassOb(self, index, title='', username='', password='', email='', location='', note=''):
        '''
        Change the attributes of the passwordobject
        And write it in a file
        '''
        
        passOb=self.passwordSafe[index]
        passOb.setTitle(title)
        passOb.setUsername(username)
        passOb.setPassword(password)
        passOb.setEmail(email)
        passOb.setLocation(location)
        passOb.setNote(note)
           
        self.write(self.filename, self.account)
                                   
    def removePassOb(self, index):
        '''
        Delete a passwordobject
        And write it in a file
        '''
        self.passwordSafe.remove(self.passwordSafe[index])
        
        self.write(self.filename, self.account)
                    
    def liesText(self, knoten):
        '''
        Return the text of the nodeType
        '''
        retVal = ''
        for k in knoten.childNodes:
            if k.nodeType == k.TEXT_NODE:
                retVal = k.nodeValue.strip()
                break
        return retVal
    
    def passsafesort(self):
        self.passwordSafe = self.sortfunc(self.passwordSafe)
     
    def sortfunc(self, array):
        less = []
        equal = []
        greater = []
    
        if len(array) > 1:
            pivot = array[0].getTitle().lower()
            for x in array:
                if x.getTitle().lower() < pivot:
                    less.append(x)
                if x.getTitle().lower() == pivot:
                    equal.append(x)
                if x.getTitle().lower() > pivot:
                    greater.append(x)
            return self.sortfunc(less)+equal+self.sortfunc(greater)
        else:  
            return array 
    
    def backupsafe(self):
        
        home = os.environ['HOME']
        today = datetime.today()
        
        self.backup = home+'/Documents/.PasswordSafe/'+self.account+'/backup/'
        if not os.path.exists(self.backup):
            os.makedirs(self.backup)
        print self.backup
        
        shutil.copy(self.filename, self.backup+str(today.year)+'-'+str(today.month)+'-'+str(today.day)+'-safe.xml')
        print ('backup completed')
     
    def printFu(self, list):
        for x in list:
            print(x.getTitle())
            
    def getSafe(self):
        return self.passwordSafe
    
    def getTitle(self, index):
        return self.passwordSafe[index].getTitle()
    
    def getUsername(self, index):
        return self.passwordSafe[index].getUsername()
    
    def getPassword(self, index):
        return self.passwordSafe[index].getPassword()
    
    def getEmail(self, index):
        return self.passwordSafe[index].getEmail()
    
    def getLocation(self, index):
        return self.passwordSafe[index].getLocation()
    
    def getNote(self, index):
        return self.passwordSafe[index].getNote()
    
    def getSafeIndex(self, index):
        return self.passwordSafe[index]
    
    def close(self):
        del self.passwordSafe
                
    
    