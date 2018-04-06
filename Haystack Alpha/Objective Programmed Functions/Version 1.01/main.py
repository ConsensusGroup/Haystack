from HayStackAPI import Configuration

#Kivy API
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

#OS imports
from os import listdir



class KivyConfig:
	def __init__(self):
		self.KivyPath = "./Kivy/"

	def ReadConfig(self):
		for i in listdir(self.KivyPath):
			Builder.load_file(self.KivyPath+ i)


######### Login Screen ##########
class LoginWidget(Widget, Configuration):
	UserName = ObjectProperty(None)
	Password = ObjectProperty(None)

	def ReadLogin(self):
		print(str(self.UserName+ " " +self.Password))

	def ShutDown(self):
		App.get_running_app().stop()
	

###### Build Main ########
class MainApp(App):

	def build(self):
		self.title = "Conensus-Haystack"
		return LoginWidget()

######### Start the app ##########
if __name__ == "__main__":
	KivyConfig().ReadConfig()
	app = MainApp()
	app.run()