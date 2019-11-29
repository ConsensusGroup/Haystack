####################################################################################
################# This is the main program that will start the UI ##################
####################################################################################
from Tools_Module import Tools
from Configuration_Module import Configuration
from HayStack_API import HayStack, Run_HayStack_Client
from User_Modules import User_Profile
from BackupRestore_Module import Restore, Backup

#Other imports
import config
import getpass
import os
from time import sleep
import sys

def Welcome_Screen():
	print("                              ####################### Welcome to the IOTA HayStack Protocol!!! ###########################")
	print("")
	print("")
	print("")
	print("""\

	                                                                                                .###
	                                                                                              ,#######*
	                                                                                              #########
	                                                                                              #########
	                                                          ((      ####    .(                    #####
	                                                        ######   ######  #####
	                                                        ######/   ####   .###  .####
	                                                        ,####*                  *#( .###        .######      /(.
	                                                                    *(.              ##(        ########  .#######
	                                                          #####   .#####  .####         ###     #######(  ########
	                                                         #######   #####  (####  ####             ###(     ######/
	                                               ,######   /######                 ###(  /.                    .,
	                                               ########     ,                         ###*      *###*
	                                               #######*                .##.                    #######    #####
	                                                 ###,        (#####.  ######  #####            #######   #######    ,*
	                                                      ,.     #######  ,####.  (####  ####       .###.    *######  ######.
	                                                   #######   /#####                  (##                    .     #######
	                                                   ########                                  #####       ..        #####
	                                                   #######                                   #####     #####/
	                                         *######     ,(/               (###*                   *.      (####.   ####
	                                        #########                ###.   (#*              ,###.                 (#####
	                                        #########          .##*  (##                     #####     .####        ####
	                                         #######                        ,####.        ,.   ,        ####     (#
	                                            .             /##(   ####    ####        ####       ##(         ####,
	                                                           ##    ,##,                 (/       ####         (###
	                                                           .,               #####          ###         .###,
	                                                          ####    #####     #####          .#       ##  ###
	                                                           /(     *####      /#/               ##/ ###/
	                                                            *#/                  ######        *#.
	                                                           #####     /####.     .#######
	                                                            ###.     ######      ######
	                                                                       #(                #######
	                                                              /#####       #####(       /#######*
	                                                              /#####      #######        #######    *######
	                                                                           #####/          (##     (########
	                                                                    #####(         ######          #########
	                                                                   #######        ########          #######*
	                                                                    #####(        (#######             .
	                                                                                    ####                                                                       """)
def First_Usage():
	if Tools().Check_File(File = str(Configuration().UserFolder+"/"+Configuration().KeysFolder+"/"+Configuration().PrivateKey)) == False:

		print("Searching for working IOTA nodes.. please wait 30 seconds...")
		Node_Finder = Run_HayStack_Client(Function = "Node_Testing")
		Node_Finder.start()
		for i in range(30):
			sleep(1)
		Node_Finder.Terminate()

		sleep(10)
		#First time this program was executed
		print("Please enter a password for HayStack.")
		while True:
			Password = getpass.getpass(prompt = "Enter a password: ")
			Password2 = getpass.getpass(prompt = "Enter the passsword again: ")
			if Password == Password2 != "":
				config.Password = Password
				break
			else:
				print("")
				print("Passwords do not match!")
				print("")

		while True:
			print("Would you like to restore from backup? (y/n)")
			Choice = raw_input(">>> ")
			if Choice == "y":
				Recovery = True
				print("You have chosen to recover your keys. Please enter your two passwords in the correct order.")
				print("Type in password 1")
				SuperSecretKey1 = raw_input(">>> ")
				print("Type in password 2")
				SuperSecretKey2 = raw_input(">>> ")

				print("Password 1: "+SuperSecretKey1+" Password 2: "+SuperSecretKey2)
				answer = raw_input("Are these correct? (y/n) ")
				if answer == "y":
					break
				else:
					pass

			elif Choice == "n":
				Recovery = False
				break
			else:
				print("Not a valid choice...")

		if Recovery == True:
			outcome = Restore(SuperSecretKey1, SuperSecretKey2).Restore_FileDirectory()
			if outcome == False:
				print("Failed to restore keys.")
				HayStack().Build_All_Directories()
			else:
				print("Found your house keys!")
		else:
			Started = False
			while True:
				try:
					HayStack().Build_All_Directories()
					Node_Finder.Terminate()
				except:
					print("Your connection is unstable. Performing a full scan of the nodes available")
					if Started == False:
						Node_Finder = Run_HayStack_Client(Function = "Node_Testing")
						Node_Finder.start()
						Started = True
					for i in range(180):
						sleep(1)



	else:
		while True:
			Password = getpass.getpass(prompt = "Enter the HayStack password: ", stream = None)
			config.Password = Password
			try:
				User_Profile().PrivateKey
				break
			except ValueError:
				print("The password was incorrect. Please try again.")
def Second_Screen():
	while True:
		User_Choice = raw_input("What would you like to do: \n a) Run the chat window\n b) Run a non interactive relaying client\n c) Quit the program \n>>> ")
		if User_Choice == "a":
			return True
		elif User_Choice == "b":
			return False
		elif User_Choice == "c":
			return None

def Non_Interactive_Client():
	Node_Finder = Run_HayStack_Client(Function = "Node_Testing")
	Node_Finder.start()
	Sync_Messanger = Run_HayStack_Client(Function = "Sync_Messanger")
	Sync_Messanger.start()
	DynamicPublicLedger = Run_HayStack_Client(Function = "Dynamic_Public_Ledger")
	DynamicPublicLedger.start()
	PingFunction = Run_HayStack_Client(Function = "Ping_Function")
	PingFunction.start()

	while True:
		User_Input = raw_input("Press 'b' to go back or press 'Enter' for a status >>> ")
		if User_Input == "b":
			Sync_Messanger.Terminate()
			DynamicPublicLedger.Terminate()
			PingFunction.Terminate()
			Node_Finder.Terminate()
			config.RunTime = False
			break
		else:
			print("Node status: "+Sync_Messanger.Output()+" Block Height: "+str(DynamicPublicLedger.Output()))

class Interactive_Client():
	def __init__(self):
		#This initiates the client
		self.Sync_Messanger = Run_HayStack_Client(Function = "Sync_Messanger")
		self.DynamicPublicLedger = Run_HayStack_Client(Function = "Dynamic_Public_Ledger")
		self.PingFunction = Run_HayStack_Client(Function = "Ping_Function")
		self.Node_Finder = Run_HayStack_Client(Function = "Node_Testing")

	def Background(self, Action):
		if Action == "Start":
			self.Sync_Messanger.start()
			self.DynamicPublicLedger.start()
			self.PingFunction.start()
			self.Node_Finder.start()
			config.RunTime = True
		elif Action == "Stop":
			config.RunTime = False
			self.Sync_Messanger.Terminate()
			self.DynamicPublicLedger.Terminate()
			self.PingFunction.Terminate()
			self.Node_Finder.Terminate()
		return self

	def Third_Screen(self):
		self.Background(Action = "Start")
		while True:
			User_Choice = raw_input("Please choose one of the options: \n a) Compose Message \n b) Check Inbox \n c) Add or remove Contacts \n d) Go back \n *) Backup Menu \n>>> ")
			if User_Choice == "a":
				self.Message_Composer()
				pass
			elif User_Choice == "b":
				Output = []
				try:
					Output = HayStack().Stored_Messages()
				except IOError:
					HayStack().Build_All_Directories()
				if len(Output) == 0:
					print("You have no messages")
				else:
					for i in Output:
						print("From: "+i[1]+" --- Message: "+i[0])
			elif User_Choice == "c":
				User_Choice= raw_input("Chose one: \na) Add contact \nb) Remove contact\nc) Go Back \n>>>")
				if User_Choice == "a":
					self.Add_To_Contacts()
				elif User_Choice == "b":
					print("Type in the user you want to remove. Or press 'b' to go back.\n")
					Contact_Loop = True
					while Contact_Loop == True:
						for i in HayStack().Return_Contact_List():
							print(i+"\n")
						Remove = raw_input(">>>")
						if Remove == "b":
							Contact_Loop = False
						elif Remove in HayStack().Return_Contact_List():
							HayStack().Delete_From_Contacts(Username = Remove)
							Contact_Loop = False
						else:
							print("User Name was not found.\n")

				elif User_Choice == "c":
					pass
			elif User_Choice == "d":
				self.Background(Action = "Stop")
				break
			elif User_Choice == "*":
				while True:
					print("Warning this is the backup menu! Here you have the ability to store your private key and password on the tangle.\nThere is a risk of compromise if the passwords chosen are not strong enough.")
					print("The passwords will be shown in clear text when you enter them in.")
					print("To leave this menu just leave the passwords blank.")
					SuperSecretKey1 = raw_input("Password 1:>>> ")
					SuperSecretKey2 = raw_input("Password 2:>>> ")
					if SuperSecretKey1 == SuperSecretKey2 == "":
						break
					elif SuperSecretKey1 != SuperSecretKey2:
						Backup(SuperSecretKey1 = SuperSecretKey1, SuperSecretKey2 = SuperSecretKey2).PublicBackUp()
						break
					elif SuperSecretKey1 == SuperSecretKey2:
						print("Try a stronger combination. The passwords have to be different")
			else:
				print("Not a valid choice.")
		return self

	def Add_To_Contacts(self):
		while True:
			print("")
			print("Your current address is: " + HayStack().Get_Current_Address().Current_Address +" at the block height "+str(HayStack().Get_Current_Ledger_Addresses().BlockNumber))
			print("")
			User_Input = raw_input("Please enter the address of the contact (You can go back with 'b'):\n>>>")
			#Check if the contact is in the Database
			Continue = False
			if len(User_Input) == 81:
				Continue = True
			elif User_Input == "b":
				break
			else:
				print("Wrong IOTA address format. A standard IOTA address has a length of 81 characters.")

			if Continue == True:
				Output = HayStack().Find_From_Address(Address = User_Input)
				if isinstance(Output, list) == True:
					User_Name = raw_input("User Name: \n>>>")
					Output = HayStack().Find_From_Address(Address = User_Input)
					if isinstance(Output, list) == True:
						print("Found address in ledger. The public key of "+User_Name+" is:\n " +Output[0] +"\n")
						print("Adding user to address book!")
						HayStack().Add_Address(Address = User_Input, Username = User_Name)
						break
					else:
						print("The user has not been found on the ledger. Please wait for the next block and try again.")
				else:
					print("It seems like you are not online")

			return self

	def Address_Book(self):
		List_of_contacts = HayStack().Return_Contact_List()
		print("Please enter the recipient. For multiple recipients write ',' between each.")
		for i in List_of_contacts:
			print(i+"\n")
		User_Input = raw_input('>>> ')
		Users = User_Input.split(',')
		Recipients = []
		for i in Users:
			Output = HayStack().Address_From_Username(Username = str(i))
			if isinstance(Output, list) == True:
				Recipients.append(Output)
		return Recipients

	def Message_Composer(self):
		while True:
			User_Choice = raw_input("Please choose one of the options: \n a) Get recipient from address book \n b) From public ledger \n c) Go Back \n>>> ")
			if User_Choice == "a":
				Recipients = self.Address_Book()
				if len(Recipients) != 0:
					print("Enter your message:\n")
					Message = raw_input(">>> ")
					Number_of_Trajectories = raw_input("Number of trajectories: (Number < 3) >>> ")
					try:
						DifferentPaths = int(Number_of_Trajectories)
						if DifferentPaths >= 3:
							DifferentPaths = 3
					except:
						DifferentPaths = Configuration().DifferentPaths
					for i in Recipients:
						PublicKey = i[0]
						Current_Address = HayStack().Last_Seen_Address(PublicKey = PublicKey)
						if Current_Address != None:
							Address = Current_Address
						else:
							Address = i[1][0]

						Receipt = HayStack().Send_Message(Message = Message, ReceiverAddress = Address, PublicKey = PublicKey, DifferentPaths = DifferentPaths, Encrypted = True)
						print("Message sent. Transaction hash: "+str(Receipt[0][1]))
					break
				if len(Recipients) == 0:
					print("You dont have any contacts. Returning to previous menu.")
					break
				else:
					print("Nothing entered. Returning to previous menu.")
					break
			elif User_Choice == "b":
				Current_Ledger_Pool = HayStack().Get_Current_Ledger_Addresses().Current_Addresses
				Current_Client_Address = HayStack().Get_Current_Address().Current_Address
				if len(Current_Ledger_Pool) >= 1:
					z = 1
					print("Choose one of the addresses below:\n")
					for i in Current_Ledger_Pool:
						Address = i[0]
						if Address == Current_Client_Address:
							print(str(z)+") "+Address+" <-- You\n")
						else:
							print(str(z)+") "+ Address+"\n")
						z = z+1

					Choice = raw_input(">>> ")
					try:
						if len(Choice) == 81:
							Public_Key_of_Choice = ""
							for i in Current_Ledger_Pool:
								if Choice == i[0]:
									Public_Key_of_Choice = i[1]
									print(Public_Key_of_Choice)
							if Public_Key_of_Choice != "":
								print("Enter your message to: "+Choice+"\n")
								Message = raw_input(">>> ")
								Receipt = HayStack().Send_Message(Message = Message, ReceiverAddress = Choice, PublicKey = Public_Key_of_Choice, DifferentPaths = Configuration().DifferentPaths, Encrypted = True)
								print("Message sent. Transaction hash: "+str(Receipt[0][1]))
								break
							else:
								print("Error with finding the public encryption key try again. Likely this is due to wrong address inserted or you copied whitespace.")
						elif int(Choice):
							Choice_Data = Current_Ledger_Pool[int(Choice)-1]
							print("Enter your message to: "+ Choice_Data[0]+"\n")
							Message = raw_input(">>> ")
							Receipt = HayStack().Send_Message(Message = Message, ReceiverAddress = i[0], PublicKey = i[1], DifferentPaths = Configuration().DifferentPaths, Encrypted = True)
							print("Message sent. Transaction hash: "+str(Receipt[0][1]))
							break
					except ValueError:
						print("Error with input. Make sure you type in either the above address in or simply choose the number.")
				else:
					print("There are currently no users online. Your address will appear shortly")
			elif User_Choice == "c":
				break
		return self

if __name__ == "__main__":
	#Check if the user is using this software for the first time
	First_Usage()
	while True:
		Outcome = Second_Screen()
		if  Outcome == None:
			config.RunTime = False
			exit()
		elif Outcome == False:
			Non_Interactive_Client()
		elif Outcome == True:
			Interactive_Client().Third_Screen()
