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

#java -jar iri-1.4.2.3.jar -p 14265

####### Instance initilization ######
ClientPassword = "5442"
class Start:
	def __init__(self,Password):
		ClientPassword = Password
		global ClientPassword

######## Configuration  ###########
class Configuration:
	def __init__(self):
		self.Server = "http://cryptoiota.win:14265"
		self.Password = ClientPassword
		self.PublicSeed = "TEAWYYNAY9BBFR9RH9JGHSSAHYJGVYACUBBNBDJLWAATRYUZCXHCUNIPXOGXI9BBHKSHDFEAJOVZDLUWV"
		self.Charlib = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= '
		self.Default_Size = 256
		self.Root = "UserData"
		self.RSA = "Keys"
		self.PrivateSeedFile = "Private_Seed.txt"
		self.PublicSeedFile = "Public_Seed.txt"
		self.PublicAddressFile = "Public_Address.txt"
		self.AddressPoolFile = "Address_Pool.txt"
		self.PrivateKeyFile = "PrivateKeyFile.pem"
		self.PublicKeyFile = "PublicKeyFile.pem"
		self.Identifier = "////"
		self.GenesisTime = 1520726570370
		self.BlockTime = 2000000

		##### Directories #####
		self.PrivateKeyDir = str(self.Root+"/"+self.RSA+"/"+self.PrivateKeyFile)
		self.PublicKeyDir = str(self.Root+"/"+self.RSA+"/"+self.PublicKeyFile)
		self.PrivateSeedDir = str(self.Root+"/"+self.PrivateSeedFile)
		self.PublicAddressDir = str(self.Root+"/"+self.PublicAddressFile)
		self.AddressPool = str(self.Root+"/"+self.AddressPoolFile)

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

	def Normalize(self, string):
		normaltext = str(string) + (self.Default_Size - len(string) - len(self.Identifier)) * str(' ') + str(self.Identifier)
		return normaltext

	def Split(self, string):
		return [string[start:start+self.Default_Size] for start in range(0, len(string), self.Default_Size)]

	def List_To_String(self, List):
		return ''.join(List)

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

class Initialization(Configuration):

	def Build_Directory(self):
		if not os.path.exists(self.Root):
			try:
				os.makedirs(self.Root)
				os.makedirs(str(self.Root+"/"+self.RSA))
			except OSError:
				pass

	def Build_Files(self):
		x = os.path
		keys = Generators().Key_Pair()
		if not (x.isfile(self.PrivateKeyDir) or x.isfile(self.PublicKeyDir) or x.isfile(self.PrivateSeedDir)):
			ClientSeed = Generators().Seed_Generator()
			Ciphertext = Encryption().AsymmetricEncryption(PlainText = ClientSeed, PublicKey = str(keys.PublicKey))
			Tools().Write(directory = self.PrivateSeedDir, data = Ciphertext)
			Tools().Write(directory = self.PrivateKeyDir, data = keys.PrivateKey)
			Tools().Write(directory = self.PublicKeyDir, data = keys.PublicKey)

####### Connectivity and User Profile ########

class User_Profile(Configuration):

	def __init__(self):
		Configuration.__init__(self)
		CipherPrivate = Tools().ReadLine(directory = self.PrivateKeyDir)
		Public = Tools().ReadLine(directory = self.PublicKeyDir)
		self.PrivateKey = RSA.importKey(Tools().List_To_String(CipherPrivate), passphrase = self.Password)
		self.ClientPublicKey = RSA.importKey(Tools().List_To_String(Public)).exportKey()
		self.PrivateSeed = Decryption().AsymmetricDecryption(CipherText = Tools().List_To_String(List = Tools().ReadLine(directory = self.PrivateSeedDir)), PrivateKey = self.PrivateKey)

class IOTA_Module(Configuration):

	def __init__(self, Seed):
		Configuration.__init__(self)
		self.api = Iota(RoutingWrapper(str(self.Server)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed)

	def Send(self, ReceiverAddress, Message):
		text_transfer = TryteString.from_string(str(Message))
		#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived.
		txn_2 = ProposedTransaction(address = Address(ReceiverAddress), message = text_transfer, value = 0)
		#Now create a new bundle (i.e. propose a bundle)
		bundle = ProposedBundle()
		#Add the transaction "txn_2" to the bundle. We can also add several addresses for receiving but we get to that later.
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
		bundle = mess.get('bundles')
		Message = []
		self.JsonEntries = []
		for i in bundle:
			message = str(i.get_messages()).strip("[u'").strip("']")
			Json = str(i.as_json_compatible()[0])
			combine = [Json,message]
			self.JsonEntries.append(combine)
			Message.append(message)

		self.Messages = Message
		try:
			self.LatestMessage = Message[len(bundle)-1]
		except IndexError:
			self.LatestMessage = "No Message"
		return self

	def Generate_Address(self, Index = 0):
		generate = self.api.get_new_addresses(index = int(Index))
		self.Address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")
		return self

	def LatestTangleTime(self):
		Node = self.api.get_node_info()
		self.TangleTime = Node.get("time")
		return self

	def GetAddresses(self, Block, Address):
		data = self.api.get_transfers(start = Block, stop = Block +1)
		bundle = data.get('bundles')
		self.PublicLedger = []
		Conf = Configuration()
		self.Check = False
		if bundle != []:
			for i in bundle:
				Entry = str(i.get_messages()).strip("[u'").strip("']")
				json = i.as_json_compatible()
				AttachedTime = str(json[0].get('attachment_timestamp'))

				#Verify that client is in pool
				if Address in Entry:
					self.Check = True

				#Block at which message was sent to
				BlockOfAddress = float(int(AttachedTime) - Conf.GenesisTime) / float(Conf.BlockTime)

				if BlockOfAddress >= Block:
					if Entry not in self.PublicLedger:
						self.PublicLedger.append(Entry)
		return self

	def Build_Inbox(self):
		x = os.path
		Address = self.Generate_Address().Address
		if not (x.isfile(self.PublicAddressDir)):
				Tools().Write(directory = self.PublicAddressDir, data = Address)

	def InboxHistory(self):
		Entries = self.Receive(Start = 0).JsonEntries
		self.Inbox = []
		for i in Entries:
			Time = eval(i[0]).get('attachment_timestamp')
			Messages = i[1]
			Combine = [Time, Messages]
			self.Inbox.append(Combine)
		return self


######## Cryptography #########
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

class Decryption(Configuration, User_Profile):

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
		Verifier = PKCS1_v1_5.nsw(RSA.importKey(PublicKey))
		self.Verified = Verifier.verify(digest, Signature)
		return self

####### Dynamic Ledger and Haystack Protocol #######

class Dynamic_Ledger(Configuration, User_Profile, IOTA_Module):

	def __init__(self):
		User_Profile.__init__(self)
		self.PublicIOTA = IOTA_Module(Seed = self.PublicSeed)
		self.PrivateIOTA = IOTA_Module(Seed = self.PrivateSeed)

	def CalculateBlock(self, Current):
		#Calculate the current Block and use as index for current address
		Blockfloat = float((Current - self.GenesisTime) / float(self.BlockTime))
		self.Block = math.trunc(Blockfloat)
		return self

	def UpdateLedger(self):
		#Check the current time of the Tangle
		Current = self.PublicIOTA.LatestTangleTime().TangleTime

		self.CalculateBlock(Current = Current)
		self.CurrentAddress = self.PublicIOTA.Generate_Address(Index = self.Block).Address
		self.ClientAddress = self.PrivateIOTA.Generate_Address(Index = self.Block).Address

		#Check if the current address is in the current block:
		AddressPool = self.PublicIOTA.GetAddresses(Block = self.Block, Address = str(self.ClientAddress))
		if (AddressPool.Check is False):
			print("Address")
			ToPublish = str(str(self.ClientAddress) +"###"+ str(self.ClientPublicKey))
			self.PrivateIOTA.Send(ReceiverAddress = self.CurrentAddress, Message = str(ToPublish))

		#Output a list of available public addresses and public keys on the ledger
		self.PublicLedger = []
		for i in AddressPool.PublicLedger:
			Entry = i.split("###")
			Combine = [Entry[0],Entry[1]]
			self.PublicLedger.append(Combine)
		return self


class Messages(Encryption, Decryption, User_Profile, Tools, Configuration, Dynamic_Ledger):

	def NormalizeAndSign(self, PlainText):
		Normal = self.Normalize(string = PlainText)
		Signature = self.MessageSignature(ToSign = Normal).Signature
		return str(Normal) + str(b64encode(Signature))

	def PathFinder(self, Length = 1, ReceiverPublicKey = ""):
		self.Trajectory = []
		self.Addresses = Dynamic_Ledger().UpdateLedger().PublicLedger
		for i in range(Length):
			index = random.randrange(0, len(self.Addresses))
			self.Trajectory.append(self.Addresses[index-1])
		return self

	def KeyFinder(self, PublicKeyToFind):

		#grab all the transactions associated with the public ledger.
		Entries = IOTA_Module(Seed = self.PublicSeed).InboxHistory().Inbox
		self.Inclusions = []

		x = 0
		for i in Entries:
			if PublicKeyToFind in i[1].replace("\\n","\n"):
				if i[0] >= x:
					x = i[0]
					Splitted = i[1].split("###")
					self.Address = Splitted[0]
		return self

	def PrepareMessage(self, PlainText, ReceiverPublicKey, TrajectoryLength = 1):
		NormalizedSigned = self.NormalizeAndSign(PlainText = PlainText)
		Address = self.KeyFinder(PublicKeyToFind = ReceiverPublicKey)
		Trajectory = self.PathFinder(Length = TrajectoryLength, ReceiverPublicKey = ReceiverPublicKey).Trajectory

		#Generate a random index to add the recipent in the trajectory
		Index = 3#int(random.randrange(0,len(Trajectory),1))
		Trajectory[int(Index)] = [Address, ReceiverPublicKey.replace("\n","\\n")]

		metadata = []
		for i in range(int(len(Trajectory))-1, Insertion, -1):
			if i == int(len(Trajectory)-1):
				bounce_address = '0' * 81
			else:
				bounce_address = Trajectory[i+1][0]
			PublicKey = Trajectory[i][1]
			PlainData = str(bounce_address)+str(PublicKey)

			encoded_bouncedata = self.AsymmetricEncryption(PlainText = PlainData, PublicKey = PublicKey)
			metadata.append(encoded_bouncedata)
