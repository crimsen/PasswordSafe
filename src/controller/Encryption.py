'''
Created on Jul 13, 2016

@author: groegert
'''

from model.Option import Option
import gnupg
import sys

class Encryption(object):
    '''
    class encapsulates the encryption and decryption 
    '''


    def __init__(self, option):
        '''
        Constructor
        '''
        self.option = option
        self.gpg = gnupg.GPG()
        
    def getSecretKeys(self):
        '''
        returns usable secret keys
        the keys are human readable strings that uniquely identifies the secret keys
        for GPG these are the email-addresses (GPG().list_keys())
        '''
        retVal = self.getGpgSecretKeys()
        return retVal
    
    def decryptData(self, data, passPhrase):
        retVal = self.gpg.decrypt(data, passphrase=str(passPhrase), always_trust=True)
        return retVal

    def encryptData(self, data, keyIds):
        retVal = self.gpg.encrypt(data, keyIds, always_trust=True)
        return retVal
    
    def getGpgSecretKeys(self):
        retVal = []
        secretKeys = self.gpg.list_keys(True)
        uids = []
        emails = []
    
        for keys in secretKeys:
            uids.append(keys['uids'])
        
        for account in uids:
            for email in account:
                if sys.hexversion < 0x3000000:
                    email = email.encode('utf-8')
                emailsplit = email.split(' ')
                emails.append(emailsplit[len(emailsplit)-1])
        retVal = self._cleanList(emails)
        return retVal
    def _cleanList(self, list):
        accounts = []
        for i in list:
            accounts.append(self._cleanString(i))
        return accounts
        
    def _cleanString(self, string): 
        retVal = ''
        for i in string:
            if (i!='<') and (i!='>'):
                retVal+=i
        return retVal

'''
PasswordSafe
gui.AccountPage (2 matches)
  50:self.labelLink = tk.Label(master=self.frameInfo, text='GPG Link', fg='blue', cursor='hand2')
  92:secretKeys = gnupg.GPG().list_keys(True)
model.OptionLoader (3 matches)
  20:self.gpg = gnupg.GPG()
  27:secretKeys = self.gpg.list_keys(True)
model.PasswordSafe (5 matches)
  23:self.gpg = gnupg.GPG()
  64:passwordSafeReader = PasswordSafeReader(self.option, self.gpg)
  71:passwordSafeWriter = PasswordSafeWriter(self.option, self.gpg)
model.PasswordSafeReader (4 matches)
  123:decrypt_data = self.gpg.decrypt_file(datei, passphrase=str(passPhrase), always_trust=True)
  19:def __init__(self, option, gpg):
  24:self.gpg = gpg
model.PasswordSafeWriter (4 matches)
  21:def __init__(self, option, gpg):
  26:self.gpg = gpg
  62:encrypt = self.gpg.encrypt(noneencrypt, encodeIds, always_trust=True)

'''