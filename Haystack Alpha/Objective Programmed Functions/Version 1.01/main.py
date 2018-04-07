from HayStackAPI import Configuration

#Kivy API
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

#OS imports
from os import listdir

##### Main Logic Commands ##########
class LogicCommands:
	def __init__(self):
		pass
	def ReadLogin(self, UserName, Password):
		#if UserName == Password:
		self.Result = True
		#else:
		#	self.Result = False
		return self
	def ShutDown(self):
		App.get_running_app().stop()

	def ReadRegister(self, UserName, Password, Password2):
		if Password == Password2 and Password != "" and UserName != "":
			self.data  = True
		elif Password != Password2 or Password == "":
			self.data = "PassError"
		elif UserName == "":
			self.data = "UserError"
		return self



		
###### App windows #################
class LoginWindow(Screen):
	def __init__(self, **kwargs):
		super(LoginWindow, self).__init__(**kwargs)
		self.Login = LoginWidget()
		self.add_widget(self.Login)

class RegisterWindow(Screen):
	def __init__(self, **kwargs):
		super(RegisterWindow, self).__init__(**kwargs)
		self.Register = RegisterWidget()
		self.add_widget(self.Register)

class MessangerWindow(Screen):
	def __init__(self, **kwargs):
		super(MessangerWindow, self).__init__(**kwargs)
		self.Messanger = MessangerWidget()
		self.add_widget(self.Messanger)

######################################



######### Screens ##########
#------ Login Windows -----------#
class LoginWidget(Widget, LogicCommands):
	pass

class RegisterWidget(Widget,LogicCommands):
	pass

#------ Messanger Windows -----------#
class MessangerWidget(Widget, LogicCommands):
	pass

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
