####################################################################################
#In this module we build directories and files needed for the application to work ##
####################################################################################

from Configuration_Module import Configuration
from Tools_Module import Tools 
from Cryptography_Module import Key_Generation, os, Encryption, Decryption
from IOTA_Module import Seed_Generator


class Initialization(Configuration, Tools):
	def __init__(self):
		Configuration.__init__(self)
		Tools.__init__(self)

	def Build_Application(self):
		Continue = False
		UserSuccess = self.Build_Directory(directory = self.UserFolder)
		KeySuccess = self.Build_Directory(directory = str(self.UserFolder+"/"+self.KeysFolder))
		PrivateSeedSuccess = self.Build_Directory(directory = str(self.UserFolder+"/"+self.SeedFolder))
		if UserSuccess == KeySuccess == PrivateSeedSuccess == True:
			Continue = True
		elif UserSuccess == KeySuccess == PrivateSeedSuccess == None: 
			Continue = True
		else: 
			Continue = False
		return Continue
	
	def Account(self):
		if self.Check_File(File = str(self.UserFolder+"/"+self.KeysFolder+"/"+self.PrivateKey)) == False:
			self.Write(directory = str(self.UserFolder+"/"+self.KeysFolder+"/"+self.PrivateKey), data = Key_Generation().Asymmetric_KeyGen().PrivateKey)
			
		if self.Check_File(File = str(self.UserFolder+"/"+self.SeedFolder+"/"+self.PrivateSeed)) == False:
			Private_Seed = Seed_Generator()
			Cipher_PrivateSeed = Encryption().AsymmetricEncryption(PlainText = Private_Seed, PublicKey = Key_Generation().PrivateKey_Import().PublicKey)
			self.Write(directory = str(self.UserFolder+"/"+self.SeedFolder+"/"+self.PrivateSeed), data = Cipher_PrivateSeed)
		return self

class User_Profile(Initialization):
	def __init__(self):
		Start = Initialization()
		Continue = Start.Build_Application()
		if Continue == True:
			Start.Account()
			Keys = Key_Generation().PrivateKey_Import()
			Private_Seed_Encrypted = Tools().List_To_String(List = Tools().ReadLine(directory = str(self.UserFolder+"/"+self.SeedFolder+"/"+self.PrivateSeed)))
			self.PrivateKey = Keys.PrivateKey
			self.PublicKey = Keys.PublicKey
			self.Private_Seed = Decryption().AsymmetricDecryption(CipherText = Private_Seed_Encrypted, PrivateKey = self.PrivateKey)
		else:
			print("Permission Error")
