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

######## Configuration  ###########
class Configuration:
	def __init__(self):
		self.Server = "http://cryptoiota.win:14265"
		self.Password = "Hello World"
		self.PublicSeed = "TEAWYYNAY9BBFR9RH9JGHSSAHYJGVYACUBBNBDJLWAATRYUZCXHCUNIPXOGXI9BBHKSHDFEAJOVZDLUWV"
		self.Charlib = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= '
		self.Default_Size = 256
		self.Root = "UserData"
		self.RSA = "Keys"
		self.PrivateSeedFile = "Private_Seed.txt"
		self.PublicSeedFile = "Public_Seed.txt"
		self.UserAddresses = "Public_Address.txt"
		self.PrivateKeyFile = "PrivateKeyFile.pem"
		self.PublicKeyFile = "PublicKeyFile.pem"
		self.Identifier = "////"
		self.Genesis = 362400
		self.BlockStep = 200

		##### Directories #####
		self.PrivateKeyDir = str(self.Root+"/"+self.RSA+"/"+self.PrivateKeyFile)
		self.PublicKeyDir = str(self.Root+"/"+self.RSA+"/"+self.PublicKeyFile)
		self.PrivateSeedDir = str(self.Root+"/"+self.PrivateSeedFile)
		self.AddressPool = str(self.Root+"/"+self.UserAddresses)

######### Base Classes ###########
class IOTA_Module(Configuration):
	def __init__(self, Seed, Server = "http://localhost:14265"):
		self.api = Iota(RoutingWrapper(str(Server)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed)

	def Sending(self, ReceiverAddress, Message):
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

	def Receive(self):
		#We pull the transaction history of the account (using the seed)
		mess = self.api.get_account_data(start = 0)
		
		#Decompose the Bundle into components
		bundle = mess.get('bundles')
		Message = []
		AssociatedMessages = []
		for i in bundle:
			message = str(i.get_messages()).strip("[u'").strip("']")

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

	def LatestMileStone(self):
		Node = self.api.get_node_info()
		self.MileStone = Node.get("latestMilestoneIndex")
		return self

	def AssociatedMessages(self):
		data = self.api.get_account_data(start = 0)
		bundle = data.get('bundles')
		self.PublicLedger = []
		if bundle != []:
			for i in bundle:
				Entry = str(i.get_messages()).strip("[u'").strip("']")
				json = i.as_json_compatible()
				dictionary = eval(str(json))
				AssociatedAddress = str(dictionary[0].get('address'))
				Combine = [Entry, AssociatedAddress]
				print(Combine)
				self.PublicLedger.append(Combine)
		return self

class Generators(Configuration, IOTA_Module):

	def Seed_Generator(self):
		random_trytes = [i for i in map(chr, range(65,91))]
		random_trytes.append('9')
		seed = [random_trytes[SystemRandom().randrange(len(random_trytes))] for x in range(81)]
		self.Seed = ''.join(seed)
		return self
	
	def Key_Pair(self):
		pair = RSA.generate(2048)
		self.PrivateKey = pair.exportKey(format = "PEM", passphrase = self.Password)
		self.PublicKey = pair.publickey().exportKey(format = 'PEM')
		return self


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
			ClientSeed = Generators().Seed_Generator().Seed
			Ciphertext = Encryption().AsymmetricEncryption(PlainText = ClientSeed, Publickey = str(keys.PublicKey))
			Tools().Writing(directory = self.PrivateSeedDir, data = Ciphertext)
			Tools().Writing(directory = self.PrivateKeyDir, data = keys.PrivateKey)
			Tools().Writing(directory = self.PublicKeyDir, data = keys.PublicKey)


class User_Profile(Configuration):

	def Client(self):
		CipherPrivate = Tools().ReadingLine(directory = self.PrivateKeyDir)
		Public = Tools().ReadingLine(directory = self.PublicKeyDir)

		self.PrivateKey = RSA.importKey(Tools().List_To_String(CipherPrivate), passphrase = self.Password)
		self.ClientPublicKey = RSA.importKey(Tools().List_To_String(Public)).exportKey()
		self.PrivateSeed = Decryption().AsymmetricDecryption(CipherText = Tools().List_To_String(List = Tools().ReadingLine(directory = self.PrivateSeedDir)), PrivateKey = self.PrivateKey).DecryptedText
		self.ClientAddress = IOTA_Module(Seed = self.PrivateSeed, Server = self.Server).Generate_Address().Address
		return self

	def Contacts(self, firstname = "", lastname = "", address = "", publickey = "", publicseed = ""):
		self.FirstName = firstname
		self.LastName = lastname
		self.Address = address
		self.PublicKey = publickey
		self.PublicSeed = publicseed


########## Other Tools #########
class Tools(Configuration): 

	def Writing(self, directory, data, setting = "wb"):
		f = open(directory, setting)
		f.write(data)
		f.close()

	def ReadingLine(self, directory, setting = "r"):
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


######## Cryptography #########
class Encryption(Configuration):

	def AsymmetricEncryption(self, PlainText, Publickey):
		cipher = PKCS1_OAEP.new(RSA.importKey(Publickey))
		return cipher.encrypt(str(PlainText))

	def SymmetricEncryption(self, PlainText, SymCode):
		return pyffx.String(str(SymCode), alphabet = str(self.CharLib) , length=len(str(PlainText))).encode("hex")

	def MessageSignature(self, ToSign):
		digest = SHA256.new()
		digest.update(ToSign)
		Signer = PKCS1_v1_5.new(User_Profile().Client().PrivateKey)
		self.Signature = Signer.sign(digest)
		return self

class Decryption(Configuration, User_Profile):

	def AsymmetricDecryption(self, CipherText, PrivateKey):
		
		cipher = PKCS1_OAEP.new(PrivateKey)
		try:
			self.DecryptedText = cipher.decrypt(str(CipherText))
		except ValueError:
			self.DecryptedText = "Failed"
		return self

	def SymmetricDecryption(self, CipherText, SymCode):
		self.DecryptedText = pyffx.String(str(SymCode), alphabet=str(self.CharLib), length=len(str(CipherText.decode("hex")))).decrypt(str(CipherText.decode("hex")))
		return self

	def SignatureVerification(self, ToVerify, PublicKey, Signature):
		digest = SHA256.new()
		digest.update(ToVerify)
		Verifier = PKCS1_v1_5.nsw(RSA.importKey(PublicKey))
		self.Verified = Verifier.verify(digest, Signature)
		return self

class Message(Encryption, Decryption, User_Profile, Tools):

	def ToProcess(self, PlainText):
		NormalizedSigned = self.NormalizeSign(PlainText = PlainText).Normal_Signed
		print(NormalizedSigned)


	def NormalizeSign(self, PlainText):
		Normal = self.Normalize(string = PlainText)
		Signature = self.MessageSignature(ToSign = Normal).Signature
		self.Normal_Signed = str(Normal) + str(b64encode(Signature))
		return self

class Dynamic_Ledger(Configuration, User_Profile):

	def __init__(self):
		User_Profile.__init__(self)
		self.PublicIOTA = IOTA_Module(Seed = self.PublicSeed)
		self.PrivateIOTA = IOTA_Module(Seed = self.Client().PrivateSeed)
		self.ToPublish = str(self.Client().ClientAddress+"###"+str(self.Client().ClientPublicKey))

	def MiletoneTrack(self):
		#Check the current milestone
		Current = self.PublicIOTA.LatestMileStone().MileStone

		#Calculate current Block and use as index for current address
		Block = float((Current - self.Genesis)/float(self.BlockStep))
		CurrentAddress = self.PublicIOTA.Generate_Address(Index = math.trunc(Block)).Address

		self.PublicPool(Check = "Yes", BlockAddress = CurrentAddress)
		print(self.Present)
		
		#Check if nunber is integer. If yes client needs to send to new address
		NewBlock = Block.is_integer()

		#Get new address public ledger block address
		if (NewBlock is True and self.Present == "False") or self.Present == "False":
			print("Changed Pool")
			self.PrivateIOTA.Sending(ReceiverAddress = CurrentAddress, Message = self.ToPublish)

	def PublicPool(self, BlockAddress, Check = "No"):
		Entries = self.PublicIOTA.AssociatedMessages().PublicLedger
		self.Pool = []
		self.Present = "False"
		for i in range(len(Entries)):
			Clients = Entries[i][0]
			AddressBlock = Entries[i][1]
			if AddressBlock == BlockAddress:
				if Clients not in self.Pool:
					self.Pool.append(Clients)

				if Check != "No":
					if str(Clients).replace("\\n","\n") == self.ToPublish:
						self.Present = "True"

		#Now Write the pool to file
#		if self.Pool != []:
#			Tools().Writing(directory = self.AddressPool, data = self.Pool)
		return self


function = "DynamicLedger"

if function == "Build":
	#Generate the dir and build the files
	Initialization().Build_Directory()
	Initialization().Build_Files()
	x =User_Profile() 
	x.Client()
	passed = x.Check().Checked
	print(passed)


if function == "Encrypt_Decrypt":
	Text = "Hello there"
	Message().To_Process(PlainText = Text)
	#Prepare the needle and encrypt it

if function == "IOTA":
	Test = "Hello World"
	x = IOTA_Module(Seed = "WCGOWTHOWPC9KYYDLOEDDZMUHPWVASCWPTX9PZEPWWNKNNEETCPZISMZTM99GNRCZQ9GGOBIBKNYNSPAS", Server = "http://node.lukaseder.de:14265")
	x.Sending(ReceiverAddress = "NPBXSOXDPLXSCSZIVQCJBHPLJONYBZEASZHDXWPYDLBXXTH9HORYWTDZEXZODIHGF9QBIB9OZTKFMFUVDGBAHFYXPD", Message = Test)
	x.Receive()

if function == "DynamicLedger":
	for i in range(10):
		IOTA_Module(Seed = Configuration().PublicSeed)
		Dynamic_Ledger().MiletoneTrack()
