####################################################################################
##################### This script handles the Haystack protocol ####################
####################################################################################

from Configuration_Module import Configuration
from Cryptography_Module import *
from IOTA_Module import *
from User_Modules import User_Profile, Initialization
from base64 import b64encode, b64decode
from DynamicPublicLedger_Module import *
from Inbox_Module import Inbox_Manager, Trusted_Paths
from time import sleep
from Tools_Module import Tools

class Sender_Client(Encryption, Key_Generation, Configuration, User_Profile):

	def __init__(self):
		Configuration.__init__(self)
		Encryption.__init__(self)
		User_Profile.__init__(self)
		self.PrivateIOTA = IOTA_Module(Seed = self.Private_Seed)

	def Send_Message(self, Message, ReceiverAddress, PublicKey, DifferentPaths = False):
		Sent_And_Confirmed = []
		Message = b64encode(Message)
		if isinstance(DifferentPaths, int):
			self.DifferentPaths = DifferentPaths
		MessageShrapnells = Dynamic_Public_Ledger().Shrapnell_Function(Message)
		Symmetric_Key = MessageShrapnells[1]
		for i in MessageShrapnells[0]:
			print(i)
			for x in range(self.DifferentPaths):
				ToSend = self.Prepare_Message(i, ReceiverAddress, PublicKey, Symmetric_Key)
				hashed = self.PrivateIOTA.Send(ReceiverAddress = ToSend[1], Message = ToSend[0])
				Sent_And_Confirmed.append([ReceiverAddress, hashed, ToSend[1]])  #[Receiver, Hash, Relayer]
		return Sent_And_Confirmed

	def Prepare_Message(self, Message = "", ReceiverAddress = "", PublicKey = "", Symmetric_Key = ""):
		#Here we generate the Trajectory of the message
		Trajectory = Dynamic_Public_Ledger().Path_Finder(ReceiverAddress, PublicKey)
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

	def __init__(self):
		Configuration.__init__(self)
		User_Profile.__init__(self)
		Inbox_Manager.__init__(self)
		self.PrivateIOTA = IOTA_Module(Seed = self.Private_Seed)
		self.Block = Dynamic_Public_Ledger().Calculate_Block().Block

	def Check_Inbox(self):
		self.Incoming_Message = []
		for BundleHash, Message in self.Read_From_Json(directory = self.NotRelayed_Dir).items():
			Output = self.Message_Decrypter(Cipher = str(Message))
			self.Postprocessing_Packet(ToSend = Output, Hash_Of_Incoming_Tx = str(BundleHash), IOTA_Instance = self.PrivateIOTA)
			self.Incoming_Message = self.Reconstruction_Of_Message(True)
			#except:
			#	print("Failed Incoming TX")
			#	self.Postprocessing_Packet(ToSend = ['INVALID', '0'*81], Hash_Of_Incoming_Tx = str(BundleHash), IOTA_Instance = self.PrivateIOTA)
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

				if self.MessageIdentifier in To_Relay:
					Contains_Message = To_Relay.split(self.MessageIdentifier)
					To_Relay = Contains_Message[0]
					Message_Fragment = Contains_Message[1:]
					if isinstance(Message_Fragment, list) == True:
						Message_As_String = str(self.MessageIdentifier + Tools().List_To_String(List = Message_Fragment) + self.MessageIdentifier)
						self.Addressed_To_Client(Message_As_String, SymKey)

				#Enforce that this has been decrypted properly
				if self.Identifier in To_Relay and Next_Address != '0'*81:
					counter = counter +1
					for i in Dynamic_Public_Ledger().Check_User_In_Ledger(ScanAll = True).All_Accounts:
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

#This will simply run the client in non interactive mode.
if __name__ == "__main__":
	RunTime = True
	Initialization().InboxGenerator()
	Inbox_Manager().Create_DB()
	while RunTime == True:
		Dynamic_Public_Ledger().Start_Ledger()
		Trusted_Paths().Catch_Up()
		Message = Receiver_Client().Check_Inbox()
		Message = Message.Incoming_Message
		for i in Message:
			try:
				if i[0] != False:
					print("Passed!"+ "\n Message From:	 " + str(i[0]) + "\n Message:	 "+ str(i[1]))
				else:
					print("No New Message for you.....")
			except:
				print("No New Message for you.")
		sleep(Configuration().RefreshRate)
