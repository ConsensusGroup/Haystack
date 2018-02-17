#Iota library
from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.crypto.addresses import AddressGenerator
from iota.adapter.wrappers import RoutingWrapper
from iota import *

#Encryption
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



#Secret code = Password



#This class is responsible for the encryption side of things
class Encryption:
	def __init__(self, PlainText = "", PubKey = "", CharLib = ".ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= ", password = ""):
		self.PlainText = PlainText
		self.PubKey = PubKey
		self.CharLib = CharLib
		self.Password = password

	def Encrypt(self):
		#First statement is the symmetric encryption 
		if self.PubKey == "":
			SecretKey = Generators().Secret_Key().SecretKey
			cipher = pyffx.String(SecretKey, alphabet = self.CharLib , length=len(str(self.PlainText)))
		#Asymetric encryption
		else:
			cipher = PKCS1_OAEP.new(RSA.importKey(self.PubKey))				
		self.CipherText = cipher.encrypt(self.PlainText)
		return self		

	def Message_Signature(self):
		digest = SHA256.new()
		digest.update(self.PlainText)
		signer = PKCS1_v1_5.new(User_Module(password = self.Password).PrivateKey)
		Signature = signer.sign(digest)
		self.Signature
	
	def Prepare_Needle(self):
		Signed = self.Message_Signature().Signature
		Normalize = Transform.normalise(self.PlainText)
		self.Needle = str(Normalize)+str(b64encode(Signed))
		
class Decryption:
	def __init__(self, Password ="", CipherText = "", CharLib = ".ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= ", Signature = "", PublicKey = "", Default_Size = 256):
		self.Default_Size = Default_Size
		self.PublicKey = PublicKey
		#SecretKey = Generators().Secret_Key().SecretKey
		if Password == "":
			cipher = pyffx.String(SecretKey, alphabet = CharLib, length = len(str(CipherText)))
		else:
			PrivKey = Generators(Pass = Password).Key_Pair().PrivateKey
			cipher = PKCS1_OAEP.new(PrivKey)
		self.DecryptedText = cipher.decrypt(CipherText)
		
		if (Signature != "" and PublicKey != ""):
			digest = SHA256.new()
			digest.update(self.DecryptedText)
			verifier = PKCS1_v1_5.new(public_key)
			verified = verifier.verify(digest, Signature)
			assert verified, "Signature verfication failed"
			self.Verification = verified
	def Verify_Needle(self):
		PlainText = self.DecryptedText[:int(self.Default_Size)]
		try:
			sig = b64decode(self.DecryptedText[int(self.Default_Size):])
			verification = verify_signature(PlainText, sig, self.PublicKey)
			self.NeedleVerified = verification
		except:
			self.NeedleVerified = "Authentication failed."

class User_Module:
	#initializes the class by building the directory
	def __init__(self, Server = "https://cryptoiota.win:14625", directory = "UserData", SeedFile = "Seed_Key.txt", RSA = "Keys", password = "", PublicSeed = "Public_Seed.txt", UserAddress = "Public_Address.txt"):

		if not os.path.exists(str(directory+"/"+RSA)):
			try:
				os.makedirs(directory)
			except OSError:
				pass
				
			os.makedirs(str(directory+"/"+RSA))
		
		if not os.path.isfile(str(directory+"/"+PublicSeed)):
			self.PublicSeed = Generators().Seed_Generator().Seed
			Writing_And_Reading().Writing(str(directory+"/"+PublicSeed), self.PublicSeed)


		Data = Writing_And_Reading().Reading(str(directory+"/"+PublicSeed)).split("\n")
		self.PublicSeed = Data[int(len(Data) -1)]

		if password != "":
			self.PrivateKey = Generators(Pass = password).Key_Pair().PrivateKey
			self.PublicKey = Generators(Pass = password).Key_Pair().PublicKey
		
		if not os.path.isfile(str(directory+"/"+SeedFile)):
			self.PrivateSeed = Generators().Seed_Generator().Seed
			EncodedSeed = Encryption(PlainText = self.PrivateSeed, PubKey = self.PublicKey).Encrypt().CipherText	
			Writing_And_Reading().Writing(str(directory+"/"+SeedFile), EncodedSeed)

			SendToLedger = IOTA_Module(server = Server).Generate_Address().Address
			self.PublicLedgerAddress = IOTA_Module(server = Server, Password = password).Generate_Address().Address

			Writing_And_Reading().Writing(str(directory+"/"+UserAddress), data = self.PublicLedgerAddress)
			StringToSend = str(self.PublicLedgerAddress+"###"+self.PublicKey)
			IOTA_Module(server = Server, Password = password).Sending(ReceiverAddress = SendToLedger, Message = StringToSend)	
		
			#Verify that the address+publickey are on the ledger
			IsThere = "No"
			while str(IsThere) == "No":
				try:
					for i in IOTA_Module(server = Server, Seed = self.PublicSeed).Receive().Messages:	
						temp = str(i).replace("\\n","\n")
						if str(temp) == str(StringToSend):
							IsThere = "Yes"

				except BadApiResponse:
					pass
		
		if os.path.isfile(str(directory+"/"+UserAddress)):
			self.PublicLedgerAddress = Writing_And_Reading().Reading(str(directory+"/"+UserAddress))

		if password != "":
			EncodedSeed = Writing_And_Reading().Reading(str(directory+"/"+SeedFile))
			self.PrivateSeed = Decryption(CipherText = EncodedSeed, Password = password).DecryptedText
	
		
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
		
	def Writing(self, directory, data, setting = "wb"):
		f = open(directory, setting)
		f.write(data)
		f.close()
		
	def Reading(self, directory):
		with open(directory) as f:
			data = f.read()
		return data
	def ReadingLine(self,directory):
		with open(directory) as f:
			data = f.readlines()
		return data
	
class Transform:
	def __init__(self):
		self.default = 256
		self.identifier = "////"
	def normalise(self,plaintext):
		normaltext = str(plaintext) + (self.default - len(plaintext) - len(self.identifier)) * str(' ') + str(self.identifier)
		return normaltext

	def split(self,string):
		return [string[start:start+self.default] for start in range(0, len(string), self.default)]

class IOTA_Module:
	def __init__(self, server = "https://cryptoiota.win:14625", Password = "", Seed = ""):
		if str(Password) != "":
			self.Seed = User_Module(password = Password).PrivateSeed
		if Seed != "":
			self.Seed = Seed
		if (Password == "" and Seed == ""):
			self.Seed = User_Module().PublicSeed		

		self.api = Iota(RoutingWrapper(str(server)).add_route('attachToTangle', 'http://localhost:14265'), seed = self.Seed)

	def Sending(self, ReceiverAddress, Message):
		text_transfer = TryteString.from_string(str(Message))
		#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived.
		txn_2 = ProposedTransaction(address = Address(ReceiverAddress), message = text_transfer, value = 0)
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
			message = str(i.get_messages()).strip("[u'").strip("']")
			Message.append(message)
		self.Messages = Message
		try:
			self.LatestMessage = Message[len(bundle)-1]
		except IndexError:
			self.LatestMessage = "No Message"
		return self		
	
	def Generate_Address(self):
		generate = self.api.get_new_addresses()
		self.Address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")		
		return self
	
	def Get_TimeStamps(self):
		Transfers = self.api.get_transfers(start = 0)
		Bundles = Transfers.get("bundles")
		Times = []
		for i in Bundles:
			for x in i:
				TimeStamp = x.attachment_timestamp
				Times.append(TimeStamp)
		self.TimeStamps = Times
	
	def Public_Addresses(self, directory = "UserData", Public = "Public_Address_Pool.txt"):
		Addresses = self.Receive().Messages
		unique_addresses = []
		for i in Addresses:
			if i not in unique_addresses:
				if i != "":
					unique_addresses.append(i)

		file = open(str(directory+"/"+Public),"w")
		for i in unique_addresses:
			file.write(str(i))
			file.write(str("\n"))
		file.close()
		self.Addresses = unique_addresses	

class Dynamic_Ledger:
	def __init__(self, directory = "UserData", Public = "Public_Address_Pool.txt", PubSeed = "Public_Seed.txt", Server = "https://cryptoiota.win:14625",Password = "", max_address_pool = 2):

		IOTA_Module(server = Server).Public_Addresses()
		self.PublicSeed = User_Module().PublicSeed 
		self.Entry = Writing_And_Reading().ReadingLine(directory = str(directory+"/"+Public))
		
		Seed = []
		Address_PublicKey = []		
		for i in self.Entry:
			if "#New_Seed#" in i:
				Seed.append(i)
			else:
				Entries = i.split("###")
				Address = Entries[0]
				PublicKey = Entries[1]
								
				Combine = [Address,PublicKey]
				Address_PublicKey.append(Combine)
		self.Addresses = Address_PublicKey

		if len(Seed) >=1:
			self.PublicSeed = Seed[0].replace("#New_Seed#","").rstrip()
			print(self.PublicSeed)
			Writing_And_Reading().Writing(directory = str(directory+"/"+PubSeed), data = str("\n"+self.PublicSeed), setting = "a")
			PublicAddress = IOTA_Module(Seed = self.PublicSeed).Generate_Address().Address.rstrip()
			print(PublicAddress)
			IOTA_Module(server = Server).Sending(ReceiverAddress = PublicAddress, Message = str(User_Module().PublicLedgerAddress+"###"+User_Module(password = Password).PublicKey))
			
		
		#Count the number of addresses within the Public Seed
		if int(max_address_pool) <= len(self.Addresses):
			
			#Generate a new public seed and send it into the current public ledger
			NewPublicSeed = Generators().Seed_Generator().Seed
			#Get old address of old ledger and send new Public Seed
			PublicAddress = IOTA_Module().Generate_Address().Address
			IOTA_Module(server = Server).Sending(ReceiverAddress = PublicAddress, Message = str("#New_Seed#"+NewPublicSeed))
			
			#Now we send our public address into the new public ledger 
			NewPublicSeedAddress = IOTA_Module(server = Server, Seed = NewPublicSeed).Generate_Address().Address
			ToPublish = str(User_Module().PublicLedgerAddress+"###"+User_Module(password = Password).PublicKey)
			PublicAddressOnLedger = IOTA_Module(server = Server).Sending(ReceiverAddress = NewPublicSeedAddress, Message = ToPublish)


