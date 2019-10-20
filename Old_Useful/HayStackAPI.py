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
import time
from multiprocessing.pool import ThreadPool
import time, math

#cd Directory/iri/target
#java -jar iri-1.4.2.2.jar -p 14265

######## Configuration  ###########
class Configuration:
	def __init__(self):
		self.Server = "https://tuna.iotasalad.org:14265"
		self.Password = "Hello World"
		self.PublicSeed = "PJKEJOSPR99CK9TVRJUUDYRWZX9IPIQBRUCWOQMQSKOGEWXYOIFGKXSCSAUTKLDQYNZWMSTVRIUXCGZZQ"
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
		self.GenesisTime = 1524586927440
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

	def Splitt(self, string, size):
		return [string[start:start+size] for start in range(0, len(string), size)]

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
		self.ClientAddress = Tools().ReadLine(directory = self.PublicAddressDir)

class IOTA_Module(Configuration):

	def __init__(self, Seed, Server = "http://iotanode.host:14265"):
		Configuration.__init__(self)
		self.api = Iota(RoutingWrapper(str(Server)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed)

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
		ClientAddress = Address.strip("[u'").strip("']")
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
				for i in Entry.split('###'):
					if i == ClientAddress:
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
		self.ToPublish = str(str(self.ClientAddress)+"###"+str(self.ClientPublicKey))

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


		#Check if the current address is in the current block:
		AddressPool = self.PublicIOTA.GetAddresses(Block = self.Block, Address = str(self.ClientAddress))
		if AddressPool.Check is False:
			print "Address not found: Broadcasting to Ledger"
			LedgerEntry = str(str(self.ClientAddress).strip("[u'").strip("']") +"###"+ str(self.ClientPublicKey).encode('hex'))
			Signed = Encryption().MessageSignature(ToSign = LedgerEntry).Signature
			ToPublish = str(LedgerEntry +"|"+ Signed.encode("hex"))

			#Publish to public ledger
			self.PrivateIOTA.Send(ReceiverAddress = self.CurrentAddress, Message = str(ToPublish))

		#Output a list of available public addresses and public keys on the ledger
		self.PublicLedger = []
		for i in AddressPool.PublicLedger:
			Entry = i.split("|")
			AddressAndKeys = Entry[0].split("###")
			Signature = Entry[1].decode("hex")

			#Verify the authenticity of the users on the ledger
			Authentic = Decryption().SignatureVerification(ToVerify = Entry[0], PublicKey = AddressAndKeys[1].decode("hex"), Signature = Signature).Verified

			#Make into a list for output
			Combine = [AddressAndKeys[0], AddressAndKeys[1]]
			if Authentic == True:
				self.PublicLedger.append(Combine)

class Contacts(Encryption, Decryption, User_Profile, Tools, Configuration, Dynamic_Ledger):

	def __init__(self, Name, PublicKey):
		self.Address = self.KeyFinder(PublicKeyToFind = ReceiverPublicKey)
		self.Name = Name
		self.LastInclusionBlock = 0

	def KeyFinder(self, PublicKeyToFind):

		#grab all the transactions associated with the public ledger.
		Entries = IOTA_Module(Seed = self.PublicSeed).InboxHistory().Inbox
		self.Inclusions = []
		print "keyfinder entries:", Entries
		x = 0
		for i in Entries:
			Splitted = i[1].split("###")
			if PublicKeyToFind == Splitted[1].decode('hex'):
				if i[0] >= x:
					x = i[0]
					Address = Splitted[0]
					print "Address found:", Address
		return Address

class Messages(Encryption, Decryption, User_Profile, Tools, Configuration, Dynamic_Ledger, Contacts):

	def NormalizeAndSign(self, PlainText):
		Normal = self.Normalize(string = PlainText)
		Signature = self.MessageSignature(ToSign = Normal).Signature
		return str(Normal) + str(b64encode(Signature))

	def PathFinder(self, Length = 1):
		self.Trajectory = []
		self.Addresses = Dynamic_Ledger().UpdateLedger().PublicLedger
		for i in range(Length):
			if len(self.Addresses) == 1:
				index = 1
			else:
				index = random.randrange(1, len(self.Addresses))
			self.Trajectory.append(self.Addresses[index-1])
		return self

	def PrepareMessage(self, PlainText, ReceiverPublicKey, TrajectoryLength = 4):
		Message = self.NormalizeAndSign(PlainText = PlainText)
		Trajectory = self.PathFinder(Length = TrajectoryLength).Trajectory
		#Trajectory = []
		for i in range(0, TrajectoryLength, 1):
			Trajectory.append(['ETQNFU9WGSQTIVPLRKUXWENEUCUGARPTZIRXWZWDNAHXQZZMQWI9VQINVKWPMCWBMNKZRHESGPFZXZ9AW', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyCc7X/Exfr+/3upjKuom\nh/45Au+48Aot7S2mwU5soIEY2ASYDyU1OoWLVQPYbiXDarOlJ3Dus76H32Ec14IQ\n5HQLIZaRb2LnlmsBRaCKyPpFA3o6GnRjDb2sqDz4kjWtEybElFmiJKXbPQmla4gQ\niBUXozERNIKKoSCvXr2MowxGc4ekpdIfRHDIkH/ZJVN9hZ2DPPqQwCrJLnbaz7y3\n8WQkH/QAy9kgnannwdtxtwXLlFX3XmasAacXDSMtpSz7YyzvoVToSiZuwZ5gjUOL\ngV8jj/d6FOJQdkDXuSmL8+7zGkOuQyNhy1xwCOHVeco+47xXKQ76Staif7UAr1cc\nDQIDAQAB\n-----END PUBLIC KEY-----'])
		print "pathfinder:", Trajectory
		Address = self.KeyFinder(PublicKeyToFind = ReceiverPublicKey)
		#Address = 'ETQNFU9WGSQTIVPLRKUXWENEUCUGARPTZIRXWZWDNAHXQZZMQWI9VQINVKWPMCWBMNKZRHESGPFZXZ9AW'
		#Generate a random index to add the recipent in the trajectory
		Index = int(random.randrange(0,len(Trajectory),1))
		print "INDEX:", Index
		Trajectory[int(Index)] = [Address, ReceiverPublicKey.replace("\n","\\n")]

		metadata = []
		for i in range(int(len(Trajectory))-1, Index, -1):
			if i == int(len(Trajectory)-1):
				bounce_address = '0' * 81
			else:
				bounce_address = Trajectory[i+1][0]
			PublicKey = Trajectory[i][1]
			SecretKey = Generators().Secret_Key()
			PlainData = str(bounce_address)+str(SecretKey)
			"".join(PlainData)
			encoded_bouncedata = self.AsymmetricEncryption(PlainText = PlainData, PublicKey = PublicKey)
			metadata.append(encoded_bouncedata)

		for i in range (int(Index), -1, -1):
			SecretKey = Generators().Secret_Key()

			if i == int(len(Trajectory))-1:
				bounce_address = '0'*81
			else:
				bounce_address = Trajectory[i+1][0]
			PublicKey = Trajectory[i][1].replace('\\n', '\n')
			SecretKey = Generators().Secret_Key()
			PlainData = str(bounce_address) + str(SecretKey)
			"".join(PlainData)
			Message = self.SymmetricEncryption(PlainText = Message, SecretKey = SecretKey)
			print 'plaindata for bounce number', i, ':', PlainData
			encoded_bouncedata = self.AsymmetricEncryption(PlainText = PlainData, PublicKey = PublicKey)
			metadata.append(encoded_bouncedata)

		random.shuffle(metadata)
		message_data = ''
		for i in range(0, len(metadata)):
			message_data = str(message_data) + str(metadata[i]) + '##:##'
		splitted = Tools().Splitt(size = 200, string = message_data)
		metadata = ''
		for i in splitted:
			encrypted_bouncedata = self.AsymmetricEncryption(PlainText = str(i), PublicKey = Trajectory[0][1].replace('\\n', '\n'))
			metadata = metadata + encrypted_bouncedata.encode('hex')
		self.LockedMessage = str(Message) + '##Begin#Metadata##' + str(metadata)
		self.FirstAddress = Trajectory[0][0]
		print 'locked message:', self.LockedMessage
		print 'partitioned message:', self.LockedMessage.partition('##Begin#Metadata##')
		return self

	def UnlockMessage(self, LockedMessage):
		parts = LockedMessage.partition('##Begin#Metadata##')
		bouncedata_blocks = Tools().Splitt(size = 256, string = parts[2].decode('hex'))
		metadata = ''
		for i in bouncedata_blocks:
			decrypted_block = self.AsymmetricDecryption(CipherText = str(i), PrivateKey = User_Profile().PrivateKey)
			metadata = metadata + decrypted_block
		encoded_bouncedata = metadata.split('##:##')
		print 'decrypted metadata:', encoded_bouncedata
		for i in encoded_bouncedata:
			decoded_bouncedata = self.AsymmetricDecryption(CipherText = str(i), PrivateKey = User_Profile().PrivateKey)
			if decoded_bouncedata != 'Failed':
				bouncedata = decoded_bouncedata
			else:
				pass
		self.MetaData = metadata
		self.BounceAddress = bouncedata[:81]
		self.UnlockedMessage = self.SymmetricDecryption(CipherText = parts[0], SecretKey = bouncedata[81:])
		return self


if function == "Build":
	#Generate the dir and build the files
	Initialization().Build_Directory()
	Initialization().Build_Files()
	IOTA_Module(Seed = User_Profile().PrivateSeed).Build_Inbox()

function = "PrepareMessage"

if function == "PrepareMessage":
	#I am the receiver.
	ReceiverPublicKey = str(User_Profile().ClientPublicKey)
	Text = "Hello there How are we today my friend I am trying to implement the decryption"
	Message = Messages().PrepareMessage(PlainText = Text, ReceiverPublicKey = ReceiverPublicKey, TrajectoryLength = 4)
	Messages().UnlockMessage(LockedMessage = Message.LockedMessage)
