'''
Created on May 29, 2015

@author: thomas
'''

from model.PasswordFileOption import PasswordFileOption
from model.Version2Writer import Version2Writer
from model.XmlMapping import XmlMapping
from model.XmlWriter import XmlWriter
from datetime import datetime
import os
import logging
import shutil
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
        self.xmlMapping = XmlMapping
    
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
        safeVersion = PasswordFileOption.defaultVersion
        fileVersion = passwordFile.getVersion()
        writer = None
        if 0 != fileVersion:
            safeVersion = fileVersion
        if 2 <= safeVersion:
            XmlWriter.setIntAttribute(doc.documentElement, XmlMapping.version, safeVersion)
            writer = Version2Writer()
        
        for i in passwordSafe.getSafe():
            if ((i.getPasswordFile() == passwordFile) or 
                ((i.getPasswordFile() == None) and passwordFile.isDefault)) :
                if 1 == safeVersion:
                    self.writePasswordItem(doc, i)
                elif 2 == safeVersion:
                    writer.writeSafeItem(doc, i)
        
        noneencrypt = doc.toprettyxml(' ','\n',encoding='UTF-8')
        encodeIds = [str(i) for i in passwordFile.getEncodeId()]
        encrypt = self.gpg.encrypt(noneencrypt, encodeIds, always_trust=True)
        encryptStr = str(encrypt)
        #ecrypt.valid is not usable, it is always False
        if ('encryption ok' != encrypt.status) or (0 == len(encryptStr)):
            logging.error('unable to encrypt file: %s' % encrypt.status)
            logging.error(encrypt.stderr)
        else:
            datei = open(passwordFile.getFilename(), 'w')
            datei.write(str(encrypt))
            datei.close()

    def writePasswordItem(self, doc, item):
        secretItem = item.getCurrentSecretObject()
        safeElem = doc.createElement('Safe')
            
        titleElem = doc.createElement('Title')
        safeElem.appendChild(titleElem)
        titleTextElem = doc.createTextNode(secretItem.getTitle())
        titleElem.appendChild(titleTextElem)
    
        usernameElem = doc.createElement('Username')
        safeElem.appendChild(usernameElem)
        usernameTextElem = doc.createTextNode(secretItem.getUsername())
        usernameElem.appendChild(usernameTextElem)
    
        passwordElem = doc.createElement('Password')
        safeElem.appendChild(passwordElem)
        passwordTextElem = doc.createTextNode(secretItem.getPassword())
        passwordElem.appendChild(passwordTextElem)
    
        emailElem = doc.createElement('EMail')
        safeElem.appendChild(emailElem)
        emailTextElem = doc.createTextNode(secretItem.getEmail())
        emailElem.appendChild(emailTextElem)
    
        locationElem = doc.createElement('URL')
        safeElem.appendChild(locationElem)
        locationTextElem = doc.createTextNode(secretItem.getLocation())
        locationElem.appendChild(locationTextElem)
    
        noteElem = doc.createElement('Note')
        safeElem.appendChild(noteElem)
        noteTextElem = doc.createTextNode(secretItem.getNote())
        noteElem.appendChild(noteTextElem)
        
        createDateElem = doc.createElement('CreateDate')
        safeElem.appendChild(createDateElem)
        createDateTextElem = doc.createTextNode(secretItem.getCreateDate().isoformat())
        createDateElem.appendChild(createDateTextElem)
        
        historyElem = doc.createElement('History')
        safeElem.appendChild(historyElem)
        for passOb in item.getHistory():
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
            
            createDateElem = doc.createElement('CreateDateOld')
            safeElemOld.appendChild(createDateElem)
            createDateTextElem = doc.createTextNode(passOb.getCreateDate().isoformat())
            createDateElem.appendChild(createDateTextElem)
            
            endDateElem = doc.createElement('EndDate')
            safeElemOld.appendChild(endDateElem)
            endDateTextElem = doc.createTextNode(passOb.getEndDate().isoformat())
            endDateElem.appendChild(endDateTextElem)
    
        doc.documentElement.appendChild(safeElem)

    def doBackup(self, filename):
        (directory, filepart) = os.path.split(filename)
        today = datetime.today()
        filepart = str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + filepart
        backupFilename = os.path.join(directory, 'backup', filepart)
        self.assureDirectory(backupFilename)
        logging.info(backupFilename)
        
        shutil.copy(filename, backupFilename)
        logging.info('backup completed')

    def assureDirectory(self, filename):
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
