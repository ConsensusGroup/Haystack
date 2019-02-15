####################################################################################
############ This script handles encryption and decryption interactions ############
####################################################################################


import os

# Imprt some modules 
from Configuration_Module import Configuration
from Tools_Module import Tools

#Cryptography Library
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
import pyffx
from base64 import b64encode, b64decode


class Key_Generation(Configuration):
	def __init__(self):
		Configuration.__init__(self)

	def Asymmetric_KeyGen(self):
		pair = RSA.generate(2048)
		self.PrivateKey = pair.exportKey(format = "PEM", passphrase = self.Password)
		self.PublicKey = pair.publickey().exportKey(format = 'PEM')
		return self

	def PrivateKey_Import(self):
		PrivateCipher = Tools().ReadLine(directory = str(self.UserFolder+"/"+self.KeysFolder+"/"+self.PrivateKey))
		Keys = RSA.importKey(PrivateCipher, passphrase = self.Password)
		self.PublicKey = Keys.publickey().exportKey(format = 'PEM')
		self.PrivateKey = Keys 
		return self

	def Secret_Key(self, length = 64):
		return os.urandom(length)

class Encryption(Configuration):
	def __init__(self):
		pass

	def AsymmetricEncryption(self, PlainText, PublicKey):
		cipher = PKCS1_OAEP.new(RSA.importKey(PublicKey))
		return cipher.encrypt(str(PlainText))

	def SymmetricEncryption(self, PlainText, SecretKey = ""):
		Cypher = pyffx.String(str(SecretKey), alphabet = str(self.Charlib) , length=len(PlainText)).encrypt(str(PlainText))
		return str(Cypher)

	def MessageSignature(self, ToSign):
		digest = SHA256.new()
		digest.update(ToSign)
		Signer = PKCS1_v1_5.new(Key_Generation().PrivateKey_Import().PrivateKey)
		self.Signature = Signer.sign(digest)
		return self

	def Layering_Encryption(self, PlainText, PublicKey, Address, SymKey = ""):
		if SymKey == "":
			SymKey = self.Secret_Key()
		To_Encrypt = str(SymKey + Address)
		Cypher_Asym = b64encode(self.AsymmetricEncryption(PlainText = To_Encrypt, PublicKey = PublicKey))
		Cypher_Sym = self.SymmetricEncryption(PlainText = b64encode(PlainText), SecretKey = SymKey)
		self.Cipher = str(Cypher_Sym + self.Identifier + Cypher_Asym)
		return self

class Decryption(Configuration):

	def AsymmetricDecryption(self, CipherText, PrivateKey):
		cipher = PKCS1_OAEP.new(PrivateKey)
		try:
			DecryptedText = cipher.decrypt(str(CipherText))
		except ValueError:
			DecryptedText = False
		return DecryptedText

	def SymmetricDecryption(self, CipherText, SecretKey):
		try:
			outcome = pyffx.String(str(SecretKey), alphabet=str(self.Charlib), length=len(str(CipherText))).decrypt(str(CipherText))
		except ValueError:
			outcome = False
		return outcome	

	def SignatureVerification(self, ToVerify, PublicKey, Signature):
		digest = SHA256.new()
		digest.update(ToVerify)
		Verifier = PKCS1_v1_5.new(RSA.importKey(PublicKey))
		self.Verified = Verifier.verify(digest, Signature)
		return self

