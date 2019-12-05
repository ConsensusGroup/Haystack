#Modules being imported
from Configuration_Module import Configuration

#PyCrypto library
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

class Key_Generation:
    def __init__(self):
        pass
    def Asymmetric_KeyGen(self, Password):
        pair = RSA.generate(2048)
        PrivateKey = pair.exportKey(format = "PEM", passphrase = Password)
        return PrivateKey

    def Import_PrivateKey(self, PrivateKey, Password):
        Keys = RSA.importKey(PrivateKey, Password)
        self.PublicKey = Keys.publickey().exportKey(format = "PEM")
        self.PrivateKey = Keys
        return self

class Encryption:
    def __init__(self):
        pass

    def Asymmetric_Encryption(self, PlainText, PublicKey):
        cipher = PKCS1_OAEP.new(RSA.importKey(PublicKey))
        return cipher.encrypt(PlainText.encode())

    def Sign_Message(self, ToSign, PrivateKey, Password):
        digest = SHA256.new()
        digest.update(ToSign)
        Signer = PKCS1_v1_5.new(RSA.importKey(PrivateKey, Password))
        Signature = Signer.sign(digest)
        return Signature

class Decryption:
    def __init__(self):
        pass

    def Asymmetric_Decryption(self, CipherText, PrivateKey, Password):
        try:
            cipher = PKCS1_OAEP.new(RSA.importKey(PrivateKey, Password))
            DecryptedText = cipher.decrypt(CipherText)
        except ValueError:
            DecryptedText = False
        return DecryptedText

    def Signature_Verification(self, ToVerify, PublicKey, Signature):
        digest = SHA256.new()
        digest.update(ToVerify)
        Verifier = PKCS1_v1_5.new(RSA.importKey(PublicKey))
        Verified = Verifier.verify(digest, Signature)
        return Verified
