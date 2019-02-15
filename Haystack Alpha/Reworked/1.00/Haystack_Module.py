####################################################################################
##################### This script handles the Haystack protocol ####################
####################################################################################

from Configuration_Module import Configuration
from Cryptography_Module import *
from IOTA_Module import *
from User_Modules import User_Profile
from Tools_Module import *
from time import sleep
import math, random
from base64 import b64encode, b64decode
from iota import TryteString

class Dynamic_Public_Ledger(Configuration, User_Profile):
	def __init__(self):
		Configuration.__init__(self)
		User_Profile.__init__(self)
		self.PublicIOTA = IOTA_Module(Seed = self.PublicSeed)
		self.PrivateIOTA = IOTA_Module(Seed = self. Private_Seed)
		self.Ledger_Accounts = []

	def Calculate_Block(self):
		#Check the current time of the Tangle
		Current = self.PublicIOTA.LatestTangleTime().TangleTime

		#Calculate the current Block and use as index for current address
		Blockfloat = float((Current - self.GenesisTime) / float(self.BlockTime))
		self.Block = math.trunc(Blockfloat)
		difference = Blockfloat - self.Block
		if difference >= self.LowerBound:
			self.ChangeBlock = True 
		else: 
			self.ChangeBlock = False
		return self

	def Validate_User(self, Ledger_Entry):
		Submited = b64decode(Ledger_Entry).split(self.Identifier)
		ToVerify = str(Submited[0]+self.Identifier+Submited[1])
		Signature = Submited[2]
		PublicKey = Submited[1]
		if Decryption().SignatureVerification(ToVerify = ToVerify, PublicKey = PublicKey, Signature = Signature).Verified == True and [Submited[0],PublicKey] not in self.Ledger_Accounts:
			self.Ledger_Accounts.append([Submited[0],PublicKey])
		else:
			pass

	def Submit_User(self):
		self.Calculate_Block()
		PublicAddress = self.PrivateIOTA.Generate_Address(Index = self.Block)
		ToSubmit = str(PublicAddress+self.Identifier+self.PublicKey)
		Signed_ToSubmit = b64encode(str(ToSubmit+self.Identifier+Encryption().MessageSignature(ToSign = ToSubmit).Signature))
		return Signed_ToSubmit

	def Check_User_In_Ledger(self):
		self.Present = False
		Entries = self.PublicIOTA.Receive(Start = self.Block).Message
		for i in Entries:
			try: 
				Address = b64decode(i).split(self.Identifier)[0]
				if Address == self.PrivateIOTA.Generate_Address(Index = self.Block):
					self.Present = True 
				self.Validate_User(Ledger_Entry = i)
			except:
				pass
		return self 

	def Start_Ledger(self):
		hashed = None
		for i in range(1):
			Block = self.Calculate_Block().Block
			try:
				if self.Check_User_In_Ledger().Present == False and hashed == None:
					hashed = self.PrivateIOTA.Send(ReceiverAddress = [self.PublicIOTA.Generate_Address(Index = self.Block)], Message = [self.Submit_User()])
			except TypeError:
				hashed = None
			#This block prevents duplicate Tx 
			if self.ChangeBlock == True:
				hashed = None
				self.Ledger_Accounts = []
		return self 

class Messaging_Client(Dynamic_Public_Ledger, Decryption, User_Profile, IOTA_Module, Encryption, Key_Generation, Tools):
	def __init__(self, Delete_Input = ""):
		Dynamic_Public_Ledger.__init__(self)
		Decryption.__init__(self)
		Encryption.__init__(self)
		User_Profile.__init__(self)
		Key_Generation.__init__(self)
		Tools.__init__(self)
		self.Ledger_Accounts = Delete_Input
		self.MessageShrapnells = []
		self.ToRelay = []

	def Shrapnell_Function(self, Message_PlainText = ""):
		Message_Signed = Message_PlainText + self.MessageIdentifier + self.MessageSignature(ToSign = Message_PlainText).Signature
		Symmetric_Message_Key = self.Secret_Key()
		Symmetrically_Encrypted = self.SymmetricEncryption(PlainText = b64encode(Message_Signed), SecretKey = Symmetric_Message_Key)
		Fragments = self.Split(string = Symmetrically_Encrypted, length = self.Default_Size)
		#Fragments = self.Split(string = Message_PlainText, length = self.Default_Size)
		Fragment_Tags = []
		if len(Fragments) > 1:
			while len(Fragments)-1 != len(Fragment_Tags):
				Fragment = str(self.Secret_Key(length = 2).encode('hex'))
				if Fragment not in Fragments:
					Fragment_Tags.append(Fragment)

		Fragment_Tags.append(self.MessageIdentifier)
		Fragment_Tags.insert(0, self.MessageIdentifier)
		for i in range(len(Fragments)):
			Fragments[i] = str(Fragment_Tags[i]+Fragments[i]+Fragment_Tags[i+1])
		return [Fragments, Symmetric_Message_Key]

	def Sending_Message(self, Message_PlainText = "", PingFunction = False, ReceiverAddress = "", PublicKey = ""):
		Shraps = self.Shrapnell_Function(Message_PlainText = Message_PlainText)
		SenderList = []
		MessageList = []
		for i in range(len(Shraps[0])):
			Output = self.Trajectory_Function(ReceiverAddress = ReceiverAddress, PublicKey = PublicKey, Message = Shraps[0][i], Message_Symmetric_Key = Shraps[1])
			print(Output)
			#SenderList.append(Output[1])
			#MessageList.append(Output[0])
		#return Output
		#hashed = self.PrivateIOTA.Send(ReceiverAddress = SenderList, Message = MessageList)
		#print(hashed)

	def Trajectory_Function(self, ReceiverAddress ="", PublicKey = "", Message = "", Message_Symmetric_Key = "", PingFunction = False):
		#Generate the trajectory of the message 
		#Trajectory = self.Path_Finder(ReceiverAddress = ReceiverAddress, PublicKey = PublicKey, PingFunction = PingFunction)
		#while  Trajectory == None:
		#	Trajectory = self.Path_Finder(ReceiverAddress = ReceiverAddress, PublicKey = PublicKey, PingFunction = PingFunction)
		Trajectory = self.Ledger_Accounts
		Trajectory.append(["0"*81, "####"])
		Trajectory.reverse()
		Cipher = ""
		for i in range(len(Trajectory)):
			Address = Trajectory[i][0]
			if i != int(len(Trajectory)-1):
				if ReceiverAddress == Trajectory[i+1][0]:
					PublicKey = Trajectory[i+1][1]
					Cipher = self.Layering_Encrpytion(PlainText = str(Cipher + Message + Message_Symmetric_Key), PublicKey = PublicKey, Address = Address)
				else:
					PublicKey = Trajectory[i+1][1]
					Cipher = self.Layering_Encrpytion(PlainText = Cipher, PublicKey = PublicKey, Address = Address)
			else:
				Receiving_Address = Address
		return [Cipher, Receiving_Address]


	def Path_Finder(self, ReceiverAddress= "", PublicKey = "", PingFunction = False):
		self.Calculate_Block().Block
		self.Check_User_In_Ledger()
		Bouncers = int(round(random.uniform(0, len(self.Ledger_Accounts)-1)))
		Trajectory = []
		for i in range(Bouncers):
			Relayer = random.choice(self.Ledger_Accounts)
			if Relayer[0] != ReceiverAddress:
				Trajectory.append(Relayer)

		if PingFunction == True:
			ReceiverAddress = self.PrivateIOTA.Generate_Address(Index = self.Block)
			PublicKey = self.PublicKey
			if len(Trajectory) == 0:
				Relayer = self.Ledger_Accounts[random.randrange(0, len(self.Ledger_Accounts))]
				Trajectory.append(Relayer)
			Ran_Index = len(Trajectory)

		elif len(Trajectory) > 0 and PingFunction == False: 
			Ran_Index = int(round(random.uniform(0, len(Trajectory))))
		else: 
			pass

		if ReceiverAddress != "" and PublicKey != "" and len(Trajectory) > 0:
			SendTo = [ReceiverAddress,PublicKey]
			Trajectory.insert(Ran_Index, SendTo)
		if len(Trajectory) > 0:
			return Trajectory

	def Receiving_Message(self, CipherText):
		Relay_Key = []
		CipherPart = []
		if "==" in CipherText[len(CipherText)-2:]:
			for i in CipherText.split(self.Identifier):
				try:
					Unencrypted = self.AsymmetricDecryption(CipherText = b64decode(i), PrivateKey = Key_Generation().PrivateKey_Import().PrivateKey)
				except TypeError:
					Unencrypted = False
				if Unencrypted != False:
					Address = Unencrypted[len(Unencrypted)-81:]
					Key = Unencrypted[:len(Unencrypted)-81]
					Relay_Key.append([Address, Key])
				else:
					CipherPart.append(i)

			for cipher in CipherPart:
				for key in Relay_Key:
					Plain = b64decode(self.SymmetricDecryption(CipherText = cipher, SecretKey = key[1]))		
					if self.Identifier in Plain and not self.MessageIdentifier in Plain:
						self.ToRelay.append([key[0], Plain])
					elif self.MessageIdentifier in Plain:
						for i in Plain.split(self.MessageIdentifier):
							if self.Identifier in i:
								self.ToRelay.append([key[0], i])
							else:
								self.MessageShrapnells.append(i)
		return self 

	def Rebuild_Shrapnells(self, String):
		Shrapnells = String[0]
		Symmetric_Key = String[1]
		Intermediate = []
		Start = ""
		End = ""
		Temp = Shrapnells
		CipherText = ""
		for i in range(len(Shrapnells)):
			if i == 0:
				Piece = Shrapnells[i]
			else:
				Piece = CipherText
			StartTag = Piece[0:len(self.MessageIdentifier)]
			EndTag = Piece[len(Piece)-len(self.MessageIdentifier):]
			cipher = Piece[4:len(Piece)-len(self.MessageIdentifier)]
			for j in Temp:
				StartTag2 = j[0:len(self.MessageIdentifier)]
				cipher2 = j[len(self.MessageIdentifier):len(j)-len(self.MessageIdentifier)]
				EndTag2 = j[len(j)-4:]
				if StartTag2 == EndTag and EndTag!=self.MessageIdentifier:
					CipherText = str(StartTag + cipher + cipher2 + EndTag2)
				elif StartTag == EndTag2 and StartTag != self.MessageIdentifier:
					CipherText = str(StartTag2 + cipher2 + cipher + EndTag)
		
		CipherText = CipherText[len(self.MessageIdentifier):len(CipherText)-len(self.MessageIdentifier)]
		Message = self.SymmetricDecryption(CipherText = CipherText, SecretKey = Symmetric_Key)
		Message = b64decode(Message).split(self.MessageIdentifier)
		for i in self.Ledger_Accounts:
			Verification = self.SignatureVerification(ToVerify = Message[0], PublicKey = i[1], Signature = Message[1]).Verified
			if Verification == True:
				print("You have received a message from: "+i[0] + "\n" + Message[0])

class Relay_Client():

	def Relay_Function(self):
		Messages = self.PrivateIOTA.Receive(Start = int(self.Calculate_Block().Block-1), Stop = int(self.Calculate_Block().Block+1)).Message
		print(Messages)

