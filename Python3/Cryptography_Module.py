#Modules being imported
from Configuration_Module import Configuration
from Tools_Module import Encoding
import os

#PyCrypto library
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

#Symmetric encryption library
import pyffx


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

    def Secret_Key(self, length = Configuration().SymKey_Length):
        return Encoding().To_Base64(Input = os.urandom(length))[0:length]

class Encryption:
    def __init__(self):
        pass

    def Asymmetric_Encryption(self, PlainText, PublicKey):
        cipher = PKCS1_OAEP.new(RSA.importKey(PublicKey))
        try:
            output = cipher.encrypt(PlainText.encode())
        except:
            output = cipher.encrypt(PlainText)
        return output

    def Sign_Message(self, ToSign, PrivateKey, Password):
        digest = SHA256.new()
        digest.update(ToSign)
        Signer = PKCS1_v1_5.new(RSA.importKey(PrivateKey, Password))
        Signature = Signer.sign(digest)
        return Signature

    def Symmetric_Encryption(self, PlainText, SecretKey):
        if isinstance(PlainText, str) == False:
            PlainText = PlainText.decode()
        if isinstance(SecretKey, bytes) == False:
            SecretKey = SecretKey.encode()
        cipher = pyffx.String(SecretKey, alphabet = Configuration().Charlib, length = len(PlainText)).encrypt(PlainText)
        return cipher.encode()

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

class Layering_Encryption:
    def __init__(self):
        pass

    def Cipher_Generator(self, Bounces, Destination):
        for i in range(len(Destination)-1):
            Sym_Key = Key_Generation().Secret_Key()
            Address_SymKey = Destination[i+1][0].encode() + Sym_Key
            Public_Key = Destination[i][1]
            if i == 0:
                Symmetric = Encryption().Symmetric_Encryption(PlainText = Destination[0][0] + Sym_Key, SecretKey = Sym_Key)
                Layer = Encoding().To_Base64(Input = Encryption().Asymmetric_Encryption(PlainText = Symmetric + Destination[i+1][0].encode() + Sym_Key, PublicKey = Encoding().From_Base64(Input = Public_Key)))
            else:
                Symmetric = Symmetric + Address_SymKey
                Phase_Shift = Symmetric[len(Symmetric)-214:]
                Residue = Symmetric[:len(Symmetric)-214]
                Layer = Residue + Encoding().To_Base64(Input = Encryption().Asymmetric_Encryption(PlainText = Phase_Shift, PublicKey = Encoding().From_Base64(Input = Public_Key)))

            Symmetric = Encryption().Symmetric_Encryption(PlainText = Layer, SecretKey = Sym_Key)
            x = len(Symmetric)
        print(x)
