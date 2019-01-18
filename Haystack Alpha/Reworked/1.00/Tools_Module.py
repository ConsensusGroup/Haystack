####################################################################################
######### This module has some useful tools used for the Haystack protocol #########
####################################################################################

from Configuration_Module import Configuration
import os

class Tools(Configuration):

	def Write(self, directory, data, setting = "wb"):
		f = open(directory, setting)
		f.write(data)
		f.close()

	def ReadLine(self, directory, setting = "r"):
		data = []
		for i in open(directory, setting):
			data.append(i)
		return data

	def Normalize(self, string):
		normaltext = str(string) + (self.Default_Size - len(string) - len(self.Identifier)) * str(' ') + str(self.Identifier)
		return normaltext

	def Split(self, string):
		return [string[start:start+self.Default_Size] for start in range(0, len(string), self.Default_Size)]

	def List_To_String(self, List):
		return ''.join(List)

	def Build_Directory(self, directory):
		if not os.path.exists(directory):
			try:
				os.makedirs(directory)
				return True
			except OSError:
				return False
		if os.path.exists(directory) == True:
			return None

	def Check_File(self, File):
		if not os.path.exists(File):
			return False
		else:
			return True