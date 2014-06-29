from simplecrypt import encrypt, decrypt

class encryption():

    def __init__(self):
        self.passphrase = 'ijdffuihadkjasdf89we7t43t78q34thiasfljb<78wqer78q34rearu8afjk'

    def encryptText(self, text):
        return encrypt(self.passphrase, text).decode('raw_unicode_escape')

    def decryptText(self, ciphertext):
        return decrypt(self.passphrase, ciphertext.encode('raw_unicode_escape')).decode('UTF-8')