####################################################################################
#################### This script is intended to serve as an API ####################
####################################################################################


from DynamicPublicLedger_Module import Dynamic_Public_Ledger
from IOTA_Module import Return_Fastest_Node
from Contact_Module import Contact_Client
from User_Modules import Initialization, User_Profile
from Inbox_Module import Inbox_Manager, Trusted_Paths
from Haystack_Module import Sender_Client, Receiver_Client
from Configuration_Module import Configuration
from NodeFinder_Module import Node_Finder
import config
import threading
from time import sleep
import random
import sys

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

	def Build_All_Directories(self, Restore = False):
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

	def Fastest_Node(self):
		Output = Return_Fastest_Node()
		#Output: Dictionary with "Send" and "Receive" string.
		return Output

	def Last_Online_Block(self):
		Output =  Trusted_Paths().Build_LedgerDB().Last_Block_Online
		#Output: Integer
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
			delay = 30
			print("Please wait whilst HayStack searches for nodes.")
			while self.RunTime:
				for i in range(delay):
					sleep(1)
					if self.RunTime == False:
						print("Shutting down Dynamic Public Ledger...\n")
						break
				try:
					x = Dynamic_Public_Ledger()
					x.Start_Ledger()
					if x.ChangeBlock == True:
						delay = 10
					elif x.ChangeBlock == False:
						delay = 20

					self.Echo = str(x.Calculate_Block().Block)
					HayStack().Refresh_Contact_List()
				except IOError:
					try:
						HayStack().Build_All_Directories()
						delay = 30
					except:
						print("Connection Error. You are not online")
						delay = 30
				except:
					if "BadApiResponse: 400 response from node:" in str(sys.exc_info()[0]):
						print("Your IOTA node is not in sync.")

			print("Dynamic Public Ledger... Offline\n")

		elif self.Function == "Sync_Messanger":
			delay = 30
			while self.RunTime:

				for i in range(delay):
					sleep(1)
					if self.RunTime == False:
						config.RunTime = False
						print("Shutting down Messanger client...\n")
						break
				try:
					x = Trusted_Paths()
					x.Catch_Up()
					self.Echo = x.Output
					x.Scan_Paths()
				except IOError:
					try:
						HayStack().Build_All_Directories()
					except:
						if "ConnectionError: HTTPConnectionPool" in str(sys.exc_info()[0]):
							print("Connection Error. You are not online")
				except:
					pass
				try:
					HayStack().Inbox()
				except KeyError:
					print("Error with Sync")
				except:
					if "ConnectionError: HTTPConnectionPool" in str(sys.exc_info()[0]):
						print("Connection Error. You are not online")

				delay = 10
			print("Messanger client... Offline\n")

		elif self.Function == "Ping_Function":
			while self.RunTime:
				delay = random.randint(120, 999)
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
					except:
						pass

			print("Ping function... Offline")

		elif self.Function == "Node_Testing":
			while self.RunTime == True:
				Node_Finder().Test_Nodes()
				for i in range(30):
					if self.RunTime == False:
						print("Shutting down node finder...")
						break
					else:
						sleep(1)
			print("Node finder... Offline...")
		return self

	def Output(self):
		return self.Echo

	def Terminate(self):
		self.RunTime = False
		config.RunTime = False
		return self
