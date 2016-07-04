'''
Created on Feb 16, 2016

@author: groegert
'''

from model.CertificateObject import CertificateObject
from model.PasswordObject import PasswordObject
from model.SecretObjectEnum import SecretObjectEnum
from model.XmlMapping import XmlMapping
from model.XmlReader import XmlReader
import logging

class Version2Reader(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def readSafe(self, element, passwordSafe, passwordFile):
        for elem1 in element.getElementsByTagName(XmlMapping.safeItem):
            secretObjects = []
            secretObjectEnum = None

            for elem2 in elem1.getElementsByTagName(XmlMapping.secretObject):
                if None == secretObjectEnum:
                    secretObjectEnum = XmlReader.getEnumAttribute(elem2, XmlMapping.type, SecretObjectEnum, None)
                secretObjects.append(self.readSecretObject(elem2))
            if 0 >= len(secretObjects):
                logging.error('there is an safeitem without objects')
            else:
                safeItem = passwordSafe.createSafeItem(secretObjects, secretObjectEnum)
                safeItem.setPasswordFile(passwordFile)
            passwordSafe.addSafeItem(safeItem)
        
    def readSecretObject(self, element):
        retVal = None
        title = XmlReader.getStrAttribute(element, XmlMapping.title, '')
        password = XmlReader.getStrAttribute(element, XmlMapping.password, '')
        note = XmlReader.getStrAttribute(element, XmlMapping.note, '')
        note = note.replace('&#10;', '\n')
        createDate = XmlReader.getDateAttribute(element, XmlMapping.createDate, None)
        endDate = XmlReader.getDateAttribute(element, XmlMapping.endDate, None)
        
        stype = XmlReader.getEnumAttribute(element, XmlMapping.type, SecretObjectEnum, None)
        if SecretObjectEnum.password == stype:
            retVal = self.readPasswordObject(element)
        elif SecretObjectEnum.smime == stype or SecretObjectEnum.gpg == stype:
            retVal = self.readCertificateObject(element)
        retVal.setTitle(title)
        retVal.setPassword(password)
        retVal.setNote(note)
        retVal.setCreateDate(createDate)
        retVal.setEndDate(endDate)
        return retVal

    def readPasswordObject(self, element):
        retVal = PasswordObject()
        username = XmlReader.getStrAttribute(element, XmlMapping.username, '')
        email = XmlReader.getStrAttribute(element, XmlMapping.email, '')
        location = XmlReader.getStrAttribute(element, XmlMapping.location, '')
        retVal.setUsername(username)
        retVal.setEmail(email)
        retVal.setLocation(location)
        return retVal

    def readCertificateObject(self, element):
        retVal = CertificateObject()
        for secretKeyElement in element.getElementsByTagName(XmlMapping.secretKey):
            fileName = XmlReader.getStrAttribute(secretKeyElement, XmlMapping.fileName, '')
            secretKey = XmlReader.getText(secretKeyElement)
            retVal.setSecretKeyFileName(fileName)
            retVal.setSecretKey(secretKey)
        for publicKeyElement in element.getElementsByTagName(XmlMapping.publicKey):
            fileName = XmlReader.getStrAttribute(publicKeyElement, XmlMapping.fileName, '')
            publicKey = XmlReader.getText(publicKeyElement)
            retVal.setPublicKeyFileName(fileName)
            retVal.setPublicKey(publicKey)
        return retVal
