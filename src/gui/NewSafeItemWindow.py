'''
Created on 28.03.2015

@author: crimsen
'''
from gui.Wizard import Wizard
from gui.Wizard import WizardView
from gui.Wizard import WizardController
from gui.CertificatePage import CertificatePage
from gui.CertificatePage import CertificatePageContext
from gui.EmptyPage import EmptyPage
from gui.EmptyPage import EmptyPageContext
from gui.PasswordForm import PasswordForm
from gui.PasswordForm import PasswordFormContext
from gui.SafeItemPage import SafeItemPage
from gui.SafeItemPage import SafeItemPageContext
from model.CertificateObject import CertificateObject
from model.NewSafeItemWindowOption import NewSafeItemWindowOption
from model.passObject import PasswordObject
from model.SecretObjectEnum import SecretObjectEnum
from edit.AddSafeItemCmd import AddSafeItemCmd

class NewSafeItemWindow(Wizard):
    '''
    NewSafeItemWindow is a top level window to create new safe items.
    First it collects all data that are needed for a new safe item:
    - the type of the secret item
    - the file where the save item has to be stored
    - the data in the secret item
    All this data is stored in NewSafeItemWindowOption.
    When there is a lock in between the NewSafeItemWindow can be completely
    restored from NewSafeItemWindowOption.
    '''
    def __init__(self, context, viewModel = None):
        if None == viewModel:
            viewModel = NewSafeItemWindowOption()
        Wizard.__init__(self, context, viewModel)
        NewSafeItemWindowController.santinizeModel(viewModel, context)
        self.view = NewSafeItemWindowView(context, viewModel)
        #self.model = context.master.createPasswordItem()
        self.controller = NewSafeItemWindowController(self.view, viewModel, context)

    def show(self):
        self.view.show()
    
    def close(self):
        self.view.close()

class NewSafeItemWindowContext(object):
    def __init__(self, client, master, editingDomain):
        self.client = client
        self.master = master
        self.editingDomain = editingDomain
    def getClient(self):
        return self.client
    def getEditingDomain(self):
        return self.editingDomain
    def getOption(self):
        return self.client
        
class NewSafeItemWindowView(WizardView):
        
    class PasswordFormContext(PasswordFormContext):
        def __init__(self, parentContext):
            PasswordFormContext.__init__(self, parentContext.client.context)
            self.mode = 'edit'
    class CertificatePageContext(CertificatePageContext):
        def __init__(self, parentContext):
            CertificatePageContext.__init__(self, parentContext.client.context)
            self.mode = 'edit'

    def __init__(self, context, viewModel):
        WizardView.__init__(self, context, viewModel)
        self.__buildFrame__()
        
    def __buildFrame__(self):
        WizardView.__buildFrame__(self)
        self.updateFromModel()
        #self.form = PasswordForm(parent, NewSafeItemWindowView.PasswordFormContext(self.context))
        #self.form.setMode('edit')
        self.__packFrame__()

    def canApply(self):
        retVal = False
        if 1 * self.viewModel.canChangeSafeItemType == self.viewModel.currentPage:
            if None != self.viewModel.safeItem:
                retVal = True
        return retVal
    def hasNextPage(self):
        retVal = False
        if 1 * self.viewModel.canChangeSafeItemType > self.viewModel.currentPage:
            retVal = True
        return retVal
    def hasPrevPage(self):
        retVal = False
        if 1 * self.viewModel.canChangeSafeItemType <= self.viewModel.currentPage:
            retVal = True
        return retVal

    def updateFromModel(self):
        '''
        updates all the view with the entered data
        '''
        self.updatePages()
        childViewModel = self.getChildModel()
        self.currentPage[1].setModel(childViewModel)
        self.finishCurrentPagePacked()
        self.updateButtonFrame()
    def updatePages(self):
        '''
        specifies which pages will be displayed and which page is current
        '''
        safeItemType = self.viewModel.safeItemType
        pageId = self.getPageId(self.viewModel.canChangeSafeItemType, safeItemType, self.viewModel.currentPage)
        page = None
        if pageId in self.pages:
            page = self.pages[pageId]
        if None == page:
            pageDescription = (None, None)
            if self.viewModel.canChangeSafeItemType and 0 == self.viewModel.currentPage:
                pageDescription = (SafeItemPage, SafeItemPageContext(self.context.getOption()))
            elif SecretObjectEnum.password == safeItemType and 0 == self.viewModel.currentPage - 1 * self.viewModel.canChangeSafeItemType:
                pageDescription = (PasswordForm, NewSafeItemWindowView.PasswordFormContext(self.context))
            elif SecretObjectEnum.smime == safeItemType and 0 == self.viewModel.currentPage - 1 * self.viewModel.canChangeSafeItemType:
                pageDescription = (CertificatePage, NewSafeItemWindowView.CertificatePageContext(self.context))
            else:
                pageDescription = (EmptyPage, EmptyPageContext(self.context.getOption()))
            page = self.buildFormPage(pageDescription)
            self.pages[pageId] = page
        self.setCurrentPageUnpacked(page)
    def getPageId(self, canChangeSafeItemType, safeItemType, pageIdx):
        retVal = pageIdx + 16 * safeItemType.value + ( 16 + 16 ) * canChangeSafeItemType
        return retVal
    def getChildModel(self):
        retVal = None
        safeItemType = self.viewModel.safeItemType
        if self.viewModel.canChangeSafeItemType and 0 == self.viewModel.currentPage:
            retVal = self.viewModel
        elif (SecretObjectEnum.password == safeItemType or SecretObjectEnum.smime == safeItemType) and 0 == self.viewModel.currentPage - 1 * self.viewModel.canChangeSafeItemType:
            retVal = self.viewModel.safeItem
        return retVal

class NewSafeItemWindowController(WizardController):
    def __init__(self, view, model, context):
        WizardController.__init__(self, view, model, context)

    @staticmethod
    def santinizeModel(model, context):
        if None == model.safeItemType:
            model.safeItemType = SecretObjectEnum.password
        if None != model.safeItem:
            # if the type does not match the safeitem
            if model.safeItemType == SecretObjectEnum.password:
                if type(model.safeItem.getCurrentSecretObject()) != PasswordObject:
                    model.safeItem = None
            elif model.safeItemType == SecretObjectEnum.smime:
                if type(model.safeItem.getCurrentSecretObject()) != CertificateObject:
                    model.safeItem = None
            else:
                model.safeItem = None
        if None == model.safeItem:
            if SecretObjectEnum.password == model.safeItemType:
                model.safeItem = context.master.createPasswordItem()
            elif SecretObjectEnum.smime == model.safeItemType:
                model.safeItem = context.master.createSmimeItem()

    def pressSave(self):
        '''
        Set a new passwordobject
        And destroy the widget
        '''
        self.view.currentPage[1].apply()
        if None != self.editingDomain and None != self.model.safeItem:
            self.editingDomain.executeCmd(AddSafeItemCmd(self.editingDomain.getModel(), self.model.safeItem))
            if None != self.client:
                self.client.onSafeChanged()
        self.view.close()
    def pressNext(self):
        safeItemType = self.model.safeItemType
        self.view.currentPage[1].apply()
        if safeItemType != self.model.safeItemType:
            self.santinizeModel(self.model, self.context)
        self.stepPage(1)
        self.view.updateFromModel()
    def pressPrev(self):
        self.view.currentPage[1].apply()
        self.stepPage(-1)
        self.view.updateFromModel()
    def stepPage(self, step):
        self.model.currentPage = self.model.currentPage + step
            
if __name__=='__main__':
    test = NewSafeItemWindow(None)
    test.show()
