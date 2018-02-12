#!/usr/bin/env python
#-*- coding: utf-8 -*-
from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.crypto.addresses import AddressGenerator
from iota.adapter.wrappers import RoutingWrapper
from encryption_module import decode
from iota import *
import sys
import random

global server
server = 'http://eugene.iota.community:14265'

'''Define administrative tasks'''

def create_user_data():
    if not os.path.exists('UserData'):
        os.makedirs('UserData')

def normalise(plaintext):
    normaltext = str(plaintext) + (default_size - len(plaintext) - len(identifier)) * str(' ') + str(identifier)
    return normaltext

def split(input):
	return [input[start:start+default_size] for start in range(0, len(input), default_size)]

def random_seed():
    rand = SystemRandom()
    random_trytes = [i for i in map(chr, range(65,91))]
    random_trytes.append('9')
    seed = [random_trytes[rand.randrange(len(random_trytes))] for x in range(81)]
    return ''.join(seed)

'''Pseudorandom seed generation and reading functions'''

def generate_seed_key():
    rand = SystemRandom()
    random_trytes = [i for i in map(chr, range(65,91))]
    random_trytes.append('9')
    seed = [random_trytes[rand.randrange(len(random_trytes))] for x in range(81)]
    content = ''.join(seed)
    encoded_seed = encode(content, read_public_key())
    with open("UserData/Seed_Key.txt", 'wb') as f:
        f.write(encoded_seed)

def read_seed_key(secret_code):
    with open('UserData/Seed_Key.txt', 'rb') as f:
        data = f.read()
    return decode(data, str(secret_code))

'''Send and receive functions'''

def generate_address(seed_key):
	api = Iota(RoutingWrapper(str(server)).add_route('attachToTangle', 'http://localhost:14265'), seed = seed_key)
	generate = api.get_new_addresses()
	address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")
	return address

def send(secret_code, receiver_address, message):
    seed_key = read_seed_key(str(secret_code))
	#This essentially connects python to the locahost which was initiated with the Java package (iri-X.X.X.X.jar) (see Node_Module.sh)
    api = Iota(RoutingWrapper(str(server)).add_route('attachToTangle', 'http://localhost:14265'), seed = seed_key)
	#We are now converting a message into the tribyte representation
    text_transfer = TryteString.from_string(str(message))
	#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived.
    txn_2 = ProposedTransaction(address = Address(receiver_address), message = text_transfer, value = 0)
	#Now create a new bundle (i.e. propose a bundle)
    bundle = ProposedBundle()
	#Add the transaction "txn_2" to the bundle. We can also add several addresses for receiving but we get to that later.
    bundle.add_transaction(txn_2)
	#Send the transaction. the variable "depth" refers to the number of previous transactions being considered.
    bundle.finalize()
    coded = bundle.as_tryte_strings()
    send = api.send_trytes(trytes = coded, depth = 4)

def receive(seed_key):
	api_rec = Iota(RoutingWrapper(server).add_route('attachToTangle', 'http://localhost:14265'), seed = seed_key)
	#We pull the transaction history of the account (using the seed)
	mess = api_rec.get_account_data(start = 0)
	#Decompose the Bundle into components
	balances = mess.get('balance')
	bundle = mess.get('bundles')
	Address = mess.get('addresses')
	Message = []
	for i in bundle:
		message_rec = i.get_messages(errors='drop')
		message=str(message_rec)
		#This cleans the string of the receiving side.
		Message.append(message.lstrip("[u'").rstrip(" ']"))
	return Message

def quick_receive(seed_key):
    #Receives only bundles and returns only the latest message
    api_rec = Iota(RoutingWrapper(server).add_route('attachToTangle', 'http://localhost:14265'), seed = seed_key)
    mess = api_rec.get_transfers(start = 0)
    bundle = mess.get('bundles')
    message = str(bundle[len(bundle)-1].get_messages(errors='drop')).lstrip("[u'").rstrip(" ']")
    return message


'''Dynamic Public Ledger functions'''

def public_addresses(public_seed):
	api_rec = Iota(RoutingWrapper(server).add_route('attachToTangle', 'http://localhost:14265'), seed = public_seed)
	#We pull the assigned address history of the account (using the seed)
	mess = api_rec.get_account_data(start = 0)
	addresses = []
	#Decompose the Bundle into components
	addresses_in_ledger = mess.get('bundles')
	for i in addresses_in_ledger:
		public_address = str(i.get_messages()).strip("[u'").strip("']")
		addresses.append(public_address)
	file = open(str("UserData/Public_Address_Pool.txt"),"w")
	unique_addresses = []
	for i in Addresses:
		if i not in unique_addresses:
			if i != "":
				unique_addresses.append(i)
	for i in unique_addresses:
		file.write(str(i))
		file.write(str("\n"))
	file.close()

def check_ledger(public_seed, max_address_pool):
	#Here we open the Current_Public_Address_Pool.txt file and count the number of addresses
	file = open(UserData/Public_Address_Pool,"r")
	Addresses = []
	for i in file:
		if "#New_Seed#" in i:
			There_Is_a_Seed_In_Pool_Already = "yes"
		else:
			addresses.append(i)
			There_Is_a_Seed_In_Pool_Already = "no"
	#Count the number of addresses within the Public Seed
	number_of_current_addresses = len(addresses)
	#If the number of addresses is equal to
	if max_address_pool <= number_of_current_addresses and There_Is_a_Seed_In_Pool_Already == "no":
		return True
	else:
		return False

def get_timestamps(public_seed):
    api_rec = Iota(RoutingWrapper(server).add_route('attachToTangle', 'http://localhost:14265'), seed = receiver_seed)
    transfers = api_rec.get_transfers(start = 0)
    bundles = transfers.get('bundles')
    times = []
    for i in bundles:
        for x in i:
            timestamp = x.attachment_timestamp
            times.append(timestamp)
    return times

def scan_entries(filepath, purpose):
	#Open the text file to be scanned
	file = open(filepath,"r")
	entries = []
	for i in file:
		entries.append(i)
	if purpose == "Seed":
		seeds_found = []
		for i in entries:
			if "#New_Seed#" in i:
				seed = i.strip("#New_Seed#").strip("\n")
				seeds_found.append(seed)
		length = len(seeds_found)
		if length > 0:
			print(seeds_found[0])
##This might need to be improved to ensure that the seed is actually working properly.##
###Here we might implement some testing mechanism to validate the seed.##
	if purpose == "Read":
		for i in entries:
			entry = i.strip("\n")
			return entry

###REQUIRED###
##function for deciding on a public address
##function for storing and reading public address
##functions for attaching public_key / public_address pair to the ledger

########################################################################################
################ Routing of functions from a shell script ##############################
########################################################################################
