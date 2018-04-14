import json

class Contacts(object):
	def __init__(self, FirstName, Address, Messages):
		self.FirstName = FirstName
		self.Address = Address
		self.Messages = Messages

class SearchFile:
	def __init__(self, database):
		self.DataBase = database
		self.Results = []

	def Search(self, Keyword):
		for i in self.DataBase:
			for z in self.DataBase[i].keys():
				if Keyword in self.DataBase[i].get(z):
					self.Results.append(self.DataBase[i])
		return self




Messages = ["sdfsdfdsdfsdfds", "asdfsadfdssdf", "dsdfsdfsd0", "adsfsddf"]
Names = ["Cooper", "Kevin", "Hendrik", "Samim"]
Addresses = ["xxx","lll", "zzzz", "zxxx"]

#Dic = {}
#for i in range(len(Names)):
#	dic = Contacts(FirstName = Names[i], Address = Addresses[i], Messages = Messages).__dict__
#	Dic[i]=dic

#with open("data.json", "w") as outfile:
#	json.dump(Dic, outfile)

data = open("data.json").read()
Entry = json.loads(data)
Key = "Cooper"
print(SearchFile(database = Entry).Search(Keyword = Key).Results)





