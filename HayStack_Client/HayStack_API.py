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
		#Output = [PublicKey(string), known by other addresses(list)]
		return Identities

	def Delete_From_Contacts(self, Username):
		Contact_Client().Delete_From_Contacts(User_Name = Username)
		#Output = Nothing
		return self

	def Username_From_Address(self, Address):
		Output = Contact_Client().Retrieve_UserName_From_Address(Address_To_Search = Address)
		#if Address in contact list; --> Output = [Saved Username (string), PublicKey(string), Has the address been found? (Bool)] otherwise a simple False(bool) will be returned
		return Output

	def Refresh_Contact_List(self):
		Contact_Client().Update_Contacts()
		#Output = Nothing
		return self

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


##### This section of the API is responsible for running background services
class Run_HayStack_Client(threading.Thread):
	def __init__(self, Function):
		threading.Thread.__init__(self)
		self.RunTime = True
		self.Function = Function
		self.Echo = ""

	def run(self):
		z = 0
		if self.Function == "Dynamic_Public_Ledger":
			while self.RunTime:
				x = Dynamic_Public_Ledger()
				x.Start_Ledger()
				if x.ChangeBlock == True:
					delay = 10
				elif x.ChangeBlock == False:
					delay = 5

				self.Echo = str(x.Calculate_Block().Block)
				HayStack().Refresh_Contact_List()
				for i in range(delay):
					sleep(1)
					if self.RunTime == False:
						break

		elif self.Function == "Sync_Messanger":
			while self.RunTime:
				x = Trusted_Paths()
				x.Catch_Up()
				self.Echo = x.Output
				HayStack().Inbox()
				for i in range(10):
					sleep(1)
					if self.RunTime == False:
						break

				x.Scan_Paths()

		elif self.Function == "Ping_Function":
			while self.RunTime:
				try:
					HayStack().Ping_Function()
				except IndexError:
					print("Error...")
				delay = random.randint(1, 240)
				for i in range(delay):
					sleep(1)
					if self.RunTime == False:
						break
		return self

	def Output(self):
		return self.Echo

	def Terminate(self):
		self.RunTime = False
		return self
