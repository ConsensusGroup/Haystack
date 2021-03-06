####################################################################################
############## This module is used to handle the inbox of the client ###############
####################################################################################

from User_Modules import Initialization
from Tools_Module import Tools
from Configuration_Module import Configuration
from DynamicPublicLedger_Module import Dynamic_Public_Ledger
from User_Modules import User_Profile
from IOTA_Module import IOTA_Module
from Contact_Module import Contact_Client

class Inbox_Manager(Initialization, Tools):
    def __init__(self):
        Initialization.__init__(self)
        Tools.__init__(self)
        Configuration.__init__(self)
        self.Received_Dir = str(self.InboxGenerator(Output_Directory = True).ReceivedMessages+"/"+Configuration().ReceivedMessages+".txt")
        self.Relayed_Dir = str(self.InboxGenerator(Output_Directory = True).RelayedMessages+"/"+Configuration().RelayedMessage+".txt")
        self.NotRelayed_Dir = str(self.InboxGenerator(Output_Directory = True).OutstandingRelay+"/"+Configuration().NotRelayedMessage+".txt")
	self.Message_Inbox = self.UserFolder+"/"+self.MessageFolder+"/"+Configuration().ReceivedMessages+"/"+self.Inbox+".txt"
    def Create_DB(self):
        #Here we check if the DB files are already written.
        self.Build_DB(File = self.Received_Dir)
        self.Build_DB(File = self.Relayed_Dir)
        self.Build_DB(File = self.NotRelayed_Dir)
        return self

    def Read_Tangle(self, IOTA_Instance, Block = "", From = "", To = ""):
        RelayedMessages_Dictionary = self.Read_From_Json(directory = self.Relayed_Dir)
        NotRelayed_Dictionary = self.Read_From_Json(directory = self.NotRelayed_Dir)

        if Block != "":
            Incoming = IOTA_Instance.Receive(Start = Block - self.Replay, Stop = Block + 1, JSON = True).Message
        elif From != To != "":
            Incoming = IOTA_Instance.Receive(Start = From, Stop = To, JSON = True).Message
        else:
            Incoming = []

        for i in Incoming:
            Bundle_Hash = str(i[0].get('bundle_hash'))
            Message_Received = i[1][1:len(i[1])-1]
            if self.Label_In_Dictionary(Input_Dictionary = RelayedMessages_Dictionary, Label = Bundle_Hash) == False:
                if self.Label_In_Dictionary(Input_Dictionary = NotRelayed_Dictionary, Label = Bundle_Hash) == False:
                    NotRelayed_Dictionary = self.Add_To_Dictionary(Input_Dictionary = NotRelayed_Dictionary, Entry_Label = Bundle_Hash, Entry_Value = Message_Received)

        #Now we write the dictionary to file.
        self.Write_To_Json(directory = self.NotRelayed_Dir, Dictionary = NotRelayed_Dictionary)
        return self

    def Postprocessing_Packet(self, ToSend, Hash_Of_Incoming_Tx, IOTA_Instance):
        Next_Address = ToSend[1]
        Cipher = ToSend[0]
        Relayed_Dictionary = self.Read_From_Json(directory = self.Relayed_Dir)
        NotRelayed_Dictionary = self.Read_From_Json(directory = self.NotRelayed_Dir)
        if Next_Address != '0'*81:
            Relayed_Bundle_Hash = str(IOTA_Instance.Send(ReceiverAddress = Next_Address, Message = Cipher))
            Relayed_Dictionary = self.Add_To_Dictionary(Input_Dictionary = Relayed_Dictionary, Entry_Label = Hash_Of_Incoming_Tx, Entry_Value = str(Relayed_Bundle_Hash))
            NotRelayed_Dictionary = self.Remove_From_Dictionary(Input_Dictionary = NotRelayed_Dictionary, Label = Hash_Of_Incoming_Tx)
        elif Next_Address == '0'*81:
            Relayed_Dictionary = self.Add_To_Dictionary(Input_Dictionary = Relayed_Dictionary, Entry_Label = Hash_Of_Incoming_Tx, Entry_Value = str('0'*81))
            NotRelayed_Dictionary = self.Remove_From_Dictionary(Input_Dictionary = NotRelayed_Dictionary, Label = Hash_Of_Incoming_Tx)

        self.Write_To_Json(directory = self.Relayed_Dir, Dictionary = Relayed_Dictionary)
        self.Write_To_Json(directory = self.NotRelayed_Dir, Dictionary = NotRelayed_Dictionary)
        return self

    def Addressed_To_Client(self, Message_PlainText, Symmetric_Message_Key):
        Client_Dictionary = self.Read_From_Json(directory = self.Received_Dir)
        if self.Label_In_Dictionary(Input_Dictionary = Client_Dictionary, Label = Message_PlainText) == False:
            self.Add_To_Dictionary(Input_Dictionary = Client_Dictionary, Entry_Label = Message_PlainText, Entry_Value = self.String_To_Base64(Symmetric_Message_Key))
            self.Write_To_Json(directory = self.Received_Dir, Dictionary = Client_Dictionary)
        return self

    def Completed_Messages(self, Input= []): #Add the message input later
        #First create the inbox DB
        self.Build_DB(File = self.Message_Inbox)
        Inbox = self.Read_From_Json(directory = self.Message_Inbox)
        Current_TangleTime = Dynamic_Public_Ledger().PublicIOTA.LatestTangleTime().TangleTime

        for i in Input:
            From_Address = i[0]
            try:
                hex = i[1].split(self.Identifier)
                int(hex,16)
                Ping = True
            except:
                Message = self.String_To_Base64(String = i[1])
                Ping = False

            if Ping == False:
                Inbox = self.Add_To_Dictionary(Input_Dictionary = Inbox, Entry_Label = Message, Entry_Value = From_Address)
                print("New Message!!!\n")
        self.Write_To_Json(directory = self.Message_Inbox, Dictionary = Inbox)
        return self

    def Reconstruction_Of_Message(self, Verify):
        #Make sure there is a file:
        self.Create_DB()

        #Read the file
        Client_Dictionary = self.Read_From_Json(directory = self.Received_Dir)
        Unique_SymKeys = []
        for i in Client_Dictionary.values():
            Unique_SymKeys.append(i)
        Unique_SymKeys = set(Unique_SymKeys)

        Message = []
        for i in Unique_SymKeys:
            Pieces_From_SymKey = []
            Unmodified_Labels = []
            for Cipher, Symkey in Client_Dictionary.items():
                if i == Symkey:
                    Pieces_From_SymKey.append(str(Cipher).replace(Configuration().MessageIdentifier,''))
                    Unmodified_Labels.append(str(Cipher))
            Sym_Key = self.Base64_To_String(str(i))
            Format_To_Digest = [Pieces_From_SymKey, Sym_Key]
            Output = Dynamic_Public_Ledger().Rebuild_Shrapnells(String = Format_To_Digest, Verify = Verify)
            if isinstance(Output, list):
                Message.append(Output)
                for z in Unmodified_Labels:
                    Client_Dictionary = self.Remove_From_Dictionary(Input_Dictionary = Client_Dictionary, Label = z)
                self.Write_To_Json(directory = self.Received_Dir, Dictionary = Client_Dictionary)

        self.Completed_Messages(Input = Message)
        if len(Message) == 0:
            return [[False, False, False]]
        else:
            return Message

    def Read_Stored_Messages(self):
        Dictionary = self.Read_From_Json(directory = self.Message_Inbox)
        Saved_Messages = self.Dictionary_To_List(Dictionary = Dictionary)
        Data = []
        for i in Saved_Messages:
            Message = self.Base64_To_String(Encoded = i[0])
            From_Address = i[1]

            #Now check if the address is in the address book.
            Output = Contact_Client().Retrieve_UserName_From_Address(Address_To_Search = From_Address)
            if Output == False:
                User = From_Address
            elif isinstance(Output, list):
                User = str(Output[0]+" ("+From_Address+")")
            Data.append([Message, User])
        return Data

class Trusted_Paths(Tools, Configuration, User_Profile):
	def __init__(self):
		Tools.__init__(self)
		Configuration.__init__(self)
		User_Profile.__init__(self)
		self.Ledger_Accounts_Dir = str(self.UserFolder+"/"+self.PathFolder+"/"+self.Ledger_Accounts_File)
		self.Last_Block_Dir = str(self.UserFolder+"/"+self.PathFolder+"/"+self.Last_Block)
		self.Ping_Dir = str(self.UserFolder+"/"+self.PathFolder+"/"+self.Trajectory_Ping)
		self.Incoming_Shrapnells = str(self.UserFolder+"/"+self.MessageFolder+"/"+Configuration().ReceivedMessages+"/"+Configuration().ReceivedMessages+".txt")
		self.TrustedNodes_Dir = str(self.UserFolder+"/"+self.PathFolder+"/"+self.Trusted_Nodes)
		self.Current_Block = Dynamic_Public_Ledger().Calculate_Block().Block
		self.PrivateIOTA = IOTA_Module(Seed = self.Private_Seed)

	def Build_LedgerDB(self):
		self.Build_Directory(directory = str(self.UserFolder+"/"+self.PathFolder))
		self.Build_DB(File = self.Ledger_Accounts_Dir)
		self.Build_DB(File = self.Last_Block_Dir)
		self.Build_DB(File = self.Ping_Dir)

		#Read the file when the user was last online
		Block_Number = self.Read_From_Json(directory = self.Last_Block_Dir)

		#If the dictionary is empty
		if Block_Number == {}:
			Block_Number = self.Add_To_Dictionary(Input_Dictionary = Block_Number, Entry_Label = "Block", Entry_Value = self.Current_Block)
			self.Write_To_Json(directory = self.Last_Block_Dir, Dictionary = Block_Number)
			self.Last_Block_Online = self.Current_Block
		else:
			self.Last_Block_Online = Block_Number["Block"]
		return self

	def Catch_Up(self):
		self.Build_LedgerDB()
		Accounts = self.Read_From_Json(directory = self.Ledger_Accounts_Dir)
		if self.Last_Block_Online != self.Current_Block:
			self.Write_To_Json(directory = str(self.UserFolder+"/"+self.PathFolder+"/"+self.Current_Ledger_Accounts), Dictionary = {})
			self.Write_To_Json(directory = self.TrustedNodes_Dir, Dictionary = {})
			self.Write_To_Json(directory = self.Ping_Dir, Dictionary = {})

		self.Last_Block_Online = self.Last_Block_Online-1
		BlockDifference = int(self.Current_Block - self.Last_Block_Online)
		if BlockDifference >= self.Replay:
			Upperbound_Block = self.Last_Block_Online + self.Replay
			Sync = "Syncing node."
		else:
			Upperbound_Block = self.Last_Block_Online + BlockDifference
			if BlockDifference == 1:
				Sync = "Node synced."
			else:
				Sync = "Syncing node."

		for i in Dynamic_Public_Ledger().Check_User_In_Ledger(ScanAll = True, From = self.Last_Block_Online, To = Upperbound_Block).All_Accounts:
			Accounts = self.Add_To_Dictionary(Input_Dictionary = Accounts, Entry_Label = i[0], Entry_Value = i[1])

		self.Write_To_Json(directory = self.Ledger_Accounts_Dir, Dictionary = Accounts)
		Inbox_Manager().Read_Tangle(IOTA_Instance = self.PrivateIOTA, From = self.Last_Block_Online-2, To = Upperbound_Block)
		self.Write_To_Json(directory = self.Last_Block_Dir, Dictionary = self.Add_To_Dictionary(Input_Dictionary = {}, Entry_Label = "Block", Entry_Value = Upperbound_Block))
		self.Output = str("Scanning from: "+str(self.Last_Block_Online) + " To: "+str(Upperbound_Block)+" Status: "+Sync)
		self.Last_Block_Online = Upperbound_Block

		if self.Current_Block == self.Last_Block_Online:
			Inbox_Manager().Read_Tangle(IOTA_Instance = self.PrivateIOTA, Block = self.Current_Block)

		return self

	def Scan_Paths(self):
		self.Build_DB(File = self.TrustedNodes_Dir)
		Pings = self.Read_From_Json(directory = self.Ping_Dir)
		Shrapnells = self.Read_From_Json(directory = self.Incoming_Shrapnells)
		Pings_List = self.Dictionary_To_List(Dictionary = Pings)
		Shrapnells_List = self.Dictionary_To_List(Dictionary = Shrapnells)
		Found_Pings = []

		#Search for ping fragments in the message bank and record them.
		for i in Shrapnells_List:
			for ping in Pings_List:
				if ping[0] in i[0]:
					Found_Pings.append(ping[0])

		#Split the ping string to find non lazy addresses
		Trusted_Nodes = []
		for entry in Found_Pings:
			String_split = Pings[entry].split("-->")
			Block = String_split.pop(0)
			Temp = []
			for node in String_split:
				if node == "LOCALCLIENT":
					Break = True
				else:
					Break = False
					Temp.append([node, Block])
				if Break == True:
					for i in Temp:
						Trusted_Nodes.append(i)


		#Read current DB
		Nodes_Dictionary = self.Read_From_Json(directory = self.TrustedNodes_Dir)
		for i in Trusted_Nodes:
			Nodes_Dictionary = self.Add_To_Dictionary(Input_Dictionary = Nodes_Dictionary, Entry_Label = str(i[0]), Entry_Value = i[1])

		self.Write_To_Json(directory = self.TrustedNodes_Dir, Dictionary = Nodes_Dictionary)
		return self
