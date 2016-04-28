'''
Created on Feb 16, 2016

@author: groegert
'''

from XmlMapping import XmlMapping
from XmlReader import XmlReader
from SecretObjectEnum import SecretObjectEnum
from model.passObject import PasswordObject
from model.CertificateObject import CertificateObject
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
            for elem2 in elem1.getElementsByTagName(XmlMapping.secretObject):
                secretObjects.append(self.readSecretObject(elem2))
            if 0 >= len(secretObjects):
                logging.error('there is an safeitem without objects')
            else:
                safeItem = passwordSafe.createSafeItem(secretObjects)
                safeItem.setPasswordFile(passwordFile)
            passwordSafe.addSafeItem(safeItem)
        
    def readSecretObject(self, element):
        retVal = None
        title = XmlReader.getStrAttribute(element, XmlMapping.title, '')
        password = XmlReader.getStrAttribute(element, XmlMapping.password, '')
        note = XmlReader.getStrAttribute(element, XmlMapping.note, '')
        createDate = XmlReader.getDateAttribute(element, XmlMapping.createDate, None)
        endDate = XmlReader.getDateAttribute(element, XmlMapping.endDate, None)
        
        stype = XmlReader.getEnumAttribute(element, XmlMapping.type, SecretObjectEnum, None)
        if SecretObjectEnum.password == stype:
            retVal = self.readPasswordObject(element)
        elif SecretObjectEnum.smime == stype:
            retVal = self.readSMimeObject(element)
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

    def readSMimeObject(self, element):
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
