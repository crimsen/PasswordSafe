'''
Created on May 8, 2015

@author: thomas
'''

import xml.dom

class OptionWriter(object):
    '''
    this is a writer that writes the option model into an xml file
    '''


    def __init__(self):
        '''
        we do not have special parameters i.e. charset yet, so no initialization is done
        '''
    
    def write(self, option, filename):
        implement = xml.dom.getDOMImplementation()
        document = implement.createDocument(None, 'Options', None)
        self.writeEmailOption(option.getEmail(), document)
        xmlfile = open(filename, 'w')
        document.writexml(xmlfile, '\n', ' ')
        xmlfile.close()

    def writeEmailOption(self, email, document):
        emailElem = document.createElement('ActivateEmail')
        emailTextElem = document.createTextNode(email)
        emailElem.appendChild(emailTextElem)
        
        document.documentElement.appendChild(emailElem)
