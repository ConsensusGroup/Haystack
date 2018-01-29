from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.crypto.addresses import AddressGenerator
from iota.adapter.wrappers import RoutingWrapper
from iota import *
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import sys
import random

def Sender_Module(Seed_key, receive, message, server):
	#This essentially connects python to the locahost which was initiated with the Java package (iri-X.X.X.X.jar) (see Node_Module.sh)
	api = Iota(RoutingWrapper(str(server)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed_key)	
	
	#We are now converting a message into the tribyte representation
	text_transfer = TryteString.from_string(str(message))

	#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived. 
	txn_2 = ProposedTransaction(address = Address(receive), message = text_transfer, value = 0)

	#Now create a new bundle (i.e. propose a bundle)
	bundle = ProposedBundle()

	#Add the transaction "txn_2" to the bundle. We can also add several addresses for receiving but we get to that later.
	bundle.add_transaction(txn_2)

	#Send the transaction. the variable "depth" refers to the number of previous transactions being considered. 
	bundle.finalize()
	coded = bundle.as_tryte_strings()
	send = api.send_trytes(trytes = coded, depth = 4)

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
	
	Message = ""
	for i in bundle:
		message_rec = i.get_messages(errors='drop')
		message=str(message_rec)

		#This cleans the string of the receiving side. 
		Message = message.lstrip("[u'").rstrip(" ']")
	return Message
		
def Public_Addresses(Public_Seed, server, SaveToDirectory):
	api_rec = Iota(RoutingWrapper(server).add_route('attachToTangle', 'http://localhost:14265'), seed = Public_Seed)

	#We pull the assigned address history of the account (using the seed)
	mess = api_rec.get_account_data(start = 0) 
	Addresses = []
	#Decompose the Bundle into components
	Addresses_In_Ledger = mess.get('bundles')
	for i in Addresses_In_Ledger:
		Public_Address = str(i.get_messages()).strip("[u'").strip("']")
		Addresses.append(Public_Address)
	file = open(str(SaveToDirectory+"/Current_Public_Address_Pool.txt"),"w")
	Unique_Addresses = []
	for i in Addresses:
		if i not in Unique_Addresses:
			if i != "":
				Unique_Addresses.append(i)
	for i in Unique_Addresses:
		file.write(str(i))
		file.write(str("\n"))
	file.close()

def Random_Bounce(Public_Address_List, File_Type):
	if File_Type == ".txt":
		file = open(Public_Address_List,"r")
		Addresses = []
		for i in file:
			if "#New_Seed#" in i:
				continue
			else:
				Addresses.append(i)
	if File_Type == "List":
		Address = Public_Address_List
	
	#Generate a random number from the range 0 to length of number of addresses in the public address pool
	choice = random.randrange(0,len(Address),1)
	
	Clean = Address[int(choice)]
	return Clean

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
			print(Seeds_Found[0])
	#This might need to be improved to ensure that the seed is actually working properly. 
		
		#Here we might implement some testing mechanism to validate the seed. 
		#....
	
	if Purpose == "Address":
		index = len(Entries)
		Address = Entries[index].split("###")
		print(Address[0])

	if Purpose == "Sending_Encrypt":
		Addresses = []
		Public_Keys = []
		for i in Entries:
			Splitted = i.split("###")
			Address = Splitted[0]
			Public_Key = Splitted[1]
			Addresses.append(Address)
			Public_Keys.append(Public_Key)
		return Addresses, Public_Keys
	if Purpose == "Read":
		for i in Entries:
			Entry = i.strip("\n")
			return Entry 
	
#################################################################################
################## Encryption Section ###########################################
#################################################################################
def Key_Generation(secret_code, directory):
	###### Key Generator ######
	key = RSA.generate(2048)
	
	#--Encrypt the private key using a password --#
	encrypted_key = key.exportKey(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")

	#--- Save the encrypted private key ---#
	file_out = open(str(directory), "wb")
	file_out.write(encrypted_key)
	print(directory)

def Get_Public_Key(secret_code, directory):
	#--- Open the file with the encrypted private key ---#
	encoded_key = open(str(directory), "rb").read()
	
	#-- decrypt private key ---#
	key1 = RSA.import_key(encoded_key, passphrase=secret_code)

	#Public Key which we need to broadcast
	recipient = key1.publickey().exportKey()
	
	return recipient

def Encrypt_Message(Public_Key, Message):
	
	Public_Key = Public_Key.replace("\\n","\n")
	
	#We encrypt the message using the public key
	keys = RSA.importKey(Public_Key)
	cipher = PKCS1_OAEP.new(keys)
	ciphertext = cipher.encrypt(Message).encode("hex")
	
	#This gets sent to the tangle.
	return ciphertext 
	
def Decrypt_Message(directory, ciphertext, secret_code):
	
	#first we open the RSA file which is stored under directory
	private_key_encoded = open(str(directory),"rb").read()
	Private_Key = RSA.import_key(private_key_encoded, passphrase = secret_code)
	unlock = PKCS1_OAEP.new(Private_Key)
	Message = unlock.decrypt(ciphertext.decode("hex"))
	return Message
	
def split(input, size):
	return [input[start:start+size] for start in range(0, len(input), size)]
	
def Prepare_and_Broadcast(Recipient_Public_Key, Public_KeyS, Addresses, Message_To_Encrypt):

	#========== Encryption Section for this function ==============#
	#First we encrypt the message
	Message_Decomposed = split(Message_To_Encrypt,64)
	
	Container = []
	for i in Message_Decomposed:
		Part = Encrypt_Message(Recipient_Public_Key, i)
		Container.append(Part)

	
	for i in range(len(Addresses)):
		Address = Addresses[i]
		Public_Key = Public_KeyS[i]
		With_Address = str("Address:"+Address)
		Encrypted_Addresses = Encrypt_Message(Public_Key,With_Address)
		Container.append(Encrypted_Addresses)

	To_Send = ""
	for i in Container:
		To_Send = str(str(To_Send)+"######:######"+str(i))
		
	return To_Send
	
def Receiver_Decryption(directory, Secret_Password, Encrypted_Message, Public_Key):

	#Pull apart the string to make it a list
	Separated = Encrypted_Message.split("######:######")

	#Iterate through each entry to see if it is decrypted. 
	Contain = []
	Operation = []
	for i in Separated:
		if i == '':
			continue
		else:
			try:
				Part = Decrypt_Message(directory, i, Secret_Password)
				Contain.append(Part)
				Open = "True"
				Operation.append(Open)
			except ValueError:
				Contain.append(i)
				Open = "False"
				Operation.append(Open)
			
	bounce = ""
	Address = ""
	Decrypted = ""
	counter = 1
	Conditions = Operation.count("True")-1
	for i in range(len(Operation)):
		message = Contain[i]
		decrypt = Operation[i]
		if decrypt == "False":
			bounce = str(str(bounce)+"######:######"+str(message))
		if decrypt == "True" and Operation[0] == "True" and counter < Conditions:
			Decrypted = str(str(Decrypted)+str(message))
			counter = counter +1
		if decrypt == "True" and Conditions >= 1:
			Address = message.strip("Address:")
			Appending = Encrypt_Message(Public_Key, "Dummy")
			bounce = str(str(bounce)+"######:######"+str(Appending))
			
	return [bounce, Address, Decrypted]



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
	print(str(Bundle))
	
if Module == "Public_Addresses":
	Seed_Key = str(sys.argv[2])
	Server = str(sys.argv[3])
	SaveToDirectory = str(sys.argv[4])
	Addresses = Public_Addresses(Seed_Key,Server,SaveToDirectory)

if Module == "Random_Bounce":
	Public_Addresses = str(sys.argv[2])
	Address = Random_Bounce(Public_Addresses)
	print(Address)
	
if Module == "Dynamic_Ledger":
	Public_Seed = str(sys.argv[2])
	Max_Address_Pool = int(sys.argv[3])
	Current_Public_Address_Pool = str(sys.argv[4])
	Dynamic_Ledger(Public_Seed, Max_Address_Pool, Current_Public_Address_Pool)
	
if Module == "Scan_Entries":
	Directory_Of_File = str(sys.argv[2])
	Purpose = str(sys.argv[3])
	entry = Scan_Entries(Directory_Of_File, Purpose)
	print(entry)
#################################################################################
################## Encryption Section ###########################################
#################################################################################

if Module == "Key_Generation":
	Secret_Code = str(sys.argv[2])
	Directory_Of_File = str(sys.argv[3])
	Key_Generation(Secret_Code, Directory_Of_File)
	
if Module == "Get_Public_Key":
	Secret_Code = str(sys.argv[2])
	Directory_Of_File = str(sys.argv[3])
	Public_Key = Get_Public_Key(Secret_Code, Directory_Of_File)
	print(Public_Key.strip("\n"))
	
if Module == "Encrypt_Message":
	Public_Key = str(sys.argv[2])
	Message = str(sys.argv[3])
	Ciphertext = Encrypt_Message(Public_Key, Message)
	print(Ciphertext)

if Module == "Decrypt_Message":
	Directory_Of_File = str(sys.argv[2])
	Ciphertext = str(sys.agv[3])
	Secret_Code = str(sys.argv[4])
	Message = Decrypt_Message(Directory_Of_File, Ciphertext, Secret_Code)
	print(Message)

if Module == "Prepare_and_Broadcast":
	Message_To_Encrypt = str(sys.argv[2])
	Receiver_Address = str(sys.argv[3])
	UserData = str(sys.argv[4])
	Server = str(sys.argv[5])
	bounces = int(sys.argv[6])
	
	Pool = str(UserData+"Current_Public_Address_Pool.txt")
	Seed = str(UserData+"Seed.txt")
	
	#Build function which reads the Public_KeyS, Addresses, Private_Seed, 
	Entries = Scan_Entries(Pool, "Sending_Encrypt")

	Private_Seed = Scan_Entries(Seed, "Read")
	
	Public_Pool = Entries[0]
	Public_Key = Entries[1]
	
	Public_KeyS = []
	Addresses = []
	
	if bounces > 0:
		for i in range(bounces):
			Random_Address_Chosen = str(Random_Bounce(Public_Pool, "List"))
			Indexing = Public_Pool.index(Random_Address_Chosen)
			Public = Public_Key[Indexing]
			Public_KeyS.append(Public)
			Addresses.append(Random_Address_Chosen)
			
	#We find the Public key of the recipient.
	Recipient_Public_Key = Public_Key[Public_Pool.index(str(Receiver_Address))]
	
	#Now add the destination address with the public key
	Addresses.append(Receiver_Address)
	Public_KeyS.append(Recipient_Public_Key)
	
	#Remove the first address. See the lists below:
	#Public_Keys = [A,B,C,D]
	#Public_Pool = ["B","C","D","E"]
	First_Send = Addresses.pop(0)
	
	#Add some more random receivers
	if bounces > 0:
		for i in range(bounces):
			Random_Address_Chosen = str(Random_Bounce(Public_Pool, "List"))
			Indexing = Public_Pool.index(Random_Address_Chosen)
			Public = Public_Key[Indexing]
			Public_KeyS.append(Public)
			Addresses.append(Random_Address_Chosen)
	
	#Add the last address for the dummy to be terminated
	Random_Address_Chosen = str(Random_Bounce(Public_Pool, "List"))
	Addresses.append(Random_Address_Chosen)
	
	#Prepare the encryption of the message:
	To_Send = Prepare_and_Broadcast(Recipient_Public_Key, Public_KeyS, Addresses, Message_To_Encrypt)

	#Send the message off.
	Sender_Module(Private_Seed, First_Send, To_Send, Server)
	
if Module == "Receiver_Decryption":

	UserData = str(sys.argv[2])
	Server = str(sys.argv[3])
	Key = str(sys.argv[4])
	Seed = str(UserData+"Seed.txt")
	Latest_Received = str(UserData+"Latest.txt")
	
	PrivateSeed = Scan_Entries(Seed, "Read")
	PublicKey = Get_Public_Key(PrivateSeed, Key)
	
	EncryptedMessage = Receiver_Module(PrivateSeed, Server)
	Content = Receiver_Decryption(Key, PrivateSeed, EncryptedMessage, PublicKey)
	
	#[bounce, Address, Decrypted]
	Bounce = Content[0]
	Next_Destination = Content[1]
	Message = Content[2]
	
	#Now we compare the previous received to the current receive to avoid resending the same message. 
	Latest = ""
	try:
		Latest = Scan_Entries(Latest_Received, "Read")
	except IOError:
		pass

	#First Case destroys the propagation of a "dummy" message
	if Message == "" and Next_Destination == "":
		print("Dummy terminated")
	
	#Second Case the message is bounced
	if (str(Next_Destination) != "" and str(Message) == "" and str(Latest) != str(EncryptedMessage)):		
		Sender_Module(PrivateSeed, Next_Destination, Bounce, Server)
		file = open(Latest_Received,"w")
		file.write(str(EncryptedMessage))
		file.close()
		
	#Third Case the receiver is able to decrypt the message. 
	if Message != "" and Next_Destination != "":
		Sender_Module(PrivateSeed, Next_Destination, Bounce, Server)
		print(Message)
		print(Next_Destination)
	
	
######## Need to find a proper implementation of this still
if Module == "Node_Finder":
	Random_Test_Seed = str(sys.argv[2])
	Server = str(sys.argv[3])
	Address = Address_Generator(Random_Test_Seed, Server)


