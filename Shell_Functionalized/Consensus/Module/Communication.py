from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.crypto.addresses import AddressGenerator
from iota.adapter.wrappers import RoutingWrapper
from iota import *
import sys
import multiprocessing
import random

def Sender_Module(Seed_key, receive, message, server):
	#This essentially connects python to the locahost which was initiated with the Java package (iri-X.X.X.X.jar) (see Node_Module.sh)
	api = Iota(RoutingWrapper(server).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed_key)	

	Send_to_IOTA=str(message)
	#We are now converting a message into the tribyte representation
	text_transfer = TryteString.from_string(Send_to_IOTA)

	#Decode the message as a test
	Tryte = TryteString(str(text_transfer))
	message = Tryte.as_string()

	#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived. 
	txn_2 = ProposedTransaction(address = Address(receive), message = text_transfer,value = 0)

	#Now create a new bundle (i.e. propose a bundle)
	bundle = ProposedBundle()

	#Add the transaction "txn_2" to the bundle. We can also add several addresses for receiving but we get to that later.
	bundle.add_transaction(txn_2)

	#Send the transaction. the variable "depth" refers to the number of previous transactions being considered. 
	bundle.finalize()
	coded = bundle.as_tryte_strings()
	send = api.send_trytes(trytes = coded, depth = 4)
	print(send)
	
def Address_Generator(Seed_key, Server):
	api = Iota(RoutingWrapper(str(Server)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed_key)
	
	Generate = api.get_new_addresses()
	Address = str(Generate.get('addresses')).strip("[Address(").strip(")]").strip("'")
	print(Address)
	
def Receiver_Module(Seed_key, Server):
	api_rec = Iota(RoutingWrapper(Server).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed_key)

	#We pull the transaction history of the account (using the seed)
	mess = api_rec.get_account_data(start = 0) 

	#Decompose the Bundle into components
	balances = mess.get('balance')
	bundle = mess.get('bundles')
	Address = mess.get('addresses')
	
	for i in bundle:
		message_rec = i.get_messages(errors='drop')
		message=str(message_rec)

		#This cleans the string of the receiving side. 
		Message = message.lstrip("[u'").rstrip(" ']")
	print(Message)
		
def Public_Addresses(Public_Seed, server, SaveToDirectory):
	api_rec = Iota(RoutingWrapper(server).add_route('attachToTangle', 'http://localhost:14265'), seed = Public_Seed)

	#We pull the assigned address history of the account (using the seed)
	mess = api_rec.get_account_data(start = 0) 
	Addresses = []
	#Decompose the Bundle into components
	Addresses_In_Ledger = mess.get('bundles')
	for i in Addresses_In_Ledger:
		Public_Addresses = str(i.get_messages()).strip("[u'").strip("']")
		Addresses.append(Public_Addresses)
	file = open(str(SaveToDirectory+"/Current_Public_Address_Pool.txt"),"w")
	Unique_Addresses = []
	for i in Addresses:
		if i not in Unique_Addresses:
			Unique_Addresses.append(i)
	for i in Unique_Addresses:
		file.write(str(i))
		file.write(str("\n"))
	file.close()

def Random_Bounce(Public_Addresses):
	file = open(Public_Addresses,"r")
	Addresses = []
	for i in file:
		if "#New_Seed#" in i:
			continue
		else:
			Addresses.append(i)
	
	#Generate a random number from the range 0 to length of number of addresses in the public address pool
	choice = random.randrange(0,len(Addresses),1)
	
	Clean = Addresses[1].split("\n")
	print(Clean[choice])

def Dynamic_Ledger(Public_Seed, Max_Address_Pool, Current_Public_Address_Pool):

	#Here we open the Current_Public_Address_Pool.txt file and count the number of addresses
	file = open(Current_Public_Address_Pool,"r")
	Addresses = []
	for i in file:
		if "#New_Seed#" in i:
			There_Is_a_Seed_In_Pool_Already = "yes"
		else:
			Addresses.append(i)
			There_Is_a_Seed_In_Pool_Already = "no"
	
	#Count the number of addresses within the Public Seed
	Number_Of_Current_Addresses = len(Addresses)
	
	#If the number of addresses is equal to 
	if Max_Address_Pool <= Number_Of_Current_Addresses and There_Is_a_Seed_In_Pool_Already == "no":
		print("True")
	else:
		print("False")
		
def Scan_Entries(Directory_Of_File, Purpose):

	#Open the text file to be scanned
	file = open(Directory_Of_File,"r")
	Entries = []
	for i in file:
		Entries.append(i)
	
	if Purpose == "Seed":
		Seeds_Found = []
		for i in Entries:
			if "#New_Seed#" in i:
				Seed = i.strip("#New_Seed#").strip("\n")
				Seeds_Found.append(Seed)
		length = len(Seeds_Found)
		if length > 0:
			print(Seeds_Found[int(length)-1])
	#This might need to be improved to ensure that the seed is actually working properly. 
		
		#Here we might implement some testing mechanism to validate the seed. 
		#....
	
	if Purpose == "Address":
		index = len(Entries)
		Address = Entries[index]
		print(Address)
			

########################################################################################
################ Routing of functions from a shell script ##############################
########################################################################################
Module = str(sys.argv[1])
	
if Module == "Sender_Module":
	
	#These are the required input parameters
	Seed_key = str(sys.argv[2]) #User seed key
	Receiver = str(sys.argv[3]) #The recepient address
	Message = str(sys.argv[4]) #The message to be sent
	Server = str(sys.argv[5]) #The server for the node
	
	#Runs the sender script
	Send = Sender_Module(Seed_key, Receiver, Message, Server)

#This generates a new address from the seed and outputs the new sender address
if Module == "Address_Generator":
	Seed_key = str(sys.argv[2]) #User seed key
	Server = str(sys.argv[3])
	Address = Address_Generator(Seed_key, Server)

if Module == "Receiver_Module":
	Seed_key = str(sys.argv[2]) #User seed key
	Server = str(sys.argv[3]) #Server address
	Bundle = Receiver_Module(Seed_key, Server)
	
if Module == "Public_Addresses":
	Seed_Key = str(sys.argv[2])
	Server = str(sys.argv[3])
	SaveToDirectory = str(sys.argv[4])
	Addresses = Public_Addresses(Seed_Key,Server,SaveToDirectory)

if Module == "Random_Bounce":
	Public_Addresses = str(sys.argv[2])
	Address = Random_Bounce(Public_Addresses)

if Module == "Dynamic_Ledger":
	Public_Seed = str(sys.argv[2])
	Max_Address_Pool = int(sys.argv[3])
	Current_Public_Address_Pool = str(sys.argv[4])
	Dynamic_Ledger(Public_Seed, Max_Address_Pool, Current_Public_Address_Pool)
	
if Module == "Scan_Entries":
	Directory_Of_File = str(sys.argv[2])
	Purpose = str(sys.argv[3])
	Scan_Entries(Directory_Of_File, Purpose)









######## Need to find a proper implementation of this still
if Module == "Node_Finder":
	Random_Test_Seed = str(sys.argv[2])
	Server = str(sys.argv[3])
	Address = Address_Generator(Random_Test_Seed, Server)


