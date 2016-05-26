'''
Created on Feb 18, 2016

@author: groegert
'''
from XmlMapping import XmlMapping
from XmlWriter import XmlWriter
from model.PasswordObject import PasswordObject
from SecretObjectEnum import SecretObjectEnum
import logging
from model.CertificateObject import CertificateObject

class Version2Writer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def writeSafeItem(self, doc, item):
        safeElement = doc.createElement(XmlMapping.safeItem)
        secretObjectEnum = item.getType()
        for obj in item.secretObjects:
            self.writeSecretObject(doc, safeElement, obj, secretObjectEnum)
        doc.documentElement.appendChild(safeElement)
    
    def writeSecretObject(self, doc, element, obj, secretObjectEnum):
        secretElement = doc.createElement(XmlMapping.secretObject)
        XmlWriter.setEnumAttribute(secretElement, XmlMapping.type, secretObjectEnum)
        XmlWriter.setStrAttribute(secretElement, XmlMapping.title, obj.getTitle())
        XmlWriter.setStrAttribute(secretElement, XmlMapping.password, obj.getPassword())
        XmlWriter.setStrAttribute(secretElement, XmlMapping.note, obj.getNote())
        XmlWriter.setDateAttribute(secretElement, XmlMapping.createDate, obj.getCreateDate())
        XmlWriter.setDateAttribute(secretElement, XmlMapping.endDate, obj.getEndDate())
        if SecretObjectEnum.password == secretObjectEnum:
            self.writePasswordObject(doc, secretElement, obj)
        elif SecretObjectEnum.smime == secretObjectEnum or SecretObjectEnum.gpg == secretObjectEnum:
            self.writeCertificateObject(doc, secretElement, obj)
        else:
            logging.error('unknown secret object type \'%s\'' % obj)
        element.appendChild(secretElement)

    def writePasswordObject(self, doc, element, obj):
        XmlWriter.setStrAttribute(element, XmlMapping.username, obj.getUsername())
        XmlWriter.setStrAttribute(element, XmlMapping.email, obj.getEmail())
        XmlWriter.setStrAttribute(element, XmlMapping.location, obj.getLocation())
        
    def writeCertificateObject(self, doc, element, obj):
        secretKeyFileElement = doc.createElement(XmlMapping.secretKey)
        XmlWriter.setStrAttribute(secretKeyFileElement, XmlMapping.fileName, obj.getSecretKeyFileName())
        XmlWriter.setText(doc, secretKeyFileElement, obj.getSecretKey())
        element.appendChild(secretKeyFileElement)
        publicKeyFileElement = doc.createElement(XmlMapping.publicKey)
        XmlWriter.setStrAttribute(publicKeyFileElement, XmlMapping.fileName, obj.getPublicKeyFileName())
        XmlWriter.setText(doc, publicKeyFileElement, obj.getPublicKey())
        element.appendChild(publicKeyFileElement)
