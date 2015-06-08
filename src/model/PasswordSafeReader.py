'''
Created on May 28, 2015

@author: thomas
'''

import os
import xml.dom.minidom

class PasswordSafeReader(object):
    '''
    classdocs
    '''

    def __init__(self, option, gpg):
        '''
        Constructor
        '''
        self.option = option
        self.gpg = gpg
    
    # passPhrase should not be stored, so it is used as parameter
    def read(self, passwordSafe, passPhrase):
        for f in self.option.getFiles():
            filename = f.getFilename()
            if os.path.isfile(filename) and os.access(filename, os.R_OK):
                self.readFile(f, passwordSafe, passPhrase)
        # TODO: sorting is only needed once, so remove sorting in passwordSafe.loadPassObject 
        #passwordSafe.passsafesort()

    def readFile(self, passwordFile, passwordSafe, passPhrase):
        '''
        Load the xml-file
        Save the passwordobjects in RAM
        '''

        datei = open(passwordFile.getFilename(), "rb")
        decrypt_data = self.gpg.decrypt_file(datei, passphrase=str(passPhrase), always_trust=True)
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
                    title = self.readText(knotenName)
                for knotenName in elem1.getElementsByTagName('Username'):
                    username = self.readText(knotenName)
                for knotenName in elem1.getElementsByTagName('Password'):
                    password = self.readText(knotenName)
                for knotenName in elem1.getElementsByTagName('EMail'):
                    email = self.readText(knotenName)
                for knotenName in elem1.getElementsByTagName('URL'):
                    location = self.readText(knotenName)
                for knotenName in elem1.getElementsByTagName('Note'):
                    note = self.readText(knotenName)
                passOb = passwordSafe.loadPassObject(title, username, password, email, location, note)
                passOb.setPasswordFile(passwordFile) 

    def readText(self, node):
        '''
        Return the text of the nodeType
        '''
        retVal = ''
        for k in node.childNodes:
            if k.nodeType == k.TEXT_NODE:
                retVal = k.nodeValue.strip()
                break
        return retVal
    