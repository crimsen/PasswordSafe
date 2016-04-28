'''
Created on Feb 18, 2016

@author: groegert
'''

class XmlWriter(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    @staticmethod
    def setStrAttribute(element, attributeName, val):
        if None != val:
            element.setAttribute(attributeName, val)

    @staticmethod
    def setIntAttribute(element, attributeName, val):
        if None != val:
            element.setAttribute(attributeName, str(val))

    @staticmethod
    def setDateAttribute(element, attributeName, val):
        if None != val:
            strVal = val.isoformat()
            element.setAttribute(attributeName, strVal)

    @staticmethod
    def setEnumAttribute(element, attributeName, val):
        if None != val:
            element.setAttribute(attributeName, val.name)

    @staticmethod
    def setText(doc, element, val):
        if None != val:
            textNode = doc.createTextNode(val)
            element.appendChild(textNode)
