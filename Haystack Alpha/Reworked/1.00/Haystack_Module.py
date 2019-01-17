####################################################################################
##################### This script handles the Haystack protocol ####################
####################################################################################

from Configuration_Module import Configuration
from Cryptography_Module import *
from IOTA_Module import *
from User_Modules import User_Profile
from Tools_Module import *
from time import sleep
import math 

class Dynamic_Public_Ledger(Configuration, User_Profile):
	def __init__(self):
		Configuration.__init__(self)
		User_Profile.__init__(self)
		self.PublicIOTA = IOTA_Module(Seed = self.PublicSeed)
		self.PrivateIOTA = IOTA_Module(Seed = self. Private_Seed)

	def Calculate_Block(self):
		#Check the current time of the Tangle
		Current = self.PublicIOTA.LatestTangleTime().TangleTime

		#Calculate the current Block and use as index for current address
		Blockfloat = float((Current - self.GenesisTime) / float(self.BlockTime))
		self.Block = math.trunc(Blockfloat)

		Difference = Blockfloat -self.Block
		if Difference >= 0.80:
			self.NewBlock = True 
		else:
			self.NewBlock = False
		return self

	def Validate_User(self, Ledger_Entry):
		Submited = Ledger_Entry.decode("hex").split(self.Identifier)
		ToVerify = str(Submited[0]+self.Identifier+Submited[1])
		Signature = Submited[2]
		PublicKey = Submited[1]
		if Decryption().SignatureVerification(ToVerify = ToVerify, PublicKey = PublicKey, Signature = Signature).Verified == True:
			##### Add here a list function of users 
		else:
			pass

	def Submit_User(self):
		PublicAddress = self.PrivateIOTA.Generate_Address(Index = self.Block)
		ToSubmit = str(PublicAddress+self.Identifier+self.PublicKey)
		Signed_ToSubmit = str(ToSubmit+self.Identifier+Encryption().MessageSignature(ToSign = ToSubmit).Signature).encode("hex")
		return Signed_ToSubmit

x = Dynamic_Public_Ledger()
x.Calculate_Block().Block
x.Validate_User(Ledger_Entry = x.Submit_User())
