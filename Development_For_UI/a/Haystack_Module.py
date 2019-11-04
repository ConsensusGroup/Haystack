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

	def Send_Message(self, Message, ReceiverAddress, PublicKey, DifferentPaths = "", Encrypted = True, Ping_Function = False):
		Sent_And_Confirmed = []
		Message = b64encode(Message)
		if isinstance(DifferentPaths, int) == True:
			self.DifferentPaths = DifferentPaths

		MessageShrapnells = Dynamic_Public_Ledger().Shrapnell_Function(Message_PlainText = Message, Encrypted_Shrapnell = Encrypted)
		Symmetric_Key = MessageShrapnells[1]
		for x in range(self.DifferentPaths):
			for i in MessageShrapnells[0]:
				ToSend = self.Prepare_Message(i, ReceiverAddress, PublicKey, Symmetric_Key)
				hashed = self.PrivateIOTA.Send(ReceiverAddress = ToSend[1], Message = ToSend[0])
				if Ping_Function == True:
					Sent_And_Confirmed.append([i, ToSend[2]])
				else:
					Sent_And_Confirmed.append([ReceiverAddress, hashed, ToSend[1]])  #[Receiver, Hash, Relayer]
		return Sent_And_Confirmed

	def Prepare_Message(self, Message = "", ReceiverAddress = "", PublicKey = "", Symmetric_Key = ""):

		#Here we generate the Trajectory of the message
		Trajectory = Dynamic_Public_Ledger().Path_Finder(ReceiverAddress, PublicKey)
		Trajectory.append(["0"*81, "######"])
		Trajectory.reverse()
		CipherText = ""
		Cipher = ""
		Repeat = True
		for i in range(len(Trajectory)):
			Address = Trajectory[i][0]
			if i != int(len(Trajectory)-1):
				if ReceiverAddress == Trajectory[i+1][0] and Repeat == True:
					Repeat = False
					PublicKey = Trajectory[i+1][1]
					Cipher = self.Layering_Encryption(PlainText = str(Cipher + self.MessageIdentifier + Message), PublicKey = PublicKey, Address = Address, SymKey = Symmetric_Key)
				else:
					PublicKey = Trajectory[i+1][1]
					Cipher = self.Layering_Encryption(PlainText = Cipher, PublicKey = PublicKey, Address = Address)
			else:
				Receiving_Address = Address
		return [Cipher, Receiving_Address, Trajectory]

	def Ping_Function(self):
		#Define directory and read the file
		Ping_Dir = str(self.UserFolder+"/"+self.PathFolder+"/"+self.Trajectory_Ping)
		Tools().Build_DB(File = Ping_Dir)
		Ping_Dictionary = Tools().Read_From_Json(directory = Ping_Dir)

		#Generate information about the client
		Current_Block = Dynamic_Public_Ledger().Calculate_Block().Block
		Client_Public_Address = self.PrivateIOTA.Generate_Address(Index = Current_Block)
		Client_Public_Key = self.PublicKey

		#Here we generate a random number used to identify the ping to a trajectory.
		Random = str(Key_Generation().Secret_Key).encode("hex")[:self.Default_Size-20]
		Data = self.Send_Message(Message = Random, ReceiverAddress = Client_Public_Address, PublicKey = Client_Public_Key, Ping_Function = True)

		#Here we record the messaage as plaintext as a label and the trajectory as a string.
		for i in Data:
			Fragment = i[0]
			Path_Taken = i[1]
			Path_Taken.reverse()
			Trajectory_As_String = str(Current_Block)
			for x in i[1]:
				if x[0] == '0'*81:
					Address = "X"
				elif x[0] == Client_Public_Address:
					Address = "LOCALCLIENT"
				else:
					Address = x[0]
				Trajectory_As_String = str(Trajectory_As_String + "-->" + Address)
				Ping_Dictionary = Tools().Add_To_Dictionary(Input_Dictionary = Ping_Dictionary, Entry_Label = Fragment, Entry_Value = Trajectory_As_String)
			Tools().Write_To_Json(directory = Ping_Dir, Dictionary = Ping_Dictionary)

		return self

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
			try:
				Output = self.Message_Decrypter(Cipher = str(Message))
				self.Postprocessing_Packet(ToSend = Output, Hash_Of_Incoming_Tx = str(BundleHash), IOTA_Instance = self.PrivateIOTA)
				self.Incoming_Message = self.Reconstruction_Of_Message(True)
				self.Error = False
			except:
				self.Error = True
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
	Trusted_Paths().Build_LedgerDB()
	For_Ping = 1
	while RunTime == True:
		if "0" == str(float(For_Ping)/float(Configuration().Ping_Rate)).split(".")[1]:
			Sender_Client().Ping_Function()
			print("Sending Ping @: "+str(For_Ping))
		For_Ping = For_Ping +1
		Dynamic_Public_Ledger().Start_Ledger()
		Trusted_Paths().Catch_Up()
		#Trusted_Paths().Scan_Paths()
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
