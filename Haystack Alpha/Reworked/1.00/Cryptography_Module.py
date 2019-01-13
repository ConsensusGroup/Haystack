####################################################################################
############ This script handles encryption and decryption interactions ############
####################################################################################

from Configuration_Module import Configuration
import os

#Cryptography Library
from Crypto.PublicKey import RSA


class Key_Generation(Configuration):
	def __init__(self):
		Configuration.__init__(self)

	def Asymmetric_KeyGen(self):
		pair = RSA.generate(2048)
		self.PrivateKey = pair.exportKey(format = "PEM", passphrase = self.Password)
		self.PublicKey = pair.publickey().exportKey(format = 'PEM')
		return self

	def Secret_Key(self):
		return os.urandom(64)

class Encryption(Configuration):

	def AsymmetricEncryption(self, PlainText, PublicKey):
		cipher = PKCS1_OAEP.new(RSA.importKey(PublicKey))
		return cipher.encrypt(str(PlainText))

	def SymmetricEncryption(self, PlainText, SecretKey):
		string = pyffx.String(str(SecretKey), alphabet = str(self.Charlib) , length=len(str(PlainText))).encrypt(str(PlainText))
		return str(string)

	def MessageSignature(self, ToSign):
		digest = SHA256.new()
		digest.update(ToSign)
		Signer = PKCS1_v1_5.new(User_Profile().PrivateKey)
		self.Signature = Signer.sign(digest)
		return self

class Decryption(Configuration):

	def AsymmetricDecryption(self, CipherText, PrivateKey):

		cipher = PKCS1_OAEP.new(PrivateKey)
		try:
			DecryptedText = cipher.decrypt(str(CipherText))
		except ValueError:
			DecryptedText = "Failed"
		return DecryptedText

	def SymmetricDecryption(self, CipherText, SecretKey):
		return pyffx.String(str(SecretKey), alphabet=str(self.Charlib), length=len(str(CipherText))).decrypt(str(CipherText))

	def SignatureVerification(self, ToVerify, PublicKey, Signature):
		digest = SHA256.new()
		digest.update(ToVerify)
		Verifier = PKCS1_v1_5.new(RSA.importKey(PublicKey))
		self.Verified = Verifier.verify(digest, Signature)
		return self


