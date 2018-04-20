from HayStackAPI import *

#Kivy API
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

#Multi Threading 
import threading
from multiprocessing import Pipe

#OS imports
from os import listdir
from time import sleep
import json

refresh_rate = 5

##### Other Classes ########
class Contacts(object):
	def __init__(self, FirstName = "", LastName = "", Address = "", Messages = "", PublicKey = ""):
		self.FirstName = FirstName
		self.LastName = LastName
		self.Address = Address
		self.Messages = Messages
		self.PublicKey = PublicKey

class DataBaseManager:
	def __init__(self):
		self.ContactJson = "Contacts.json"
		self.Root = "UserData"
		self.DataBaseDir = str(self.Root+"/"+self.ContactJson)
		self.DataBase = {}
		self.Results = []

	def Read(self):
		try:
			data = open(self.DataBaseDir).read()
			self.DataBase = json.loads(data)
		except:
			pass
		return self	
	
	def Write(self):
		try:
			with open(self.DataBaseDir, "w") as outfile:
				json.dump(self.DataBase, outfile)
		except:
			pass
		return self		

	def SearchDatabase(self, Keyword):
		self.Read()
		for i in self.DataBase:
			for z in self.DataBase[i].keys():
				if Keyword in self.DataBase[i].get(z):
					self.Results.append(self.DataBase[i])
		return self

	def AddToDataBase(self):
		Index = len(self.DataBase)
		self.DataBase[Index] = self.Dictionary
		self.Write()
		return self

	def RemoveFromDataBase(self, Dictionary):
		Temp = {}
		x = 0
		for i in self.DataBase:
			if Dictionary in i:
				pass
			else:
				Temp[x] = i
				x = x+1
		self.DataBase = Temp
		self.Write()
		return self

	def ObjectToDictionary(self, ObjectInstance):
		self.Dictionary = ObjectInstance.__dict__
		return self

Instance = DataBaseManager()
Instance.Read()

##### Main Logic Commands ##########

class LogicCommands(Configuration):
	def __init__(self):
		Configuration.__init__(self)

	def ReadLogin(self, UserName, Password):
		Start(Password = Password)
		try:
			User_Profile().PrivateKey
			self.Result = True
		except:
			self.Result = False
		return self
	def ShutDown(self):
		App.get_running_app().stop()

	def ReadRegister(self, UserName, Password, Password2):
		if Password == Password2 and Password != "" and UserName != "":
			self.data  = True
			Client = Initialization()
			Start(Password = Password)
			Client.Build_Directory()
			Client.Build_Files()
		elif Password != Password2 or Password == "":
			self.data = "PassError"
		elif UserName == "":
			self.data = "UserError"
		return self

	def ReadInput(self, Text, Function):
		self.Found = []
		if Function == "Contact":
			Dictionary = Instance.SearchDatabase(Keyword = Text).Results
			for entries in Dictionary:
				if (str(Text) in (str(entries.get("FirstName")) or str(entries.get("LastName")))) and str(Text) != "":
					string = str(entries.get("FirstName")+" "+entries.get("LastName"))
					if string not in self.Found:
						self.Found.append(string)
		return self

	def On_Type(self):
		for i in self.History:
			self.ids.ContactsList.remove_widget(i)

		for i in self.Found:			
			self.btn = Button(text = str(i), size_hint_y = None, height=10)
			self.btn.bind(on_press = self.btn_pressed)
			self.ids.ContactsList.add_widget(self.btn)
			self.History.append(self.btn)	
		return self

	def btn_pressed(self, instance):
	    print(instance.text)

	def All_Contacts(self, *args):
		Instance.Read()
		for i in Instance.DataBase:
			Entries = Instance.DataBase.get(i)
			FirstName = Entries.get("FirstName")
			LastName = Entries.get("LastName")
			Address = Entries.get("Address")
			string = str(FirstName+" "+LastName+" ("+Address+")")
			if string not in self.History:
				self.btn = Button(text = string, size_hint_y = None, height=10, font_size = 20, valign = "middle")
				self.btn.bind(on_press = self.btn_pressed)
				self.ids.UserContacts.add_widget(self.btn)
				self.History.append(string)
		return self

	def Add_Contact(self, FirstName, LastName, Address):
		self.Pass = False
		if FirstName != "" and LastName != "" and Address != "":
			ToAdd = Contacts(FirstName = FirstName, LastName = LastName, Address = Address)
			Instance.ObjectToDictionary(ObjectInstance = ToAdd)
			Instance.AddToDataBase()
			self.Pass = True
		else:
			self.Pass = "LabelAddress"
		return self

	def Message_Inbox(self,*args):
		List = []
		try:
			for i in Instance.DataBase:
				keys = Instance.DataBase.get(i)
				LastMessage = keys.get("Messages")
				UserFirstName = keys.get("FirstName")
				UserLastName = keys.get("LastName")
				if LastMessage != "":
					string = str("     "+UserFirstName+" "+UserLastName+": "+LastMessage)
					List.append(string)
		except:
			pass

		for i in List:
			self.btn = Button(text = i, size_hint_y = None, height=10, font_size = 20, valign = "middle")
			self.btn.bind(size = self.btn.setter('text_size'))
			self.btn.bind(on_press = self.btn_pressed)
			self.ids.MessageList.add_widget(self.btn)
			self.History.append(self.btn)	
		return self

	def BlockUpdate(self, *args):
		ChangeBlock = False
		try:
			Dynamics = Dynamic_Ledger()
			CurrentBlock = Dynamics.CalculateBlock().Block
			ChangeBlock = Dynamics.CalculateBlock().NewBlock
			self.ids.StatusLabel.text = str("Block: "+str(CurrentBlock))
		except:
			pass

		try:
			if ChangeBlock == True:
				PublicLedger = Dynamics.UpdateLedger()
		except:
			pass

		return self

######### Screens ##########
#------ Login Windows -----------#
class LoginWindow(Screen):
	def __init__(self, **kwargs):
		super(LoginWindow, self).__init__(**kwargs)
		self.Login = LoginWidget()
		self.add_widget(self.Login)

class LoginWidget(Widget, LogicCommands):
	pass

class RegisterWindow(Screen):
	def __init__(self, **kwargs):
		super(RegisterWindow, self).__init__(**kwargs)
		self.Register = RegisterWidget()
		self.add_widget(self.Register)

class RegisterWidget(Widget,LogicCommands):
	pass

#------ Messanger Windows -----------#
class MessangerWindow(Screen):
	def __init__(self, **kwargs):
		super(MessangerWindow, self).__init__(**kwargs)
		self.Messanger = MessangerWidget()
		self.add_widget(self.Messanger)

class MessangerWidget(BoxLayout, LogicCommands):
	def __init__(self):
		BoxLayout.__init__(self)
		LogicCommands.__init__(self)
		self.History = []
		Clock.schedule_interval(self.BlockUpdate, refresh_rate)
		Clock.schedule_interval(self.Message_Inbox, refresh_rate)

class NewMessageWindow(Screen):
	def __init__(self, **kwargs):
		super(NewMessageWindow, self).__init__(**kwargs)
		self.NewMessage = NewMessageWidget()
		self.add_widget(self.NewMessage)
		
class NewMessageWidget(Widget, LogicCommands):
	def __init__(self):
		Widget.__init__(self)
		LogicCommands.__init__(self)
		self.History = []
		Clock.schedule_interval(self.BlockUpdate, refresh_rate)

#------- Contacts Window ------------#
class ContactWindow(Screen):
	def __init__(self, **kwargs):
		super(ContactWindow, self).__init__(**kwargs)
		self.Contact = ContactsLayout()
		self.History = []
		self.add_widget(self.Contact)


class ContactsLayout(BoxLayout, LogicCommands):
	def __init__(self):
		BoxLayout.__init__(self)
		LogicCommands.__init__(self)
		self.History = []
		self.All_Contacts()
		Clock.schedule_interval(self.BlockUpdate, refresh_rate)

class NewContactWindow(Screen):
	def __init__(self, **kwargs):
		super(NewContactWindow,self).__init__(**kwargs)
		self.AddContact = AddContactLayout()
		self.add_widget(self.AddContact)

class AddContactLayout(BoxLayout, LogicCommands):
	def __init__(self):
		BoxLayout.__init__(self)
		LogicCommands.__init__(self)
		Clock.schedule_interval(self.BlockUpdate, refresh_rate)

##################################


class KivyConfig:
	def __init__(self):
		self.KivyPath = "./Kivy/"

	def ReadConfig(self):
		for i in listdir(self.KivyPath):
			Builder.load_file(self.KivyPath+ i)

	def ScreenLoader(self):
		self.sm = ScreenManager()
		self.sm.add_widget(LoginWindow(name = "Login"))
		self.sm.add_widget(RegisterWindow(name = "Register"))
		self.sm.add_widget(MessangerWindow(name = "Messanger"))
		self.sm.add_widget(NewMessageWindow(name = "NewMessage"))
		self.sm.add_widget(ContactWindow(name = "Contacts"))
		self.sm.add_widget(NewContactWindow(name = "NewContact"))
		return self

###### Build Main ########
class MainApp(App):

	def build(self):
		self.title = "Conensus-Haystack"
		return KivyConfig().ScreenLoader().sm

######### Start the app ##########
if __name__ == "__main__":

	KivyConfig().ReadConfig()
	app = MainApp()
	app.run()
