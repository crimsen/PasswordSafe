'''
Created on 28.03.2015

@author: crimsen
'''
import xml.dom.minidom
import StringIO as StringStream
import gnupg
from model.passObject import PasswordObject



class PasswordSafe(object):
    
    def __init__(self, filename, account):
        self.passwordSafe = []
        self.filename = filename
        self.account = account
        self.gpg = gnupg.GPG(use_agent=False)
        self.load(self.filename)
        self.passwordSafe = self.sort(self.passwordSafe)
                 
    def newPassObject(self, title='', username='', password='', email='', location='', note=''):
        '''
        Create a new passwordobject
        And save it in RAM
        '''
        passOb = PasswordObject(str(title), str(username), str(password), str(email), str(location), str(note))
        self.passwordSafe.append(passOb)
        
        self.write(self.filename, self.account)
        
    def loadPassObject(self, title, username, password, email, location, note):
        '''
        Load a Passobject from XML file
        '''
        
        passOb = PasswordObject(str(title), str(username), str(password), str(email), str(location), str(note))
        self.passwordSafe.append(passOb)
        
    
    def load(self, filename):
        '''
        Load the xml-file
        Save the passwordobjects in RAM
        '''
        
        try:
            datei = open(filename, "rb")
            decrypt_data = self.gpg.decrypt_file(datei, always_trust=False)
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
            return True
        
               
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
        encrypt = self.gpg.encrypt(s, str(account))
        datei.write(str(encrypt))
        datei.close()
        
        self.passwordSafe = self.sort(self.passwordSafe)
        
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
     
    def sort(self, array):
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
            # Don't forget to return something!
            return self.sort(less)+equal+self.sort(greater)  # Just use the + operator to join lists
        # Note that you want equal ^^^^^ not pivot
        else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
            return array 
     
    def printFu(self, list):
        for x in list:
            print(x.getTitle())
            
    def getSafe(self):
        return self.passwordSafe
    
    def getSafeIndex(self, index):
        return self.passwordSafe[index]
    
    def close(self):
        del self.passwordSafe
                
    
    