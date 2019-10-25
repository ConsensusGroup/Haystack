####################################################################################
################### This script handles the Dynamic Public Ledger ##################
####################################################################################

from Configuration_Module import Configuration
from User_Modules import User_Profile
from IOTA_Module import *
from Cryptography_Module import *
import math, random
from base64 import b64encode, b64decode
from iota import TryteString
from Tools_Module import *

class Dynamic_Public_Ledger(Configuration, User_Profile):
	def __init__(self):
		Configuration.__init__(self)
		User_Profile.__init__(self)
		self.PublicIOTA = IOTA_Module(Seed = self.PublicSeed)
		self.PrivateIOTA = IOTA_Module(Seed = self.Private_Seed)
		self.Ledger_Accounts = []
		self.All_Accounts = []

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

	def Validate_User(self, Ledger_Entry, ScanAll = False):
		Submited = b64decode(Ledger_Entry).split(self.Identifier)
		ToVerify = str(Submited[0]+self.Identifier+Submited[1])
		Signature = Submited[2]
		PublicKey = Submited[1]
		if Decryption().SignatureVerification(ToVerify = ToVerify, PublicKey = PublicKey, Signature = Signature).Verified == True and [Submited[0],PublicKey] not in self.Ledger_Accounts and ScanAll == False:
			self.Ledger_Accounts.append([Submited[0],PublicKey])
		elif Decryption().SignatureVerification(ToVerify = ToVerify, PublicKey = PublicKey, Signature = Signature).Verified == True and ScanAll == True:
			self.All_Accounts.append([Submited[0],PublicKey])
		else:
			pass

	def Submit_User(self):
		self.Calculate_Block()
		PublicAddress = self.PrivateIOTA.Generate_Address(Index = self.Block)
		ToSubmit = str(PublicAddress+self.Identifier+self.PublicKey)
		Signed_ToSubmit = b64encode(str(ToSubmit+self.Identifier+Encryption().MessageSignature(ToSign = ToSubmit).Signature))
		return Signed_ToSubmit

	def Check_User_In_Ledger(self, ScanAll = False):
		self.Present = False
		self.Calculate_Block()
		if ScanAll == True:
			Entries = self.PublicIOTA.Receive(Start = int(self.Block-self.Replay), Stop = self.Block+1).Message
		else:
			Entries = self.PublicIOTA.Receive(Start = self.Block, Stop = self.Block +1).Message
		for i in Entries:
			try:
				Address = b64decode(i).split(self.Identifier)[0]
				if ScanAll == False:
					if Address == self.PrivateIOTA.Generate_Address(Index = self.Block):
						self.Present = True
				self.Validate_User(Ledger_Entry = i, ScanAll = ScanAll)
			except:
				pass
		return self

	def Start_Ledger(self):
		hashed = None
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

	def Shrapnell_Function(self, Message_PlainText = "", Encrypted_Shrapnell = True):
		Message_Signed = Message_PlainText + self.MessageIdentifier + Encryption().MessageSignature(ToSign = Message_PlainText).Signature
		Symmetric_Message_Key = Key_Generation().Secret_Key()
		Symmetrically_Encrypted = Encryption().SymmetricEncryption(PlainText = b64encode(Message_Signed), SecretKey = Symmetric_Message_Key)
		if Encrypted_Shrapnell == True:
			Fragments = Tools().Split(string = Symmetrically_Encrypted, length = self.Default_Size) ###Encrypted Communication
		else:
			Fragments = Tools().Split(string = Message_PlainText, length = self.Default_Size) ###Plain Communication

		Fragment_Tags = []
		if len(Fragments) > 1:
			while len(Fragments)-1 != len(Fragment_Tags):
				Fragment = str(Key_Generation().Secret_Key(length = 2).encode('hex'))
				if Fragment not in Fragment_Tags:
					Fragment_Tags.append(Fragment)

		Fragment_Tags.append(self.MessageIdentifier)
		Fragment_Tags.insert(0, str(self.MessageIdentifier))
		Shrapnells = []
		for i in range(len(Fragments)):
			Fragment = str(Fragment_Tags[i]+Fragments[i]+Fragment_Tags[i+1])
			Shrapnells.append(Fragment)
		return [Shrapnells, Symmetric_Message_Key]

	def Rebuild_Shrapnells(self, String, Verify):
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
			cipher = Piece[len(self.MessageIdentifier):len(Piece)-len(self.MessageIdentifier)]
			for j in Temp:
				StartTag2 = j[0:len(self.MessageIdentifier)]
				cipher2 = j[len(self.MessageIdentifier):len(j)-len(self.MessageIdentifier)]
				EndTag2 = j[len(j)-len(self.MessageIdentifier):]
				if StartTag2 == EndTag and EndTag!=self.MessageIdentifier:
					CipherText = str(StartTag + cipher + cipher2 + EndTag2)
				elif StartTag == EndTag2 and StartTag != self.MessageIdentifier:
					CipherText = str(StartTag2 + cipher2 + cipher + EndTag)

		Message = str(Decryption().SymmetricDecryption(CipherText = CipherText, SecretKey = Symmetric_Key))
		try:
			Message = b64decode(Message).split(self.MessageIdentifier)
			if Verify == True:
				self.Check_User_In_Ledger(ScanAll = True)
				for i in self.All_Accounts:
					Verification = Decryption().SignatureVerification(ToVerify = Message[0], PublicKey = i[1], Signature = Message[1]).Verified
					if Verification == True:
						return [i[0], b64decode(Message[0]), Verification] # --> Output is [Address, Message, Verification_Of_Signature]
				if Verification == False:
					return ["UNKNOWN", b64decode(Message[0]), False] # --> Output is [Address, Message, Verification_Of_Signature]
		except:
			return False

	def Path_Finder(self, ReceiverAddress= "", PublicKey = "", PingFunction = False, index = 0):
		self.Calculate_Block().Block
		if index == 0:
			self.Check_User_In_Ledger()
		Trajectory = []
		while len(Trajectory) != self.MaxBounce:
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

		elif len(Trajectory) >= 0 and PingFunction == False:
			Ran_Index = int(round(random.uniform(0, len(Trajectory))))
		else:
			pass

		if ReceiverAddress != "" and PublicKey != "" and len(Trajectory) >= 0:
			SendTo = [ReceiverAddress,PublicKey]
			Trajectory.insert(Ran_Index, SendTo)
		if len(Trajectory) > 0:
			return Trajectory

class Trusted_Paths(Tools, Configuration):
	def __init__(self):
		Tools.__init__(self)
		Configuration.__init__(self)
		self.Ledger_Accounts_Dir = str(self.UserFolder+"/"+self.PathFolder+"/"+self.Ledger_Accounts_File)
		self.Last_Block_Dir = str(self.UserFolder+"/"+self.PathFolder+"/"+self.Last_Block)
		self.Current_Block = Dynamic_Public_Ledger().Calculate_Block().Block

	def Build_LedgerDB(self):
		self.Build_Directory(directory = str(self.UserFolder+"/"+self.PathFolder))
		self.Build_DB(File = self.Ledger_Accounts_Dir)
		self.Build_DB(File = self.Last_Block_Dir)

		#Read the file when the user was last online
		Block_Number = self.Read_From_Json(directory = self.Last_Block_Dir)

		#If the dictionary is empty
		if Block_Number == {}:
			Block_Number = self.Add_To_Dictionary(Input_Dictionary = Block_Number, Entry_Label = "Block", Entry_Value = self.Current_Block)
			self.Write_To_Json(directory = self.Last_Block_Dir, Dictionary = Block_Number)
			self.Last_Block_Online = self.Current_Block
		else:
			self.Last_Block_Online = self.Block_Number
		return self

	def Gather_Ledger_Accounts(self):
		self.Build_LedgerDB()
		self.Replay = int(self.Current_Block - self.Last_Block_Online)
		return self
