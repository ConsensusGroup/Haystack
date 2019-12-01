#Modules being imported
from Configuration_Module import Configuration

#PyCrypto library
from Crypto.PublicKey import RSA

class Key_Generation(Configuration):
    def __init__(self):
        Configuration.__init__(self)

    def Asymmetric_KeyGen(self, Password):
        pair = RSA.generate(2048)
        PrivateKey = pair.exportKey(format = "PEM", passphrase = Password)
        return PrivateKey

    def Import_PrivateKey(self, PrivateKey, Password):
        Keys = RSA.importKey(PrivateKey, Password)
        self.PublicKey = Keys.publickey().exportKey(format = "PEM")
        self.PrivateKey = Keys
        return self
