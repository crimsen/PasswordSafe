'''
Created on 28.03.2015

@author: crimsen
'''
import xml.dom.minidom
import StringIO as StringStream
import gnupg
from model.passObject import PasswordObject



class PasswordSafe(object):
    
    def __init__(self, filename, account, controller):
        self.passwordSafe = []
        self.filename = filename
        self.account = account
        self.maincontroller = controller
        self.gpg = gnupg.GPG(use_agent=True)
        self.load(self.filename)
        self.passsafesort()
                 
    def newPassObject(self, title='', username='', password='', email='', location='', note=''):
        '''
        Create a new passwordobject
        And save it in RAM
        '''
        passOb = PasswordObject(str(title), str(username), str(password), str(email), str(location), str(note))
        self.passwordSafe.append(passOb)
        self.passsafesort()
        
        self.write(self.filename, self.account)
        
    def loadPassObject(self, title, username, password, email, location, note):
        '''
        Load a Passobject from XML file
        '''
        
        passOb = PasswordObject(str(title), str(username), str(password), str(email), str(location), str(note))
        self.passwordSafe.append(passOb)
        self.passsafesort()
        
    
    def load(self, filename):
        '''
        Load the xml-file
        Save the passwordobjects in RAM
        '''
        
        try:
            datei = open(filename, "rb")
            decrypt_data = self.gpg.decrypt_file(datei, always_trust=True)
            decrypt = str(decrypt_data)
            dom = xml.dom.minidom.parseString(decrypt)
            datei.close()
        
            for elem in dom.getElementsByTagName('Safes'):
                for elem1 in elem.getElementsByTagName('Safe'):
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
        except:
            print('fail to load safe.xml')
        
               
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
            titleTextElem = doc.createTextNode(str(i.getTitle()))
            titleElem.appendChild(titleTextElem)
        
            usernameElem = doc.createElement('Username')
            safeElem.appendChild(usernameElem)
            usernameTextElem = doc.createTextNode(str(i.getUsername()))
            usernameElem.appendChild(usernameTextElem)
        
            passwordElem = doc.createElement('Password')
            safeElem.appendChild(passwordElem)
            passwordTextElem = doc.createTextNode(str(i.getPassword()))
            passwordElem.appendChild(passwordTextElem)
        
            emailElem = doc.createElement('EMail')
            safeElem.appendChild(emailElem)
            emailTextElem = doc.createTextNode(str(i.getEmail()))
            emailElem.appendChild(emailTextElem)
        
            locationElem = doc.createElement('URL')
            safeElem.appendChild(locationElem)
            locationTextElem = doc.createTextNode(str(i.getLocation()))
            locationElem.appendChild(locationTextElem)
        
            noteElem = doc.createElement('Note')
            safeElem.appendChild(noteElem)
            noteTextElem = doc.createTextNode(str(i.getNote()))
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
        for k in knoten.childNodes:
            if k.nodeType == k.TEXT_NODE:
                return k.nodeValue.strip()
    
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
                
    
    