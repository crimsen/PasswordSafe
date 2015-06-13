'''
Created on May 29, 2015

@author: thomas
'''

import os
from datetime import datetime
import shutil
import StringIO as StringStream
import xml.dom.minidom

class PasswordSafeWriter(object):
    '''
    classdocs
    '''


    def __init__(self, option, gpg):
        '''
        Constructor
        '''
        self.option = option
        self.gpg = gpg
    
    def write(self, passwordSafe):
        for passwordFile in self.option.getFiles():
            if passwordFile.isChanged:
                filename = passwordFile.getFilename()
                if passwordFile.needBackup:
                    if os.path.isfile(filename):
                        self.doBackup(filename)
                self.assureDirectory(passwordFile.getFilename())
                self.writeFile(passwordFile, passwordSafe)
                passwordFile.resetChanged()

    def writeFile(self, passwordFile, passwordSafe):
        implement = xml.dom.getDOMImplementation()
        doc = implement.createDocument(None, 'Safes', None)
        
        for i in passwordSafe.getSafe():
            
            if ((i.getPasswordFile() == passwordFile) or 
                ((i.getPasswordFile() == None) and passwordFile.isDefault)) :
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
                
                historyElem = doc.createElement('History')
                safeElem.appendChild(historyElem)
                for passOb in i.getHistory():
                    safeElemOld = doc.createElement('SafeOld')
                    historyElem.appendChild(safeElemOld)
                    
                    titleElem = doc.createElement('TitleOld')
                    safeElemOld.appendChild(titleElem)
                    titleTextElem = doc.createTextNode(passOb.getTitle())
                    titleElem.appendChild(titleTextElem)
                
                    usernameElem = doc.createElement('UsernameOld')
                    safeElemOld.appendChild(usernameElem)
                    usernameTextElem = doc.createTextNode(passOb.getUsername())
                    usernameElem.appendChild(usernameTextElem)
                
                    passwordElem = doc.createElement('PasswordOld')
                    safeElemOld.appendChild(passwordElem)
                    passwordTextElem = doc.createTextNode(passOb.getPassword())
                    passwordElem.appendChild(passwordTextElem)
                
                    emailElem = doc.createElement('EMailOld')
                    safeElemOld.appendChild(emailElem)
                    emailTextElem = doc.createTextNode(passOb.getEmail())
                    emailElem.appendChild(emailTextElem)
                
                    locationElem = doc.createElement('URLOld')
                    safeElemOld.appendChild(locationElem)
                    locationTextElem = doc.createTextNode(passOb.getLocation())
                    locationElem.appendChild(locationTextElem)
                
                    noteElem = doc.createElement('NoteOld')
                    safeElemOld.appendChild(noteElem)
                    noteTextElem = doc.createTextNode(passOb.getNote())
                    noteElem.appendChild(noteTextElem)
            
                doc.documentElement.appendChild(safeElem)
        
        datei = open(passwordFile.getFilename(), 'w')
        noneencrypt = StringStream.StringIO()
        doc.writexml(noneencrypt, '\n', ' ')
        s = noneencrypt.getvalue()
        encodeIds = [str(i) for i in passwordFile.getEncodeId()]
        encrypt = self.gpg.encrypt(s, encodeIds, always_trust=True)
        datei.write(str(encrypt))
        datei.close()

    def doBackup(self, filename):
        (directory, filepart) = os.path.split(filename)
        today = datetime.today()
        filepart = str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + filepart
        backupFilename = os.path.join(directory, 'backup', filepart)
        self.assureDirectory(backupFilename)
        print backupFilename
        
        shutil.copy(filename, backupFilename)
        print ('backup completed')

    def assureDirectory(self, filename):
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
