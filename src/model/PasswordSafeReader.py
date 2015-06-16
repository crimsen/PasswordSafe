'''
Created on May 28, 2015

@author: thomas
'''

import os
import xml.dom.minidom
import datetime

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
        passwordSafe.passsafesort()

    def readFile(self, passwordFile, passwordSafe, passPhrase):
        '''
        Load the xml-file
        Save the passwordobjects in RAM
        '''
        dom = self.decryptFile(passwordFile.getFilename(), passPhrase)
        if None == dom:
            print "decryption of %s failed" % passwordFile.getFilename()
            if passwordFile.isDefault:
                raise Exception("decryption not possible")
        else:
            for elem in dom.getElementsByTagName('Safes'):
                for elem1 in elem.getElementsByTagName('Safe'):
                    # set default values to prevent None-types
                    title = ''
                    username = ''
                    password = ''
                    email = ''
                    location = ''
                    note = ''
                    createDate = None
                    history = []
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
                    for knotenName in elem1.getElementsByTagName('CreateDate'):
                        createDate = self.decodeDate(self.readText(knotenName)) 
                    for historySafe in elem1.getElementsByTagName('History'):
                        for elem2 in historySafe.getElementsByTagName('SafeOld'):
                            # set default values to prevent None-types
                            titleOld = ''
                            usernameOld = ''
                            passwordOld = ''
                            emailOld = ''
                            locationOld = ''
                            noteOld = ''
                            createDateOld = None
                            endDate = None
                            for knotenName in elem2.getElementsByTagName('TitleOld'):
                                titleOld = self.readText(knotenName)
                            for knotenName in elem2.getElementsByTagName('UsernameOld'):
                                usernameOld = self.readText(knotenName)
                            for knotenName in elem2.getElementsByTagName('PasswordOld'):
                                passwordOld = self.readText(knotenName)
                            for knotenName in elem2.getElementsByTagName('EMailOld'):
                                emailOld = self.readText(knotenName)
                            for knotenName in elem2.getElementsByTagName('URLOld'):
                                locationOld = self.readText(knotenName)
                            for knotenName in elem2.getElementsByTagName('NoteOld'):
                                noteOld = self.readText(knotenName)
                            for knotenName in elem2.getElementsByTagName('CreateDateOld'):
                                createDateOld = self.decodeDate(self.readText(knotenName))
                            for knotenName in elem2.getElementsByTagName('EndDate'):
                                endDate = self.decodeDate(self.readText(knotenName))
                                
                            passObOld = passwordSafe.loadHistoryPassObject(titleOld, usernameOld, passwordOld, emailOld, locationOld, noteOld, createDateOld, endDate)
                            history.append(passObOld)
                        
                    passOb = passwordSafe.loadPassObject(title, username, password, email, location, note, createDate, history)
                    passOb.setPasswordFile(passwordFile) 

    def decryptFile(self, filename, passPhrase):
        retVal = None
        datei = open(filename, "rb")
        decrypt_data = self.gpg.decrypt_file(datei, passphrase=str(passPhrase), always_trust=True)
        if decrypt_data.ok:
            decrypt = decrypt_data.data
            retVal = xml.dom.minidom.parseString(decrypt)
        datei.close()
        return retVal
    
    def decodeDate(self, date):
        retVal = None
        listDate = date.split('-')
        year = int(listDate[0])
        month = int(listDate[1])
        day = int(listDate[2])
        retVal = datetime.date(year, month, day)
        return retVal

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
    