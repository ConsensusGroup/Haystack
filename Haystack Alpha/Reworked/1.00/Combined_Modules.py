####################################################################################
#In this module we build directories and files needed for the application to work ##
####################################################################################

from Configuration_Module import Configuration
from Tools_Module import Tools 
from Cryptography_Module import Key_Generation, os

class Initialization(Configuration, Tools):
	def __init__(self):
		Configuration.__init__(self)
		Tools.__init__(self)

	def Build_Application(self):
		UserSuccess = self.Build_Directory(directory = self.UserFolder)
		KeySuccess = self.Build_Directory(directory = str(self.UserFolder+"/"+self.KeysFolder))
		PrivateSeedSuccess = self.Build_Directory(directory = str(self.UserFolder+"/"+self.SeedFolder))
		if UserSuccess == KeySuccess == PrivateSeedSuccess == True:
			Continue = True
		elif UserSuccess == KeySuccess == PrivateSeedSuccess == None:
			Continue = True
		else:
			Continue = False

		#Continue here with the key generation of the RSA and Seed 

print(Initialization().Build_Application())
