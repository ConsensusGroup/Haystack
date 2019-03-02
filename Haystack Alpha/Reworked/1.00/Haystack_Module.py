####################################################################################
##################### This script handles the Haystack protocol ####################
####################################################################################

from Configuration_Module import Configuration
from Cryptography_Module import *
from IOTA_Module import *
from User_Modules import User_Profile
from base64 import b64encode, b64decode
from DynamicPublicLedger_Module import *

class Sender_Client(Encryption, Key_Generation, Configuration, User_Profile):

	def __init__(self, BlockTime):
		Configuration.__init__(self)
		Encryption.__init__(self)
		User_Profile.__init__(self)
		self.BlockTime = BlockTime
		self.PrivateIOTA = IOTA_Module(Seed = self.Private_Seed)

	def Send_Message(self, Message, ReceiverAddress, PublicKey):
		MessageShrapnells = Dynamic_Public_Ledger(self.BlockTime).Shrapnell_Function(Message)
		Symmetric_Key = MessageShrapnells[1]
		for i in MessageShrapnells[0]:
			ToSend = self.Prepare_Message(Message, ReceiverAddress, PublicKey, Symmetric_Key)
			hashed = self.PrivateIOTA.Send(ReceiverAddress = ToSend[1], Message = ToSend[0])
			print(hashed)
		return ToSend

	def Prepare_Message(self, Message = "", ReceiverAddress = "", PublicKey = "", Symmetric_Key = ""):
		#Here we generate the Trajectory of the message
		Trajectory = Dynamic_Public_Ledger(BlockTime = self.BlockTime).Path_Finder(ReceiverAddress, PublicKey)
		Trajectory.append(["0"*81, "######"])
		Trajectory.reverse()
		CipherText = ""
		Cipher = ""
		for i in range(len(Trajectory)):
			Address = Trajectory[i][0]
			if i != int(len(Trajectory)-1):
				if ReceiverAddress == Trajectory[i+1][0]:
					PublicKey = Trajectory[i+1][1]
					Cipher = self.Layering_Encryption(PlainText = str(Cipher + self.MessageIdentifier + Message), PublicKey = PublicKey, Address = Address, SymKey = Symmetric_Key).Cipher
				else:
					PublicKey = Trajectory[i+1][1]
					Cipher = self.Layering_Encryption(PlainText = Cipher, PublicKey = PublicKey, Address = Address).Cipher
			else:
				Receiving_Address = Address
		return [Cipher, Receiving_Address]

class Receiver_Client(Decryption, Encryption, Key_Generation, Configuration, User_Profile, Dynamic_Public_Ledger):

	def __init__(self, BlockTime):
		Configuration.__init__(self)
		User_Profile.__init__(self)
		self.BlockTime = BlockTime
		self.PrivateIOTA = IOTA_Module(Seed = self.Private_Seed)

	def Check_Inbox(self, Hashes):
		Messages = self.PrivateIOTA.Receive(Start = int(Dynamic_Public_Ledger(BlockTime = self.BlockTime).Calculate_Block().Block-2)).Message
		print(Messages)
		if len(Messages) != len(Hashes):
			for i in Messages:
				print(i)
				hashed = self.Message_Decrypter(Cipher = i)
				Hashes.append(hashed)
		return Hashes

	def Message_Decrypter(self, Cipher):
		Message = Cipher
		RelayNumber = 1
		NextAddress_PublicKey = ""
		counter = 0
		hashed = ""
		while counter <= self.MaxBounce +2:
			try:
				Message = self.Message_Delayering(Message)
				RelayText = Message[0]
				NextAddress = Message[1]
			except TypeError:
				pass

			#case 1: The message cant be decrypted at all -> Terminate loop
#			if RelayText == False:
#				Send = Cipher 
#				counter = self.MaxBounce + 5
#			#case 2: The Message was decrypted but has been decryted before -> See how many bounces

			if NextAddress == "0"*81:
				RelayNumber = RelayNumber + 1
				Message = Message[0]

			#Case 3: Previously relayed -> check relay number
			elif self.Identifier in RelayText and NextAddress != "0"*81:
				for i in Dynamic_Public_Ledger(self.BlockTime).Check_User_In_Ledger(ScanAll = True).All_Accounts:
					if i[0] == NextAddress:
						NextAddress_PublicKey = i[1]
				if NextAddress_PublicKey != "":
					for i in range(RelayNumber):
						RelayText = self.Layering_Encryption(PlainText = RelayText, PublicKey = NextAddress_PublicKey, Address = "0"*81).Cipher
					Send = RelayText
					hashed = self.PrivateIOTA.Send(ReceiverAddress = NextAddress, Message = Send)
					counter = self.MaxBounce+5
			counter = counter +1
		return hashed




