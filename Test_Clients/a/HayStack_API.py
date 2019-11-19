####################################################################################
#################### This script is intended to serve as an API ####################
####################################################################################


from DynamicPublicLedger_Module import Dynamic_Public_Ledger
from Contact_Module import Contact_Client
from User_Modules import Initialization, User_Profile
from Inbox_Module import Inbox_Manager, Trusted_Paths
from Haystack_Module import Sender_Client, Receiver_Client
from Configuration_Module import Configuration
import config
import threading
from time import sleep
import random

class HayStack():
	def __init__(self):
		pass

	def Get_Current_Ledger_Addresses(self):
		self.Current_Addresses = Dynamic_Public_Ledger().Check_User_In_Ledger(Current_Ledger = True).Ledger_Accounts
		#Output = Current addresses within the ledger pool (list)
		self.BlockNumber = Dynamic_Public_Ledger().Calculate_Block().Block
		#Output = Current block number since genesis (int)
		return self

	def Get_Current_Address(self):
		self.Current_Address = Dynamic_Public_Ledger().PrivateIOTA.Generate_Address(Index = Dynamic_Public_Ledger().Calculate_Block().Block)
		#Output = Address of client at current block height (String)
		return self

	def Find_From_PubKey(self, PublicKey):
		self.Identities = Contact_Client().Link_Address_To_PubKey(Public_Key_To_Search = PublicKey).Other_Identities
		#Output = [PublicKey(string), known by other addresses(list)]
		return self

	def Find_From_Address(self, Address):
		Identities = Contact_Client().Link_Address_To_PubKey(Address_To_Search = Address).Other_Identities
		if Identities[0] != "0"*81:
			return Identities
			#Output = [PublicKey(string), known by other addresses(list)]
		else:
			return False
			#Output = False (bool)

	def Add_Address(self, Address, Username):
		Contact_Client().Link_Address_To_PubKey(Address_To_Search = Address, User_Name = Username)
		return self

	def Delete_From_Contacts(self, Username):
		Contact_Client().Delete_From_Contacts(User_Name = Username)
		#Output = Nothing
		return self

	def Username_From_Address(self, Address):
		Output = Contact_Client().Retrieve_UserName_From_Address(Address_To_Search = Address)
		#if Address in contact list; --> Output = [Saved Username (string), PublicKey(string), Has the address been found? (Bool)] otherwise a simple False(bool) will be returned
		return Output

	def Address_From_Username(self, Username):
		Output = Contact_Client().Username_To_Address(Username = Username)
		#Output: if contact present a list is returned [Public Key, Address], else 'None' is returned
		return Output

	def Last_Seen_Address(self, PublicKey):
		Output = Contact_Client().Get_Current_Address_From_PublicKey(PublicKey = PublicKey)
		#Output: String if address included in current ledger, else 'None' is returned
		return Output

	def Refresh_Contact_List(self):
		Contact_Client().Update_Contacts()
		#Output = Nothing
		return self

	def Return_Contact_List(self):
		Contact_Names = Contact_Client().Saved_Contacts()
		#Output = [List of usernames]
		return Contact_Names

	def Build_All_Directories(self):
		Initialization().Build_Application()
		Initialization().InboxGenerator()
		User_Profile()
		Inbox_Manager().Create_DB()
		Contact_Client().Build_ContactDB()
		Trusted_Paths().Build_LedgerDB()
		#Output = Nothing
		return self

	def Send_Message(self, Message, ReceiverAddress, PublicKey, DifferentPaths, Encrypted):
		Output = Sender_Client().Send_Message(Message = Message, ReceiverAddress = ReceiverAddress, PublicKey = PublicKey, DifferentPaths = DifferentPaths, Encrypted = Encrypted)
		#Output = [ReceiverAddresses, Hash of Tx, Relaying Address] (This will be a list)
		return Output

	def Ping_Function(self):
		Sender_Client().Ping_Function()
		#Output = Nothing
		return self

	def Inbox(self):
		Output = Receiver_Client().Check_Inbox()
		Incoming_Message = Output.Incoming_Message
		#Output = If messages are addressed to client; --> Output = [Messages] (list), otherwise [[False, False, False]]

		Sending_Error = Output.Error
		#Output = If there are errors in relaying, True (Bool); else False (Bool)
		return [Incoming_Message, Sending_Error]

	def Stored_Messages(self):
		Output = Inbox_Manager().Read_Stored_Messages()
		#Output: If there are messages a list is returned [Message, User] else an empty list is returned []
		return Output


##### This section of the API is responsible for running background services
class Run_HayStack_Client(threading.Thread):
	def __init__(self, Function):
		threading.Thread.__init__(self)
		self.RunTime = True
		self.Function = Function
		self.Echo = ""

	def run(self):
		if self.Function == "Dynamic_Public_Ledger":
			while self.RunTime:
				try:
					x = Dynamic_Public_Ledger()
					x.Start_Ledger()
					if x.ChangeBlock == True:
						delay = 10
					elif x.ChangeBlock == False:
						delay = 5

					self.Echo = str(x.Calculate_Block().Block)
					HayStack().Refresh_Contact_List()
				except:
					print("\nThere appears to be a problem with your IRI node.\n")
					delay = 120

				for i in range(delay):
					sleep(1)
					if self.RunTime == False:
						print("Shutting down Dynamic Public Ledger...\n")
						break
			print("Dynamic Public Ledger... Offline\n")

		elif self.Function == "Sync_Messanger":
			while self.RunTime:
				x = Trusted_Paths()
				try:
					x.Catch_Up()
					self.Echo = x.Output
					x.Scan_Paths()
				except IOError:
					HayStack().Build_All_Directories()
				except:
					print("\nLikely BadApi error. Ignore this.\n")
				try:
					HayStack().Inbox()
					for i in range(10):
						sleep(1)
						if self.RunTime == False:
							config.RunTime = False
							print("Shutting down Messanger client...\n")
							break
				except KeyError:
					print("Error with Sync")
			print("Messanger client... Offline\n")

		elif self.Function == "Ping_Function":
			while self.RunTime:
				delay = 9999 #random.randint(120, 240)
				for i in range(delay):
					sleep(1)
					if self.RunTime == False:
						print("Shutting down ping function...")
						break
				if self.RunTime == True:
					try:
						HayStack().Ping_Function()
						print("\nPing has been sent.\n")
					except IndexError:
						print("\nPing Error...\n")
			print("Ping function... Offline")
		return self

	def Output(self):
		return self.Echo

	def Terminate(self):
		self.RunTime = False
		return self
