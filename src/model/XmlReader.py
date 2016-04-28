'''
Created on Feb 12, 2016

@author: groegert
'''

import logging
import datetime
import xml.dom

class XmlReader(object):
    '''
    some functions that every xml-based reader should have
    '''

    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def getBoolean(boolstring):
        return boolstring in ['true']

    @staticmethod
    def decodeDate(datestring):
        listDate = datestring.split('-')
        year = int(listDate[0])
        month = int(listDate[1])
        day = int(listDate[2])
        retVal = datetime.date(year, month, day)
        return retVal

    @staticmethod
    def getStrAttribute(element, attributeName, defaultValue):
        retVal = defaultValue
        attributeNode = element.getAttributeNode(attributeName)
        if None != attributeNode:
            retVal = attributeNode.value
        return retVal

    @staticmethod
    def getBoolAttribute(element, attributeName, defaultValue):
        retVal = defaultValue
        attributeNode = element.getAttributeNode(attributeName)
        if None != attributeNode:
            retVal = XmlReader.getBoolean(attributeNode.value)
        return retVal
    
    @staticmethod
    def getIntAttribute(element, attributeName, defaultValue):
        retVal = defaultValue
        attributeNode = element.getAttributeNode(attributeName)
        if None != attributeNode:
            retVal = int(attributeNode.value)
        return retVal

    @staticmethod
    def getDateAttribute(element, attributeName, defaultValue):
        retVal = defaultValue
        attributeNode = element.getAttributeNode(attributeName)
        if None != attributeNode:
            retVal = XmlReader.decodeDate(attributeNode.value)
        return retVal
    
    @staticmethod
    def getEnumAttribute(element, attributeName, enumType, defaultValue):
        retVal = defaultValue
        attributeNode = element.getAttributeNode(attributeName)
        if None != attributeNode:
            try:
                retVal = enumType[attributeNode.value]
            except KeyError as e:
                logging.error('element \'%s\' does not support type \'%s\'' % (element.name, attributeNode.value))
                pass
        return retVal

    @staticmethod
    def getText(element):
        retVal = ''
        for node in element.childNodes:
            if xml.dom.Node.TEXT_NODE == node.nodeType:
                retVal += node.data
        return retVal
