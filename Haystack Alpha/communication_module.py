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

#This class is responsible for the encryption side of things
class Encryption:
	def __init__(self, PlainText = "", PubKey = "", ReceiverAddress = "", CharLib = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= ', password = "", bounce = 1):

		#Here we set the attributes of the class
		self.PlainText = PlainText
		self.PubKey = PubKey
		self.CharLib = CharLib
		self.Password = password
		self.ReceiverAddress = ReceiverAddress
		self.bounce = 1

	def Encrypt(self):
		#First statement is the symmetric encryption
		if str(self.PubKey) == "":
			cipher = pyffx.String(str(self.Password), alphabet = str(self.CharLib) , length=len(str(self.PlainText)))

		#Asymetric encryption
		else:
			cipher = PKCS1_OAEP.new(self.PubKey)				
		self.CipherText = cipher.encrypt(str(self.PlainText))
		return self		

	def Message_Signature(self):
		digest = SHA256.new()
		digest.update(self.Normal)
		signer = PKCS1_v1_5.new(Generators(Pass = self.Password).Key_Pair().PrivateKey)
		self.Signature = signer.sign(digest)
		return self	

	def Prepare_Needle(self):
		self.Normal = Transform().normalise(self.PlainText)
		Signed = self.Message_Signature().Signature
		self.Needle = str(self.Normal)+str(b64encode(Signed))
		return self
	
	def Lock_And_Load(self):
		needle = self.Prepare_Needle().Needle

		#Generate a list of random addresses which are the trajectory of a message
		Trajectory = Generators(bounce = self.bounce).Path_Finder().Address
		TrajKeys = Dynamic_Ledger(FindAddress = Trajectory).Key_Finder().FoundKey

		#Generate a random index to add the recipent in the trajectory
		Insertion = int(random.randrange(0,int(self.bounce),1))
		Trajectory[int(Insertion)] = self.ReceiverAddress
		TrajKeys[int(Insertion)] = Dynamic_Ledger(FindAddress = [self.ReceiverAddress]).Key_Finder().FoundKey[0]
		metadata = []

		for i in range(int(self.bounce)-1, Insertion, -1):
			if i == int(self.bounce-1):
				bounce_address = '0' * 81
			else:
				bounce_address = Trajectory[i+1]
			self.PubKey = TrajKeys[i]
			self.PlainText = str(bounce_address)+str(self.PubKey)
			encoded_bouncedata = self.Encrypt().CipherText
			metadata.append(encoded_bouncedata)

		for i in range (int(Insertion), -1, -1):
			self.Password = Generators().Secret_Key().SecretKey
			self.PlainText = needle
			self.PubKey = ""
			needle = self.Encrypt().CipherText
			if i == int(self.bounce)-1:
				bounce_address = '0'*81
			else:
				bounce_address = Trajectory[i+1]

			self.PubKey = TrajKeys[i]
			self.PlainText = str(bounce_address) + str(self.Password)
			encoded_bouncedata = self.Encrypt().CipherText
			metadata.append(encoded_bouncedata)

		random.shuffle(metadata)
		message_data = ''
		for i in range(0, len(metadata)):
			message_data = str(message_data) + str(metadata[i]) + '##:##'
		self.MessageLocked = str(needle) + '##Begin#Metadata##' + str(message_data)
		self.FirstAddress = Trajectory[0]
		return self


class Decryption:
	def __init__(self, Password ="", CipherText = "", CharLib = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= ', Default_Size = 256):
		self.Default_Size = Default_Size
		self.CipherText = CipherText
		self.CharLib = CharLib
		self.Password = Password
		self.PrivateKey = Generators(Pass = Password).Key_Pair().PrivateKey
		self.fractal = self.CipherText
		self.identifier = '////'

	def Decrypt(self):
		if self.Password != "":
			try:
				cipher = PKCS1_OAEP.new(self.PrivateKey)
				self.DecryptedText = cipher.decrypt(str(self.fractal))
			except ValueError:
				self.DecryptedText = ""
				pass
		else:
			self.DecryptedText = pyffx.String(str(self.SecretKey), alphabet=str(self.CharLib), length=len(str(self.fractal))).decrypt(str(self.fractal))
		return self

	def Unlock(self):
		Cipher = self.CipherText[:600]
		metadata = self.CipherText[618:].split("##:##")
		metadata.remove('')
		decoded_data = ''
		
		for i in range(len(metadata)):
			try:
				self.fractal = metadata[i]
				decoded_data = self.Decrypt().DecryptedText
			except:
				pass
			try:
				bounce_address = decoded_data[:81]
			except:
				sys.exit(1)

		self.SecretKey = decoded_data[81:]
		self.Password = ""
		self.fractal = Cipher
		self.Status = ""
		needle = self.Decrypt().DecryptedText
		if needle[int(self.Default_Size - len(self.identifier)):int(self.Default_Size)] == str(self.identifier):
			self.Message = str(needle[:int(int(self.Default_Size) - len(self.identifier))])
		else:
			self.Status = 'Message is still locked!'
		if bounce_address == '0'*81:
			self.Status = 'Message terminated.'
		else:
			self.Status = 'Bouncing...'
		self.DecryptedText = needle
		self.Verification = self.Verify_Needle().NeedleVerified
		return self

	def Verify_Needle(self):
		self.Text = self.DecryptedText[:int(self.Default_Size)]
		Addresses_PubKey = Dynamic_Ledger().Scan_Address_Pool().Addresses
		self.Signature = b64decode(self.DecryptedText[int(self.Default_Size):])
		self.NeedleVerified = []
		for i in Addresses_PubKey:
			self.PublicKey = i[1].replace("\\n","\n")
		try:
			self.Signature_Verification().Verified
			self.NeedleVerified.append("From Address: '{}'".format(i[0]))
		except:
			self.NeedleVerified.append("Authentication failed.")
		return self

	def Signature_Verification(self):
		digest = SHA256.new()
		digest.update(self.Text)
		verifier = PKCS1_v1_5.new(RSA.importKey(self.PublicKey))
		self.Verified = verifier.verify(digest, self.Signature)
		return self

class User_Module:
	#initializes the class by building the directory
	def __init__(self, Server = "https://cryptoiota.win:14625", directory = "UserData", SeedFile = "Seed_Key.txt", RSA = "Keys", password = "", PublicSeed = "Public_Seed.txt", UsePublicSeed = "", UserAddress = "Public_Address.txt"):
	
		if not os.path.exists(str(directory+"/"+RSA)):
			try:
				os.makedirs(directory)
			except OSError:
				pass
				
			os.makedirs(str(directory+"/"+RSA))
		
		if not os.path.isfile(str(directory+"/"+PublicSeed)):
			if UsePublicSeed == "":
				self.PublicSeed = Generators().Seed_Generator().Seed
			else:
				self.PublicSeed = UsePublicSeed

			Writing_And_Reading().Writing(str(directory+"/"+PublicSeed), self.PublicSeed)

		Data = Writing_And_Reading().Reading(str(directory+"/"+PublicSeed)).split("\n")
		self.PublicSeed = Data[int(len(Data) -1)]

		if password != "":
			self.PrivateKey = Generators(Pass = password).Key_Pair().PrivateKey
			self.PublicKey = Generators(Pass = password).Key_Pair().PublicKey
		
		if not os.path.isfile(str(directory+"/"+SeedFile)):
			self.PrivateKey = Generators(PublicKey = self.PublicKey).Private_Seed(directory = str(directory+"/"+SeedFile)).PrivateKey	
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
			self.PrivateSeed = Decryption(CipherText = EncodedSeed, Password = password).Decrypt().DecryptedText
	def __call__(self):
		pass



class Generators:
	#Generates a random seed
	def __init__(self, Pass = "", bounce = 1, PublicKey = []):
		self.password = Pass
		self.beta = bounce
		self.Address = []
		self.PublicKey = PublicKey

	def Seed_Generator(self):
		rand = SystemRandom()
		random_trytes = [i for i in map(chr, range(65,91))]
		random_trytes.append('9')
		seed = [random_trytes[rand.randrange(len(random_trytes))] for x in range(81)]
		self.Seed = ''.join(seed)
		return self
		
 	def Private_Seed(self, directory = ""):
 		self.PrivateKey = self.Seed_Generator().Seed
 		EncodedSeed = Encryption(PlainText = str(self.PrivateKey), PubKey = RSA.importKey(self.Key_Pair().PublicKey)).Encrypt().CipherText
 		Writing_And_Reading().Writing(directory, EncodedSeed)
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
			try:	
   				self.PrivateKey = RSA.importKey(Priv, passphrase = self.password)
   				self.PublicKey = RSA.importKey(Writing_And_Reading().Reading(PublKey)).exportKey()
   			except ValueError:
   				self.PrivateKey = ""
   		return self

	def Secret_Key(self):
		self.SecretKey = os.urandom(64)
		return self
	
	def Path_Finder(self):
		for i in range(int(self.beta)):
			self.Address.append(Dynamic_Ledger().Random_Bounce().RandomAddress)
			self.PublicKey.append(Dynamic_Ledger().Random_Bounce().RandomPublicKey)
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
	def ReadingLine(self, directory, setting = "r"):
		data = []
		for i in open(directory, setting):
			data.append(i)
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
		self.Genesis = 1518435400
		self.BlockTime = 3600
		self.Block = 0
		self.directory = "UserData"
		self.Public = "Public_Address_Pool.txt"

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
		generate = self.api.get_new_addresses(index = int(self.Block))
		self.Address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")		
		return self
	
	def Get_Public_Addresses(self):
		block = self.Current_Block().Block
		Transfers = self.api.get_transfers(start = int(block), stop = int(block +1))
		Bundles = Transfers.get("bundles")
		Times = []
		Addresses = []
		for i in Bundles:
			public_addresses = str(i.get_messages()).strip("[u'").strip("']")
			Addresses.append(public_addresses)
			for x in i:
				TimeStamp = x.attachment_timestamp
				Times.append(TimeStamp)

		unique_addresses = []
		unique_times = []
		x = 0
		for i in Addresses:
			if i not in unique_addresses:
				if i != "":
					unique_addresses.append(i)
					unique_times.append(Times[0])
					x = x+1
		final_addresses = []
		for i in range(len(Addresses)):
			if int(unique_times[i] + 60) >= int(self.Genesis + self.BlockTime*block) and int(unique_times[i] - 60) <= int(self.Genesis + self.BlockTime*block + self.BlockTime):
				final_addresses.append(unique_addresses[i])

		file = open(str(self.directory+"/"+self.Public),"w")
		for i in unique_addresses:
			file.write(str(i))
			file.write(str("\n"))
		file.close()

		self.TimeStamps = Times
		return self
	
	def Current_Block(self):
    	decimal_block = (time.time() - int(self.Genesis)) / self.BlockTime
    	self.Block = int(math.ceil(decimal_block))-1
    	return self

##### =====================Add to this module ==========================#
def publish_address(secret_code):
    key = read_public_key().exportKey().replace('\n', '.').replace('\r', ',')
    seed_key = read_seed_key(str(secret_code))
    public_address = generate_address(seed_key, 0) #this will need to be fixed to generate new public addresses when inbox is full
    block = current_block()
    active_ledger = generate_address(public_seed, int(block))
    address_pair = str(public_address) + str(key) + '\n'
    send(active_ledger, address_pair, str(secret_code))

##### ====================================================================#






##########Not sure where this is being used. 
	def active_ledger(self):
    	self.Block = self.Current_Block()
    	Generate_Address()


########## Old Definition of Public Addresses. This will be deleted later once testing of new implementation is complete
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
	def __init__(self, directory = "UserData", Contact = "Contacts.txt", Public = "Public_Address_Pool.txt", PubSeed = "Public_Seed.txt", Server = "https://cryptoiota.win:14625",Password = "", max_address_pool = 2, FindAddress = ""):

		self.PublicSeed = User_Module().PublicSeed 
		self.FindAddress = FindAddress
		self.directory = directory
		self.Public = Public
		self.PubSeed = PubSeed
		self.Server = Server
		self.Password = Password
		self.max_address_pool = max_address_pool
		self.Seed = []
		self.FoundKey = []
		self.Contact = Contact

##### Contacts #######
	def Add_Contact(self, Name, Address):
		found = "No"
		Find = self.Scan_Address_Pool().Addresses
		for i in Find:
			if i[0] == Address:
				key = i[1]
		Contacts = Writing_And_Reading().ReadingLine(directory = str(self.directory+ "/" + self.Contact), setting = "r+b")
		for i in Contacts:
			if i == key:
				found = "Yes"
		if found == "No":
			string = str(name + "###" + key + "\n")
			Writing_And_Reading().Writing(directory = str(self.directory+ "/" + self.Contact), data = string, setting = "a")

	def Find_Contact(self, name):
		Contacts = Writing_And_Reading().ReadingLine(directory = str(self.directory+ "/" + self.Contact))
		for i in range(len(Contacts)):
			Seperated = i.split("###")
			if Seperated[0] == name:
				self.FindAddress = Seperated[1]
				self.RSA = self.Key_Finder().FoundKey


	def Scan_Address_Pool(self):
		Address_PublicKey = []
		Entry = Writing_And_Reading().ReadingLine(directory = str(self.directory+"/"+self.Public))
		for i in Entry:
			if "#New_Seed#" in i:
				self.Seed.append(i)
			else:
				Entries = i.split("###")
				Address = Entries[0]
				PublicKey = Entries[1]
								
				Combine = [Address,PublicKey]
				Address_PublicKey.append(Combine)
		self.Addresses = Address_PublicKey
		return self

	def Dynamic_Ledger_Start(self):
		while True:
			IOTA_Module(server = self.Server, Seed = self.PublicSeed).Public_Addresses()
			self.Scan_Address_Pool()
			if len(self.Seed) >=1:
				print("self.Seed")
				self.PublicSeed = self.Seed[0].replace("#New_Seed#","").rstrip()
				Writing_And_Reading().Writing(directory = str(self.directory+"/"+self.PubSeed), data = str("\n"+self.PublicSeed), setting = "a")
				PublicAddress = IOTA_Module(Seed = self.PublicSeed).Generate_Address().Address.rstrip()
				IOTA_Module(server = self.Server).Sending(ReceiverAddress = PublicAddress, Message = str(User_Module().PublicLedgerAddress+"###"+User_Module(password = self.Password).PublicKey))

			#Count the number of addresses within the Public Seed
			print(self.max_address_pool, len(self.Addresses))
			if (int(self.max_address_pool) <= len(self.Addresses) and len(self.Seed) == 0):
				print("Generate new Pool")
				#Generate a new public seed and send it into the current public ledger
				self.PublicSeed = Generators().Seed_Generator().Seed
				#Get old address of old ledger and send new Public Seed
				PublicAddress = IOTA_Module().Generate_Address().Address
				IOTA_Module(server = self.Server).Sending(ReceiverAddress = PublicAddress, Message = str("#New_Seed#"+self.PublicSeed))
			
				#Now we send our public address into the new public ledger 
				NewPublicSeedAddress = IOTA_Module(server = self.Server, Seed = self.PublicSeed).Generate_Address().Address
				ToPublish = str(User_Module().PublicLedgerAddress+"###"+User_Module(password = self.Password).PublicKey)
				PublicAddressOnLedger = IOTA_Module(server = self.Server).Sending(ReceiverAddress = NewPublicSeedAddress, Message = ToPublish)

	def Random_Bounce(self):
		self.Scan_Address_Pool()
		index = random.randrange(0,len(self.Addresses))
		RandomContent = self.Addresses[int(index)-1]
		self.RandomAddress = RandomContent[0]
		self.RandomPublicKey = RandomContent[1]
		return self

	def Key_Finder(self):
		self.Scan_Address_Pool()
		try:
			for i in self.FindAddress:
				for j in self.Addresses:
					if str(i) == str(j[0]):
						self.FoundKey.append(RSA.importKey(str(j[1]).replace('\\n','\n')))
		except ValueError:
			self.FoundKey.append(str("Address: " + i + " not found!"))
		return self

class Background:

	#Example use case:
	#Background(function = Example().ExampleFunction, arguments = str("{'test': 3}")).Run()

	def __init__(self, function, arguments = "()"):
		self.Variable = ""
		self.Function = function
		self.Arg = arguments

	def Run(self):
		Pool = ThreadPool(processes = 1)
		Start = Pool.apply_async(self.Function, eval(self.Arg))



if __name__ == "__main__":
	#Here we start the program and initialize the user profile
	PublicSeed = "XHWUWMFFOVOXHYHOPNM9KUSHPABPVLXQUBDLAWJSOURWYQMKQATAELXIVRKWY9YGDYCCSKJTFRRDSWFLA"
	Password = "Hello World"
	server = "http://localhost:14265"


	#Here we generate the user files or check if they are present
	User_Module(Server = server, password = Password, UsePublicSeed = PublicSeed)

	Dynamic_Ledger(Server = server, Password = Password, max_address_pool = 4).Dynamic_Ledger_Start()
	pass