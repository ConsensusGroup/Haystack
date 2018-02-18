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


#This class is responsible for the encryption side of things
class Encryption:
	def __init__(self, PlainText = "", PubKey = "", ReceiverAddress = "", CharLib = ".,!ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= ", password = "", bounce = 1):
		self.PlainText = PlainText
		self.PubKey = PubKey
		self.CharLib = CharLib
		self.Password = password
		self.ReceiverAddress = ReceiverAddress
		self.bounce = bounce 

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
		signer = PKCS1_v1_5.new(Generators(Pass = self.Password).Key_Pair().PrivateKey)
		self.Signature = signer.sign(digest)
		return self	

	def Prepare_Needle(self):
		Signed = self.Message_Signature().Signature
		Normalize = Transform().normalise(self.PlainText)
		self.Needle = str(Normalize)+str(b64encode(Signed))
		return self
	
	def Lock_And_Load(self):
		needle = self.Prepare_Needle().Needle
		Gen = Generators(bounce = self.bounce).Path_Finder()
		Tranjectory = Gen.Address
		TrajKeys = Gen.PublicKey
		Insertion = random.randrange(0,int(self.bounce),1)
		Tranjectory[Insertion] = self.ReceiverAddress
		TrajKeys[Insertion] = Dynamic_Ledger(FindAddress = self.ReceiverAddress).Key_Finder().FoundKey
		self.PubKey = Dynamic_Ledger(FindAddress = self.ReceiverAddress).Key_Finder().FoundKey

		metadata = []
		for i in range(int(self.bounce)-1, Insertion, -1):
			if i == int(self.bounce)-1:
				bounce_address = '0' * 81
			else:
				bounce_address = Tranjectory[i+1]
			bounce_key = TrajKeys[i]
			self.PlainText = str(bounce_address)+str(bounce_key)
			encoded_bouncedata = self.Encrypt().CipherText
			metadata.append(encoded_bouncedata)

		for i in range(Insertion, -1, -1):
			self.PubKey = ""
			self.PlainText = needle 
			needle = self.Encrypt().CipherText
			if i == int(self.bounce)-1:
				bounce_address = '0' * 81
			else:
				bounce_address = Tranjectory[i+1]
			self.PlainText = str(bounce_address) + str(Generators().Secret_Key().SecretKey)
			self.PubKey = TrajKeys[i].replace(r"\n","\n")
			encoded_bouncedata = self.Encrypt().CipherText
			metadata.append(encoded_bouncedata)
			self.PlainText = needle

		random.shuffle(metadata)
		message_data = ""
		for i in range(0, len(metadata)):
			message_data = str(message_data) + str(metadata[i]) + "##:##"
		self.MessageLocked = str(self.PlainText) + "##Begin#Metadata##" + str(message_data)
		self.FirstAddress = Tranjectory[0]
		return self


class Decryption:
	def __init__(self, Password ="", CipherText = "", CharLib = "#,!:''.\ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-=", Default_Size = 256):
		self.Default_Size = Default_Size
		self.CipherText = CipherText
		self.CharLib = CharLib
		self.Password = Password
		self.PrivateKey = Generators(Pass = Password).Key_Pair().PrivateKey
		self.fractal = self.CipherText
		self.SecretKey = Generators().Secret_Key().SecretKey
		self.identifier = '////'

	def Decrypt(self):
		if self.Password != "" and str(self.PrivateKey) != "":
			try:
				cipher = PKCS1_OAEP.new(self.PrivateKey)
				self.DecryptedText = cipher.decrypt(self.fractal)
			except ValueError:
				self.DecryptedText = ""
				pass
		else:
			self.DecryptedText = pyffx.String(self.SecretKey, alphabet = self.CharLib, length = len(str(self.fractal))).decrypt(str(self.fractal))
		return self

	def Unlock(self):
		Cipher = self.CipherText[:600]
		metadata = self.CipherText[618:].split("##:##")
		metadata.remove("")
		decoded_data = ""
		for i in metadata:
			try:
				print(i)
				self.fractal = i
				decoded_data = self.Decrypt().DecryptedText
			except:
				pass

			try:
				bounce_address = self.fractal[:81]
			except:
				sys.exit(1)
		self.SecretKey = decoded_data[81:]
		self.Password = ""
		needle = self.Decrypt().DecryptedText
		if needle[int(self.Default_Size - len(self.identifier)):int(self.Default_Size)] == str(self.identifier):
			print("Message successfully received.")
			print('Message:', needle[:int(int(self.default_size) - len(self.identifier))])
		else:
			print('Message is still locked!')
		if bounce_address == '0'*81:
			print('Message terminated.')
		else:
			print('Bouncing...')
		self.DecryptedText = needle
		return self

	def Verify_Needle(self):
		PlainText = self.DecryptedText[:int(self.Default_Size)]
		Addresses_PubKey = Dynamic_Ledger().Scan_Address_Pool().Addresses
		for i in Addresses_PubKey:
			self.PublicKey = i[1] 
			try:
				self.Signature = b64decode(self.DecryptedText[int(self.Default_Size):])
				self.NeedleVerified = self.Signature_Verification().Verification
				self.FromAddress = i[0]
			except:
				self.NeedleVerified = "Authentication failed."
		return self

	def Signature_Verification(self):
		digest = SHA256.new()
		digest.update(self.DecryptedText)
		verifier = PKCS1_v1_5.new(self.PublicKey)
		verified = verifier.verify(digest, self.Signature)
		assert verified, "Signature verfication failed"
		self.Verification = verified



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
			self.PrivateSeed = Decryption(CipherText = EncodedSeed, Password = password).Decrypt().DecryptedText
	
		
class Generators:
	#Generates a random seed
	def __init__(self, Pass = "", bounce = 1):
		self.password = Pass
		self.beta = bounce
		self.Address = []
		self.PublicKey = []

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
			try:	
   				self.PrivateKey = RSA.importKey(Priv, passphrase = self.password)
   				Data = Writing_And_Reading().Reading(PublKey)
   				self.PublicKey = RSA.importKey(Data.replace("\\n","\n")).exportKey()
   			except ValueError:
   				self.PrivateKey = ""
   				pass
   		return self

	def Secret_Key(self):
		self.SecretKey = str(os.urandom(64))
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
	def __init__(self, directory = "UserData", Public = "Public_Address_Pool.txt", PubSeed = "Public_Seed.txt", Server = "https://cryptoiota.win:14625",Password = "", max_address_pool = 2, FindAddress = ""):

		self.PublicSeed = User_Module().PublicSeed 
		self.Entry = Writing_And_Reading().ReadingLine(directory = str(directory+"/"+Public))
		self.FindAddress = FindAddress
		self.directory = directory
		self.Public = Public
		self.PubSeed = PubSeed
		self.Server = Server
		self.Password = Password
		self.max_address_pool = max_address_pool
		self.Seed = []

	def Scan_Address_Pool(self):
		Address_PublicKey = []		
		for i in self.Entry:
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

	def Initialization(self):
		IOTA_Module(server = Server).Public_Addresses()
		self.Scan_Address_Pool()

		if len(self.Seed) >=1:
			self.PublicSeed = self.Seed[0].replace("#New_Seed#","").rstrip()
			Writing_And_Reading().Writing(directory = str(self.directory+"/"+self.PubSeed), data = str("\n"+self.PublicSeed), setting = "a")
			PublicAddress = IOTA_Module(Seed = self.PublicSeed).Generate_Address().Address.rstrip()
			IOTA_Module(server = Server).Sending(ReceiverAddress = PublicAddress, Message = str(User_Module().PublicLedgerAddress+"###"+User_Module(password = self.Password).PublicKey))
			
		
		#Count the number of addresses within the Public Seed
		if int(self.max_address_pool) <= len(self.Addresses):
			
			#Generate a new public seed and send it into the current public ledger
			NewPublicSeed = Generators().Seed_Generator().Seed
			#Get old address of old ledger and send new Public Seed
			PublicAddress = IOTA_Module().Generate_Address().Address
			IOTA_Module(server = self.Server).Sending(ReceiverAddress = PublicAddress, Message = str("#New_Seed#"+NewPublicSeed))
			
			#Now we send our public address into the new public ledger 
			NewPublicSeedAddress = IOTA_Module(server = self.Server, Seed = NewPublicSeed).Generate_Address().Address
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
			for i in self.Addresses:
				if i[0] == self.FindAddress:
					self.FoundKey = i[1]
		except ValueError:
			self.FoundKey = "No such address found!"
		return self



global chars
chars = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= '
global identifier
identifier = '////'
global default_size
default_size = 256
global alpha # number of trajectories
alpha = 1
global beta # number of bounces
beta = 1


def decode(ciphertext, secret_code):
	priv_key = User_Module(password = secret_code).PrivateKey
	cipher = PKCS1_OAEP.new(priv_key)
	msg = cipher.decrypt(str(ciphertext))
	return msg

def decrypt(ciphertext, secret_key):
	cipher = pyffx.String(str(User_Module(password = secret_key).PrivateKey), alphabet=str(chars), length=len(str(ciphertext)))
	plaintext = cipher.decrypt(str(ciphertext))
	return plaintext



def unlock(locked_message, secret_code):
    ciphertext = locked_message[:600]
    metadata = locked_message[618:].split("##:##")
    metadata.remove('')
    for i in range (0, len(metadata)):
        try:
            decoded_data = decode(metadata[i], secret_code)
        except:
            pass
        try:
            bounce_address = decoded_data[:81]
        except:
            print 'Format error: No metadata could be decoded or the message exceeds 252 characters.'
            sys.exit(1)
    secret_key = decoded_data[81:]
    needle = decrypt(ciphertext, secret_code)
    if needle[int(default_size - len(identifier)):int(default_size)] == str(identifier):
        print 'Message successfully received.'
        print 'Message:', needle[:int(int(default_size) - len(identifier))]
    else:
        print 'Message is still locked!'
    if bounce_address == '0'*81:
        print 'Message terminated.'
    else:
        print 'Bouncing...'
    return needle











# Here we initialize the script:
Password = "Hello World"
message = "Ergo "
address = "DCNHW9HVYKNLC9DJVDOJIWB9FMCERABH9NVIKHVKQFBMTV9DL9SFNPFDYRNCEDMGDVJPKSIOZTTLGGMAX"
Sev = "http://localhost:14265"
Setup = User_Module(password = Password, Server = Sev)

AboutToSend = Encryption(password = Password, PlainText = message, ReceiverAddress = str(address)).Lock_And_Load()
cipher = AboutToSend.MessageLocked
addressing = AboutToSend.FirstAddress

needle = unlock(cipher, Password)
#verify_needle(needle, read_public_key())


#Faction = Decryption(Password = Password, CipherText = cipher)
#unlocked = Faction.Unlock().DecryptedText
#verify = Faction.Verify_Needle().NeedleVerified
#print(unlocked)
#print(verify)