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
		Submited = Ledger_Entry.decode("hex").split(self.Identifier)
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
		Signed_ToSubmit = str(ToSubmit+self.Identifier+Encryption().MessageSignature(ToSign = ToSubmit).Signature).encode("hex")
		return Signed_ToSubmit

	def Check_User_In_Ledger(self):
		self.Present = False
		Entries = self.PublicIOTA.Receive(Start = self.Block).Message
		for i in Entries:
			try: 
				Address = i.decode("hex").split(self.Identifier)[0]
				if Address == self.PrivateIOTA.Generate_Address(Index = self.Block):
					self.Present = True 
				self.Validate_User(Ledger_Entry = i)
			except:
				pass
		return self 

	def Start_Ledger(self):
		hashed = None
		for i in range(1000):
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

class Relay_Client(Dynamic_Public_Ledger, Decryption, User_Profile, IOTA_Module, Encryption, Key_Generation):
	def __init__(self, Delete_Input):
		Dynamic_Public_Ledger.__init__(self)
		Decryption.__init__(self)
		Encryption.__init__(self)
		User_Profile.__init__(self)
		Key_Generation.__init__(self)
		self.Ledger_Accounts = Delete_Input
		
	
	def Shrapnell_Function(self, Message_PlainText = ""):
		Message_Signed = Message_PlainText + self.MessageSignature(ToSign = Message_PlainText).Signature
		Symmetric_Message_Key = self.Secret_Key()
		Symmetrically_Encrypted = self.SymmetricEncryption(PlainText = Message_Signed.encode('hex'), SecretKey = Symmetric_Message_Key)
		Fragments = self.Split(string = Symmetrically_Encrypted, length = 248)
		Fragment_Tags = []
		if len(Fragments) > 1:
			while len(Fragments)-1 != len(Fragment_Tags):
				Fragment = str(self.Secret_Key(length = 2).encode('hex'))
				if Fragment not in Fragments:
					Fragment_Tags.append(Fragment)

		Fragment_Tags.append(self.Identifier)
		Fragment_Tags.insert(0, self.Identifier)
		for i in range(len(Fragments)):
			Fragments[i] = str(Fragment_Tags[i]+Fragments[i]+Fragment_Tags[i+1])
		return [Fragments, Symmetric_Message_Key]
	
	def Relay_Function(self):
		Messages = self.PrivateIOTA.Receive(Start = int(self.Calculate_Block().Block-1), Stop = int(self.Calculate_Block().Block+1)).Message
		print(Messages)

	def Sender_Function(self, ReceiverAddress ="", PublicKey = "", Message = "", PingFunction = False):

		#Generate the trajectory of the message 
		Trajectory = self.Path_Finder(ReceiverAddress = ReceiverAddress, PublicKey = PublicKey, PingFunction = PingFunction)
		while  Trajectory == None:
			Trajectory = self.Path_Finder(ReceiverAddress = ReceiverAddress, PublicKey = PublicKey, PingFunction = PingFunction)

		#Reverse the Trajectory list
		for i in range(len(Trajectory)):
			if i == 0:
				Sending_To = Trajectory[0][0]
				if len(Trajectory) > i+1:
					Relayer_After = Trajectory[i+1][0] 
				else:
					Relayer_After = '0' * 81
				PublicKey_To = Trajectory[0][1]
				if Sending_To == ReceiverAddress:
					string = self.Layering_Encrpytion(string = Message, PublicKey = PublicKey_To, Address = Relayer_After)
					#string = str(Sending_To+"<<<"+PublicKey_To+"|"+Message+"||||||||"+Relayer_After+"|>>> ")
				else:
					string = self.Layering_Encrpytion(string = "", PublicKey = PublicKey_To, Address = Relayer_After)
					#string = str(Sending_To+"<"+PublicKey_To+"|"+Relayer_After+"|> ")
			else:
				Relayer = Trajectory[i][0]
				PublicKey_of_Relayer = Trajectory[i][1]
				if len(Trajectory) > i+1:
					Relayer_After = Trajectory[i+1][0]
					if Relayer == ReceiverAddress:
						string = self.Layering_Encrpytion(string = str(Message+self.Identifier + string), PublicKey = PublicKey_of_Relayer, Address = Relayer_After)
						#string = string + str(Relayer+"<<<"+PublicKey_of_Relayer+"|"+Message+"||||||||"+Relayer_After+"|>>>")
					else:
						string = self.Layering_Encrpytion(string = string , PublicKey = PublicKey_of_Relayer, Address = Relayer_After)
						#string = string + str(Relayer + "<" + PublicKey_of_Relayer + "|" + Relayer_After + "|> ")
				else:
					Relayer_After = '0' * 81
					string = self.Layering_Encrpytion(string = string, PublicKey = PublicKey_of_Relayer, Address = Relayer_After)
					#string = string + str(Relayer + "<" + PublicKey_of_Relayer + "|" + Relayer_After + "|> ")
		return string

	def Path_Finder(self, ReceiverAddress= "", PublicKey = "", PingFunction = False):
		self.Calculate_Block().Block
		#self.Check_User_In_Ledger()
		Bouncers = int(round(random.uniform(0, self.MaxBounce)))
		Trajectory = []
		for i in range(Bouncers):
			index = int(round(random.uniform(0, len(self.Ledger_Accounts)-1)))
			Relayer = self.Ledger_Accounts[index]
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
