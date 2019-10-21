####################################################################################
##################### This script handles the Haystack protocol ####################
####################################################################################

from Configuration_Module import Configuration
from Cryptography_Module import *
from IOTA_Module import *
from User_Modules import User_Profile
from base64 import b64encode, b64decode
from DynamicPublicLedger_Module import *
from Inbox_Module import Inbox_Manager

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
			ToSend = self.Prepare_Message(i, ReceiverAddress, PublicKey, Symmetric_Key)
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
					Cipher = self.Layering_Encryption(PlainText = str(Cipher + self.MessageIdentifier + Message), PublicKey = PublicKey, Address = Address, SymKey = Symmetric_Key)
				else:
					PublicKey = Trajectory[i+1][1]
					Cipher = self.Layering_Encryption(PlainText = Cipher, PublicKey = PublicKey, Address = Address)
			else:
				Receiving_Address = Address
		return [Cipher, Receiving_Address]

class Receiver_Client(Decryption, Encryption, Key_Generation, Configuration, User_Profile, Dynamic_Public_Ledger, Inbox_Manager):

	def __init__(self, BlockTime):
		Configuration.__init__(self)
		User_Profile.__init__(self)
		Inbox_Manager.__init__(self)
		self.BlockTime = BlockTime
		self.PrivateIOTA = IOTA_Module(Seed = self.Private_Seed)
		self.Block = Dynamic_Public_Ledger(BlockTime).Calculate_Block().Block

	def Check_Inbox(self):
		self.Read_Tangle(IOTA_Instance = self.PrivateIOTA, Block = self.Block)
		for BundleHash, Message in self.Read_From_Json(directory = self.NotRelayed_Dir).items():
			try:
				Output = self.Message_Decrypter(Cipher = str(Message))
				self.Postprocessing_Packet(ToSend = Output, Hash_Of_Incoming_Tx = str(BundleHash), IOTA_Instance = self.PrivateIOTA)
			except:
				self.Postprocessing_Packet(ToSend = ['INVALID', '0'*81], Hash_Of_Incoming_Tx = str(BundleHash), IOTA_Instance = self.PrivateIOTA)
		return self

	def Message_Decrypter(self, Cipher):
		#Break the message cipher into two parts:
		if Cipher[0] == Cipher[len(Cipher)-1] == "'":
			Pieces = Cipher[1:len(Cipher)-1].split(self.Identifier)
		else:
			Pieces = Cipher.split(self.Identifier)

		Runtime = True
		counter = 0
		Next_Address = '0'*81
		while Runtime == True:
			if len(Pieces) != 2:
				Decrypted = False
			else:
				#This will be the asymmetric part:
				Decrypted = self.AsymmetricDecryption(b64decode(Pieces[1]), Key_Generation().PrivateKey_Import().PrivateKey)

			if Decrypted != False:
				Next_Address = Decrypted[len(Decrypted)-81:]
				SymKey = Decrypted[:len(Decrypted)-81]

				#Now we try to decrypt the symmetric part
				To_Relay = b64decode(self.SymmetricDecryption(CipherText = Pieces[0], SecretKey = SymKey))

				#Enforce that this has been decrypted properly
				if self.Identifier in To_Relay and Next_Address != '0'*81:
					if self.MessageIdentifier in To_Relay:
						counter = counter +1
						Message_PlainText = To_Relay.split(self.MessageIdentifier)
						Message_PlainText_Temp  = To_Relay
						To_Relay = Message_PlainText[0]
						Message_PlainText = Message_PlainText_Temp[len(To_Relay):]
						self.Addressed_To_Client(Message_PlainText, SymKey)

					for i in Dynamic_Public_Ledger(self.BlockTime).Check_User_In_Ledger(ScanAll = True).All_Accounts:
						if i[0] == Next_Address:
							NextAddress_PublicKey = i[1]
						#Terminate the while condition once a non dummy address was found.
						Runtime = False

				elif '0'*81 == Next_Address:
					counter = counter +1
					Pieces = To_Relay.split(self.Identifier)

				if Runtime == False:
					#Replace the stripped layers by re-encrypting the (counter) layers.
					for i in range(counter+1):
						To_Relay = self.Layering_Encryption(PlainText = To_Relay, PublicKey = NextAddress_PublicKey, Address = '0'*81)
					return [To_Relay, Next_Address]
			else:
				Runtime = False
				return [Cipher, Next_Address]
