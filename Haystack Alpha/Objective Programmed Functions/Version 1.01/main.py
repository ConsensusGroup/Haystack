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

refresh_rate = 5

##### Main Logic Commands ##########
class LogicCommands(Configuration):
	def __init__(self):
		Configuration.__init__(self)

	def ReadLogin(self, UserName, Password):
		Start(Password = Password)
		try:
			User_Profile().PrivateKey
			self.Result = True
		except ValueError:
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

	def Search(self, List, Element):
		matches = []
		for i in List:
			if str(Element) in i and i not in matches and str(Element) != "":
				matches.append(i)
		return matches

	def ReadInput(self, Text, Function):
		self.Found = []
		if Function == "Contact":
			List = ["Cooper", "Cooper", "Kevin", "Hendrik", "Samim"]
			self.Found = self.Search(List = List, Element = Text)
		return self

	def On_Type(self):
		for i in self.History:
			self.ids.ContactsList.remove_widget(i)

		for i in self.Found:			
			self.btn = Button(text = i, size_hint_y = None, height=10)
			self.btn.bind(on_press = self.btn_pressed)
			self.ids.ContactsList.add_widget(self.btn)
			self.History.append(self.btn)	
		return self

	def btn_pressed(self, instance):
	    print(instance.text)
	    #threading.Thread(target = self.IOTA).start()

	def Message_Inbox(self):
		List = ["Cooper", "Cooper", "Kevin", "Hendrik", "Samim"]
		for i in List:
			self.btn = Button(text = i, size_hint_y = None, height=10)
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
		except ValueError:
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
		self.Message_Inbox()
		Clock.schedule_interval(self.BlockUpdate, refresh_rate)


class NewMessageWindow(Screen):
	def __init__(self, **kwargs):
		super(NewMessageWindow, self).__init__(**kwargs)
		self.NewMessage = NewMessageWidget()
		self.add_widget(self.NewMessage)
		
class NewMessageWidget(Widget, LogicCommands):
	def __init__(self):
		Widget.__init__(self)
		LogicCommands.__init__(self)
		Clock.schedule_interval(self.BlockUpdate, refresh_rate)
		self.History = []
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
