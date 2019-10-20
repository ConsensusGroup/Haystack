##############################################################
####################### User Interface #######################
##############################################################

#Importing relevant Kivy classes
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

#Importing OS related classes
from os import listdir

######### Screens ##########
#------ Login Window -----------#
class LoginWindow(Screen):
	def __init__(self):
		pass


####################################
class KivyConfig:
	def __init__(self):
		self.KivyPath = "./Kivy/"

	def ReadConfigurationFiles(self):
		for i in listdir(self.KivyPath):
			Builder.load_file(self.KivyPath + i)

	def ScreenLoader(self):
		self.sm = ScreenManager()
		self.sm.add_widget(LoginWindow())
		return self 

###### Build Main #######
class MainApp(App):

	def build(self):
		self.title = "The Haystack Application"
		return KivyConfig().ScreenLoader().sm

##### This starts the app #####
if __name__ == "__main__":
	
	KivyConfig().ReadConfigurationFiles()
	app = MainApp()
	app.run()
