'''
Created on 16.04.2015

@author: timgroger
'''

from controller.Environment import Environment 
from model.PasswordFileOption import PasswordFileOption
from model.XmlReader import XmlReader
import xml.dom

class OptionLoader(object):
    '''
    classdocs
    '''
    def __init__(self, filename, controller):
        self.maincontroller = controller
        self.filename = filename       
    
    def loadOptions(self, filename, option):
        datei = open(filename, "r")
        dom = xml.dom.minidom.parse(datei)
        datei.close()

        option.files = []
        
        for elem in dom.getElementsByTagName('Options'):
            for elem1 in elem.getElementsByTagName('ActivateEmail'):
                option.email = self.liesText(elem1)
            for passwordFile in elem.getElementsByTagName('passwordfile'):
                filename = passwordFile.getAttribute('filename')
                encodeId = self.getList(passwordFile.getAttribute('encodeid'))
                encodeId.insert(0, option.getEmail())
                isDefault = XmlReader.getBoolean(passwordFile.getAttribute('isdefault'))
                needBackup = XmlReader.getBoolean(passwordFile.getAttribute('needbackup'))
                version = XmlReader.getIntAttribute(passwordFile, 'version', 2)
                passwordFileOption = PasswordFileOption(filename, encodeId, isDefault=isDefault, needBackup=needBackup, version=version)
                option.files.append(passwordFileOption)
            self.readGuiOption(elem, option.gui)
        self.updateDefaultValues(option)
        self.controlEmailOld(option)
        
    def controlEmailOld(self, option):
        if option.emailOld == None:
            option.emailOld = option.email

    def readGuiOption(self, parent, gui):
        for element in parent.getElementsByTagName('gui'):
            gui.autolock = XmlReader.getIntAttribute(element, 'autolock', gui.autolock)

    def updateDefaultValues(self, option):
        '''
        sets default values that are not saved in the optionfile,
        but that are used implicitly
        '''
        # delete all files that are default, because we are updating
        option.files = [x for x in option.files if not x.isDefault]
        filename = Environment().profileDir + '/' + option.getEmail() + '/safe.xml'
        passwordFileOption = PasswordFileOption(filename, [option.getEmail()], isDefault=True, needBackup=True)
        option.files.insert(0, passwordFileOption)

    
    def liesText(self, knoten):
        '''
        Return the text of the nodeType
        '''
        for k in knoten.childNodes:
            if k.nodeType == k.TEXT_NODE:
                return k.nodeValue.strip()
    
    def getList(self, liststring):
        return liststring.split()
