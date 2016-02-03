'''
Created on Jan 29, 2016

@author: groegert
'''

class EditingDomain(object):
    '''
    this class ist for keeping track of modifications that are done via commands
    so every ui should modifiy the model via this editing domain
    view -> editing domain -> model
    '''

    def __init__(self, model=None):
        '''
        Constructor
        '''
        self.model = model
        self.cmdQueue = []
        #TODO: cmdQueueLen as option
        self.cmdQueueLen = 20

    def setModel(self, model):
        self.model = model
    def getModel(self):
        return self.model

    def executeCmd(self, cmd):
        if cmd.canDo():
            cmd.doExecute()
        self.cmdQueue.append(cmd)
        while len(self.cmdQueue) > self.cmdQueueLen:
            self.cmdQueue.pop(0)
        self.model.save()
    