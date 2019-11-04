####################################################################################
################# This is the main program that will start the UI ##################
####################################################################################
from Tools_Module import Tools
from Configuration_Module import Configuration
from HayStack_API import HayStack, Run_HayStack_Client
from User_Modules import User_Profile

#Other imports
import config
import getpass
import os

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
		#First time this program was executed
		while True:
			Password = getpass.getpass(prompt = "Enter a password: ")
			Password2 = getpass.getpass(prompt = "Enter the passsword again: ")
			if Password == Password2:
				config.Password = Password
				break
			else:
				print("")
				print("Passwords do not match!")
				print("")
		HayStack().Build_All_Directories()
	else:
		while True:
			#Turn this on later
			#Password = getpass.getpass(prompt = "Enter the HayStack password: ", stream = None)
			#config.Password = Password
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
	Sync_Messanger = Run_HayStack_Client(Function = "Sync_Messanger")
	Sync_Messanger.start()
	DynamicPublicLedger = Run_HayStack_Client(Function = "Dynamic_Public_Ledger")
	DynamicPublicLedger.start()
	PingFunction = Run_HayStack_Client(Function = "Ping_Function")
	PingFunction.start()
	while True:
		User_Input = raw_input("Press 'b' to go back >>> ")
		if User_Input == "b":
			Sync_Messanger.Terminate()
			DynamicPublicLedger.Terminate()
			PingFunction.Terminate()
			break
		else:
			print("Node status: "+Sync_Messanger.Output()+" Block Height: "+DynamicPublicLedger.Output())


if __name__ == "__main__":
	#Check if the user is using this software for the first time
	First_Usage()
	Outcome = Second_Screen()
	if  Outcome == None:
		exit()
	elif Outcome == False:
		Non_Interactive_Client()
