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

class Relay_Client(Dynamic_Public_Ledger, Decryption, User_Profile, IOTA_Module):
	def __init__(self):
		Dynamic_Public_Ledger.__init__(self)
		Decryption.__init__(self)
		User_Profile.__init__(self)

	def Relay_Function(self):
		Messages = self.PrivateIOTA.Receive(Start = int(self.Calculate_Block().Block-1), Stop = int(self.Calculate_Block().Block+1)).Message
		print(Messages)

	def Sender_Function(self):
		pass

	def Shrapnell_Function(self):
		pass

	def Path_Finder(self, ReceiverAddress= "", PublicKey = "", PingFunction = False):
		self.Calculate_Block().Block
		self.Check_User_In_Ledger()
		Bouncers = random.randrange(0, len(self.Ledger_Accounts))
		Addresses = self.Ledger_Accounts
		Trajectory = []
		for i in range(Bouncers):
			index = random.randrange(0, len(Addresses))
			Relayer = Addresses.pop(index)
			Trajectory.append(Relayer)
			print(Bouncers)
		
		if PingFunction == True:
			Ran_Index = int(len(Trajectory))
			ReceiverAddress = self.PrivateIOTA.Generate_Address(Index = self.Block)
			PublicKey = self.PublicKey
		else: 
			Ran_Index = random.randrange(0, len(Trajectory))
		
		if ReceiverAddress != "" and PublicKey != "":
			SendTo = [ReceiverAddress,PublicKey]
			Trajectory.insert(Ran_Index, SendTo)

			print(Trajectory)
		return Trajectory




#y = Dynamic_Public_Ledger().Start_Ledger()
x = Relay_Client().Path_Finder()
