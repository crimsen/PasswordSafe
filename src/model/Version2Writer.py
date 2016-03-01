'''
Created on Feb 18, 2016

@author: groegert
'''
from XmlMapping import XmlMapping
from XmlWriter import XmlWriter
from model.passObject import PasswordObject
from SecretObjectEnum import SecretObjectEnum
import logging

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
        for obj in item.secretObjects:
            self.writeSecretObject(doc, safeElement, obj)
        doc.documentElement.appendChild(safeElement)
    
    def writeSecretObject(self, doc, element, obj):
        secretElement = doc.createElement(XmlMapping.secretObject)
        secretObjectEnum = None
        if type(obj) == PasswordObject:
            secretObjectEnum = SecretObjectEnum.password
        XmlWriter.setEnumAttribute(secretElement, XmlMapping.type, secretObjectEnum)
        XmlWriter.setStrAttribute(secretElement, XmlMapping.title, obj.getTitle())
        XmlWriter.setStrAttribute(secretElement, XmlMapping.password, obj.getPassword())
        XmlWriter.setStrAttribute(secretElement, XmlMapping.note, obj.getNote())
        XmlWriter.setDateAttribute(secretElement, XmlMapping.createDate, obj.getCreateDate())
        XmlWriter.setDateAttribute(secretElement, XmlMapping.endDate, obj.getEndDate())
        if SecretObjectEnum.password == secretObjectEnum:
            self.writePasswordObject(doc, secretElement, obj)
        else:
            logging.error('unknown secret object type \'%s\'' % obj)
        element.appendChild(secretElement)

    def writePasswordObject(self, doc, element, obj):
        XmlWriter.setStrAttribute(element, XmlMapping.username, obj.getUsername())
        XmlWriter.setStrAttribute(element, XmlMapping.email, obj.getEmail())
        XmlWriter.setStrAttribute(element, XmlMapping.location, obj.getLocation())
    
