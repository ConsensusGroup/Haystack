####################################################################################
######### This module has some useful tools used for the Haystack protocol #########
####################################################################################

from Configuration_Module import Configuration
import os
import json
from base64 import b64encode, b64decode

class Tools(Configuration):

	#Simple file/directory manipulation
	def Write(self, directory, data, setting = "wb"):
		f = open(directory, setting)
		f.write(data)
		f.close()

	def ReadLine(self, directory, setting = "r"):
		data = []
		for i in open(directory, setting):
			data.append(i)
		return data

	def Check_File(self, File):
		if not os.path.exists(File):
			return False
		else:
			return True

	def Build_Directory(self, directory, Return_Dir = False):
		if Return_Dir == False:
			if not os.path.exists(directory):
				try:
					os.makedirs(directory)
					return True
				except OSError:
					return False
			if os.path.exists(directory) == True:
				return None
		elif Return_Dir == True:
			return directory

	def Build_DB(self, File):
		Empty_Dictionary = {}
		if self.Check_File(File = File) == False:
			self.Write_To_Json(directory = File, Dictionary = Empty_Dictionary, setting = "w+")

	def Split(self, string, length = Configuration().Default_Size):
		return [string[start:start+length] for start in range(0, len(string), length)]

	def List_To_String(self, List):
		return ''.join(List)

	#This section is the dictionary functions.
	def Write_To_Json(self, directory, Dictionary, setting = "wb"):
		with open(directory, setting) as file:
			file.write(json.dumps(Dictionary))
		return self

	def Read_From_Json(self, directory, setting = "r"):
		Dictionary = json.load(open(directory, setting))
		return Dictionary

	def Entry_In_Dictionary(self, Input_Dictionary, Entry):
		Present = Entry in Input_Dictionary.values()
		return Present

	def Label_In_Dictionary(self, Input_Dictionary, Label):
		Present = Label in Input_Dictionary
		return Present

	def Add_To_Dictionary(self, Input_Dictionary, Entry_Label, Entry_Value):
		Input_Dictionary[Entry_Label] = Entry_Value
		return Input_Dictionary

	def Remove_From_Dictionary(self, Input_Dictionary, Label):
		Input_Dictionary.pop(Label)
		return Input_Dictionary

	def NonAsciiEncode(self, string):
		converted = unicode(string, "utf-8").encode('unicode_escape')
		return converted

	def ToNonAsciiDecode(self, string):
		converted = unicode(string, "utf-8").decode('unicode_escape')
		return converted

	def String_To_Base64(self, String):
		return b64encode(String)

	def Base64_To_String(self, Encoded):
		return b64decode(Encoded)
