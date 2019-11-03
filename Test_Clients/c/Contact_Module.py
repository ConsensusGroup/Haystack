####################################################################################
##################### This script handles the client Contacts ######################
####################################################################################



from Configuration_Module import Configuration
from Tools_Module import Tools
from DynamicPublicLedger_Module import Dynamic_Public_Ledger
import ast

class Contact_Client(Configuration, Tools):
	def __init__(self):
		Configuration.__init__(self)
		Tools.__init__(self)

		#Core directory objects
		self.Contact_Folder_Dir = str(self.UserFolder+"/"+self.Contacts_Folder)
		self.Contacts_File_Dir = str(self.Contact_Folder_Dir+"/"+self.Contacts_File)

	def Build_ContactDB(self):
		self.Build_Directory(directory = self.Contact_Folder_Dir)
		self.Build_DB(File =self.Contacts_File_Dir)
		return self

	def Link_Address_To_PubKey(self, Address_To_Search = "0"*81, Public_Key_To_Search = "", User_Name = ""):
		All_Ledger_DB = Dynamic_Public_Ledger().Check_User_In_Ledger(ScanAll = True).All_Accounts
		self.Public_Key_Found = "0"*81
		self.Other_Identities = []
		self.Saved = False
		if isinstance(All_Ledger_DB, list) == True:
			if Address_To_Search != "0"*81:
				for i in All_Ledger_DB:
					Address = i[0]
					PubKey = i[1]
					if Address == Address_To_Search:
						self.Public_Key_Found = PubKey
			elif Public_Key_To_Search != "":
				self.Public_Key_Found = Public_Key_To_Search

			Temp_List = []
			for i in All_Ledger_DB:
				if i[1] == self.Public_Key_Found:
					Temp_List.append(i[0])
			self.Other_Identities = [self.Public_Key_Found, Temp_List]

			if User_Name != "" and len(self.Other_Identities) != 0:
				Contact_List = self.Read_From_Json(directory = self.Contacts_File_Dir)
				if self.Label_In_Dictionary(Input_Dictionary = Contact_List, Label = User_Name) == False:
					Contact_List = self.Add_To_Dictionary(Input_Dictionary = Contact_List, Entry_Label = User_Name, Entry_Value = str(self.Other_Identities))
					self.Write_To_Json(directory = self.Contacts_File_Dir, Dictionary = Contact_List)
					self.Saved = True
		return self

	def Delete_From_Contacts(self, User_Name):
		Contact_List = self.Read_From_Json(directory = self.Contacts_File_Dir)
		Contact_List = self.Remove_From_Dictionary(Input_Dictionary = Contact_List, Label = User_Name)
		self.Write_To_Json(directory = self.Contacts_File_Dir, Dictionary = Contact_List)
		return self

	def Retrieve_UserName_From_Address(self, Address_To_Search):
		Contact_List = self.Read_From_Json(directory = self.Contacts_File_Dir)
		Present = False
		Contact_List_Dic = Contact_List

		#First check if the Address is in the contact list.
		Contact_List = self.Dictionary_To_List(Dictionary = Contact_List)
		for i in Contact_List:
			Username = i[0]
			Identities = ast.literal_eval(i[1])
			PubKey = Identities[0]
			for z in Identities[1]:
				if Address_To_Search == z:
					Present = True
					PublicKey = PubKey
					User_Name = Username

		#Now if the address is not in the contact list check the global ledger again for an update on the identity.
		if Present == False:
			User_Name = ""
			Address = self.Link_Address_To_PubKey(Address_To_Search = Address_To_Search)
			if Address.Public_Key_Found != "0"*81:
				Public = Address.Other_Identities[0]
				for i in Contact_List:
					Username = i[0]
					Identities = ast.literal_eval(i[1])
					if Public == Identities[0]:
						User_Name = Username
						Contact_List_Dic = self.Add_To_Dictionary(Input_Dictionary = Contact_List_Dic, Entry_Label = Username, Entry_Value = str(Address.Other_Identities))
				if User_Name != "":
					self.Write_To_Json(directory = self.Contacts_File_Dir, Dictionary = Contact_List_Dic)
					return [User_Name, Public, True]
				else:
					return False
			else:
				return False
		else:
			return [User_Name, PublicKey, Present]

	def Update_Contacts(self):
		for i in Dynamic_Public_Ledger().Check_User_In_Ledger(ScanAll = True).All_Accounts:
			Address = i[0]
			self.Retrieve_UserName_From_Address(Address_To_Search = Address)
		return self
