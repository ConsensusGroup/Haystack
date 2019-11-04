####################################################################################
#################### This script is intended to serve as an API ####################
####################################################################################


from DynamicPublicLedger_Module import Dynamic_Public_Ledger
from Contact_Module import Contact_Client
from User_Modules import Initialization, User_Profile
from Inbox_Module import Inbox_Manager, Trusted_Paths
from Haystack_Module import Sender_Client, Receiver_Client
from Configuration_Module import Configuration

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
		Contact_Client().Build_Directory()
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




	######################################## Work in progress for later ##########################################
	# def Sync_To_Lastest_Block(self):
	# 	for i in Trusted_Paths().Catch_Up():
	# 		print(i)
	#
	# def Return_Trusted_Paths(self):
	# 	## # TODO: Write a script that reads back all the checked nodes
	# 	return self
	#
	# def Start_Ledger(self):
	# 	Dynamic_Public_Ledger().Start_Ledger()
	# 	return self
	#
	# def Run_HayStack_Client(self):
	# 	global RunTime
	# 	RunTime = True
	# 	self.Build_All_Directories()
	# 	For_Ping = 1
	# 	while RunTime == True:
	# 		if "0" == str(float(For_Ping)/float(Configuration().Ping_Rate)).split(".")[1]:
	# 			self.Ping_Function()
	# 			print("Sending Ping @: "+str(For_Ping))
	# 		For_Ping = For_Ping +1
	# 		Dynamic_Public_Ledger().Start_Ledger()
	# 		Trusted_Paths().Catch_Up()
	# 		#Trusted_Paths().Scan_Paths()
	# 		Message = Receiver_Client().Check_Inbox()
	# 		Message = Message.Incoming_Message
	# 		print(Message)
	#
	# 		for i in Message:
	# 			try:
	# 				if i[0] != False:
	# 					print("Passed!"+ "\n Message From:	 " + str(i[0]) + "\n Message:	 "+ str(i[1]))
	# 				else:
	# 					print("No New Message for you.....")
	# 			except:
	# 				print("No New Message for you.")
	# 		sleep(Configuration().RefreshRate)
	#
	#
	#
	#
	# 	return self
	# 
