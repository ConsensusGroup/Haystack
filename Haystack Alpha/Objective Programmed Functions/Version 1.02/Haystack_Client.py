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
import time, math

#This python script is used for the non interactive usage of the HayStack protocol. It is used only for relaying purposes.

######### Configuration variables #########
class Configuration:
	def __init__(self):
		self.Server = "http://node04.iotatoken.nl:14265"
		self.Password = "password"
		self.PublicSeed = "TEAWYYNAY9BBFR9RH9JGHSSAHYJGVYACUBBNBDJLWAATRYUZCXHCUNIPXOGXI9BBHKSHDFEAJOVZDLUWV"
		self.Root = "UserData"

		##### PEM files #####
		self.PrivateKeyFile = "PrivateKeyFile.pem"
		self.PublicKeyFile = "PublicKeyFile.pem"
		self.Seed = "ClientSeed.txt"

		##### Directories #####
		self.PrivateKeyDir = str(self.Root + "/"+ self.PrivateKeyFile)
		self.PublicKeyDir = str(self.Root + "/" + self.PublicKeyFile)
		self.SeedDir = str(self.Root + "/" + self.Seed)

	def Credentials(self):
		User = Generators()
		self.SeedKey = User.PathBuilder(Path = self.SeedDir).Seed
		self.User_Keys = User.PathBuilder(Path = self.PrivateKeyDir)
		return self



######### Base Classes ###########
class Generators(Configuration):

	def Seed_Generator(self):
		random_trytes = [i for i in map(chr, range(65,91))]
		random_trytes.append('9')
		seed = [random_trytes[SystemRandom().randrange(len(random_trytes))] for x in range(81)]
		return ''.join(seed)

	def Key_Pair(self):
		pair = RSA.generate(2048)
		self.PrivateKey = pair.exportKey(format = "PEM", passphrase = self.Password)
		self.PublicKey = pair.publickey().exportKey(format = 'PEM')
		return self

	def Secret_Key(self):
	    return os.urandom(64)

	def PathBuilder(self, Path):
		self.BuildPath(Build = os.path.exists(Path), Path = Path)
		return self

	def BuildPath(self, Build, Path):
		if Build == False and ".pem" in Path:
			Keys = self.Key_Pair()
			Tools().Write(directory = Path, data = Keys.PrivateKey)
			Tools().Write(directory = self.PublicKeyDir, data = Keys.PublicKey)
			Build = True

		elif Build == False and ".txt" in Path:
			PublicKey = RSA.importKey(Tools().List_To_String(Tools().ReadLine(directory = self.PublicKeyDir))).exportKey()
			Tools().Write(directory = Path, data = Encryption().AsymmetricEncryption(PlainText = self.Seed_Generator(), PublicKey = PublicKey))
			Build = True

		elif Build == False:
			os.makedirs(Path)

		if Build == True and ".pem" in Path:
			self.PrivateKey = RSA.importKey(Tools().List_To_String(Tools().ReadLine(directory = self.PrivateKeyDir)), passphrase = self.Password)
			self.PublicKey = RSA.importKey(Tools().List_To_String(Tools().ReadLine(directory = self.PublicKeyDir))).exportKey()

		elif Build == True and ".txt" in Path:
			PrivateKey = RSA.importKey(Tools().List_To_String(Tools().ReadLine(directory = self.PrivateKeyDir)), passphrase = self.Password)
			self.Seed = Decryption().AsymmetricDecryption(CipherText = Tools().List_To_String(List = Tools().ReadLine(directory = self.SeedDir)), PrivateKey = PrivateKey)

		elif Build == True:
			return True

########## Tools #########
class Tools(Configuration):

	def Write(self, directory, data, setting = "wb"):
		f = open(directory, setting)
		f.write(data)
		f.close()

	def ReadLine(self, directory, setting = "r"):
		data = []
		for i in open(directory, setting):
			data.append(i)
		return data

	def List_To_String(self, List):
		return ''.join(List)

######## Cryptography #########
class Encryption(Configuration):

	def AsymmetricEncryption(self, PlainText, PublicKey):
		cipher = PKCS1_OAEP.new(RSA.importKey(PublicKey))
		return cipher.encrypt(str(PlainText))

	def MessageSignature(self, ToSign):
		digest = SHA256.new()
		digest.update(ToSign)
		Signer = PKCS1_v1_5.new(self.Credentials().User_Keys.PrivateKey)
		self.Signature = Signer.sign(digest)
		return self

class Decryption(Configuration):

	def AsymmetricDecryption(self, CipherText, PrivateKey):
		cipher = PKCS1_OAEP.new(PrivateKey)
		try:
			DecryptedText = cipher.decrypt(CipherText)
		except ValueError:
			DecryptedText = "Failed"
		return DecryptedText

	def SignatureVerification(self, ToVerify, PublicKey, Signature):
		digest = SHA256.new()
		digest.update(ToVerify)
		Verifier = PKCS1_v1_5.new(RSA.importKey(PublicKey))
		self.Verified = Verifier.verify(digest, Signature)
		return self

##### IOTA Communication module ######
class IOTA_Module(Configuration):

	def __init__(self, Seed):
		Configuration.__init__(self)
		self.api = Iota(RoutingWrapper(str(self.Server)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed)

	def Generate_Address(self, Index = 0):
		generate = self.api.get_new_addresses(index = int(Index))
		self.Address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")
		return self

	def Send(self, ReceiverAddress, Message):
		text_transfer = TryteString.from_string(Message.encode("hex"))
		txn_2 = ProposedTransaction(address = Address(ReceiverAddress), message = text_transfer, value = 0)
		bundle = ProposedBundle()
		bundle.add_transaction(txn_2)
		bundle.finalize()
		coded = bundle.as_tryte_strings()
		send = self.api.send_trytes(trytes = coded, depth = 4)

	def Receive(self, Start = 0, Stop = ""):
		#We pull the transaction history of the account (using the seed)
		if Stop == "":
			mess = self.api.get_account_data(start = Start)
		else:
			mess = self.api.get_account_data(start = Start, stop = Stop)

		#Decompose the Bundle into components
		self.JsonEntries = []
		for i in mess.get('bundles'):
			message = str(i.get_messages()).strip("[u'").strip("']").decode("hex")
			Json = str(i.as_json_compatible()[0])
			combine = [message] #[Json,message]
			self.JsonEntries.append(combine)
		return self



######### Setting up the client environment ##########
class SetupClient(Configuration):
	def __init__(self):

		#Import the config variables
		Configuration.__init__(self)

		#Check if user directory is present
		Generators().PathBuilder(Path = self.Root)

		#Check if the pem files are present and if not we generate them. 
		Generators().PathBuilder(Path = self.PrivateKeyDir)

		#Check now if the seed is present and if not generate a file. 
		Generators().PathBuilder(Path = self.SeedDir)

	def WriteToLedger(self):

		#Calling the user credentials.
		Client_Creds = self.Credentials()

		#Creating a user and public IOTA instance
		User_IOTA = IOTA_Module(Seed = Client_Creds.SeedKey)
		Public_IOTA = IOTA_Module(Seed = self.PublicSeed)

		#Generate a transaction which has the following format: [UserAddress, PublicKey] + Signature
		UserAddress = User_IOTA.Generate_Address().Address
		ToSign = str(UserAddress + "\\" + Client_Creds.User_Keys.PublicKey)

		#Here we sign the string to ensure no one can commit fraud.
		Signature = Encryption().MessageSignature(ToSign = ToSign).Signature
		ToSubmit = str(ToSign + "\\" + Signature).encode("hex")

		#Send to the ledger. 
		User_IOTA.Send(ReceiverAddress = Address, Message = ToSubmit)

	def ValidationOfLedger(self, TextFromLedger):
		RawText = TextFromLedger.decode("hex").split("\\")
		PublicAddress = RawText[0]
		PublicKey = RawText[1]
		Signature = RawText[2]

		#Here we validate the signature to ensure the address and public key are authentic
		Compare = str(PublicAddress + "\\" + PublicKey)
		Validation = Decryption().SignatureVerification(ToVerify = Compare, PublicKey = PublicKey, Signature = Signature).Verified
		if Validation == True:
			pass #Do something here 



		#print(User_IOTA.Receive().JsonEntries)


if "__main__" == __name__:
	Setup = SetupClient()
	Setup.WriteToLedger()

