#Iota library
from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.crypto.addresses import AddressGenerator
from iota.adapter.wrappers import RoutingWrapper
from iota import *

#Encryption
from encryption_module import decode
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
from random import SystemRandom

#Other
import random
import pyffx
import os
import sys
from base64 import b64encode, b64decode

#This class is responsible for the encryption side of things
class Encrypt:
	def __init__(self, PlainText = "", PubKey = "", CharLib = ".ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= "):
		#First statement is the symmetric encryption 
		if PubKey == "":
			SecretKey = Generators().Secret_Key().SecretKey
			cipher = pyffx.String(SecretKey, alphabet = CharLib , length=len(str(PlainText)))
		#Asymetric encryption
		else:
			Key = RSA.importKey(PubKey)
			cipher = PKCS1_OAEP.new(Key)				
		self.CipherText = cipher.encrypt(PlainText)


class Decryption:
	def __init__(self, Password ="", CipherText = "", CharLib = ".ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= "):
		SecretKey = Generators().Secret_Key().SecretKey
		if Password == "":
			cipher = pyffx.String(SecretKey, alphabet = CharLib, length = len(str(CipherText)))
		else:
			PrivKey = Generators(Pass = Password).Key_Pair().PrivateKey
			cipher = PKCS1_OAEP.new(PrivKey)
		self.DecryptedText = cipher.decrypt(CipherText)
		
class User_Module:
	#initializes the class by building the directory
	def __init__(self, directory = "UserData", SeedFile = "Seed_Key.txt", RSA = "Keys", password = ""):
		if not os.path.exists(str(directory+"/"+RSA)):
			try:
				os.makedirs(directory)
			except OSError:
				pass
				
			os.makedirs(str(directory+"/"+RSA))
			
		self.PrivateKey = Generators(Pass = password).Key_Pair().PrivateKey
		self.PublicKey = Generators(Pass = password).Key_Pair().PublicKey
		
		if not os.path.isfile(str(directory+"/"+SeedFile)):
		
			self.Seed = Generators().Seed_Generator().Seed
			EncodedSeed = Encrypt(PlainText = self.Seed, PubKey = self.PublicKey).CipherText		
			Writing_And_Reading().Writing(str(directory+"/"+SeedFile),EncodedSeed)
		else:
			EncodedSeed = Writing_And_Reading().Reading(str(directory+"/"+SeedFile))
			self.Seed = Decryption(CipherText = EncodedSeed, Password = password).DecryptedText
			
			
class Generators:
	#Generates a random seed
	def __init__(self, Pass = ""):
		self.password = Pass
	
	def Seed_Generator(self):
		rand = SystemRandom()
		random_trytes = [i for i in map(chr, range(65,91))]
		random_trytes.append('9')
		seed = [random_trytes[rand.randrange(len(random_trytes))] for x in range(81)]
		self.Seed = ''.join(seed)
 		return self
 		
 	def Key_Pair(self, directory = "UserData", Keys = "Keys", PrivKey = "priv_key.pem", PubKey = "pub_key.pem"):
 		PublKey = str(directory+"/"+Keys+"/"+PubKey)
 		PrivaKey = str(directory+"/"+Keys+"/"+PrivKey)
 		
 		#If neither of the files are present we generate the public and private keys
 		if not (os.path.isfile(PrivaKey) and os.path.isfile(PublKey)):
 			#Generate them here 
			pair = RSA.generate(2048)
			self.PrivateKey = pair.exportKey(format = 'PEM', passphrase = self.password)
			self.PublicKey = pair.publickey().exportKey(format = 'PEM')
			
			#Now we write both keys to separate files
			Writing_And_Reading().Writing(PrivaKey, self.PrivateKey)
			Writing_And_Reading().Writing(PublKey, self.PublicKey)

		else:
			Priv = Writing_And_Reading().Reading(PrivaKey)	
   			self.PrivateKey = RSA.importKey(Priv, passphrase = self.password)
   			Data = Writing_And_Reading().Reading(PublKey)
   			self.PublicKey = RSA.importKey(Data.replace("\\n","\n")).exportKey()
   			
		return self
	
	def Secret_Key(self):
		self.SecretKey = os.urandom(64)
		return self
 	
	
class Writing_And_Reading:
	def __init__(self):
		pass
		
	def Writing(self, directory, data):
		f = open(directory, "wb")
		f.write(data)
		f.close()
		
	def Reading(self, directory):
		with open(directory) as f:
			data = f.read()
		return data

class Transform:
	def __init__(self):
		self.default = 256
		self.identifier = "////"
	def normalise(self,plaintext):
		normaltext = str(plaintext) + (self.default - len(plaintext) - len(self.identifier)) * str(' ') + str(self.identifier)
		return normaltext

	def split(self,input):
		return [input[start:start+self.default] for start in range(0, len(input), self.default)]

class IOTA_Module:
	def __init__(self, server = "https://cryptoiota.win:14625",Password = ""):
		self.Seed = User_Module(password = Password).Seed
		self.api = Iota(RoutingWrapper(str(server)).add_route('attachToTangle', 'http://localhost:14265'), seed = self.Seed)
	
	def Sending(self, ReceiverAddress, Message):
		text_transfer = TryteString.from_string(str(message))
		#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived.
		txn_2 = ProposedTransaction(address = Address(receiver_address), message = text_transfer, value = 0)
		#Now create a new bundle (i.e. propose a bundle)
		bundle = ProposedBundle()
		#Add the transaction "txn_2" to the bundle. We can also add several addresses for receiving but we get to that later.
		bundle.add_transaction(txn_2)
		#Send the transaction. the variable "depth" refers to the number of previous transactions being considered.
		bundle.finalize()
		coded = bundle.as_tryte_strings()
		send = self.api.send_trytes(trytes = coded, depth = 4)
	
	def Receive(self):
		#We pull the transaction history of the account (using the seed)
		mess = self.api.get_account_data(start = 0)
		
		#Decompose the Bundle into components
		bundle = mess.get('bundles')
		Message = []
		for i in bundle:
			message_rec = i.get_messages(errors='drop')
			message=str(message_rec)
			#This cleans the string of the receiving side.
			Message.append(message.lstrip("[u'").rstrip(" ']"))
		self.Messages = Message
		self.LatestMessage = Message[len(bundle)-1]

	def generate_address(self):
		generate = self.api.get_new_addresses()
		Address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")
		self.Address
	


User = User_Module(password = "lol")
print(User.PrivateKey, User.PublicKey, User.Seed)