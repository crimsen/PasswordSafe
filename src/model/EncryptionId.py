'''
Created on Jun 22, 2023

@author: groegert
'''

class EncryptionId(object):
    '''
    class that encapsulates an encryption key i.e. a GPG-key
    This is needed because the human readable form does not always identify such encryption key.
    i.e. there might be several GPG-keys that do have the same uid. These keys still have to be
    distinguishable.
    '''
    def __init__(self, id = "", label = ""):
        self.id = id
        self.label = label
