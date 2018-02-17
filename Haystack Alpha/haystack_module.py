#!/usr/bin/env python
#-*- coding: utf-8 -*-

from communication_module import *
from encryption_module import *
from Crypto.PublicKey import RSA
import time
import math

'''Haystack Network Parameters'''


global block_time
block_time = 3600
global public_seed
public_seed = 'RLNYJUUABIIJVMOACWJNDQBNWIRMXKWIBQRSJQRBOEEMJLAXSAMHSVZFGAZKZOTZCJLJBBV9MWCHRIIXU'
global genesis
genesis = 1518435400

'''Dynamic Public Ledger functions'''

def current_block():
    decimal_block = (time.time() - int(genesis)) / block_time
    block = int(math.ceil(decimal_block))-1
    return block

def active_ledger():
    block = current_block()
    return generate_address(public_seed, int(block))

def get_public_addresses():
    block = current_block()
    api_rec = Iota(RoutingWrapper(server).add_route('attachToTangle', 'http://localhost:14265'), seed = public_seed)
    transfers = api_rec.get_transfers(start = int(block), stop = int(block + 1))
    bundles = transfers.get('bundles')
    times = []
    addresses = []
    for i in bundles:
        public_addresses = str(i.get_messages()).strip("[u'").strip("']")
        addresses.append(public_addresses)
        for x in i:
            message = str(x)
            timestamp = x.attachment_timestamp
            times.append(timestamp)
    unique_addresses = []
    unique_times = []
    x = 0
    for i in addresses:
		if i not in unique_addresses:
			if i != "":
				unique_addresses.append(i)
                unique_times.append(times[x])
                x = x + 1
    final_addresses = []
    for i in range (0, len(addresses)):
        if int(unique_times[i] + 60) >= int(genesis + block_time * block) and int(unique_times[i] - 60) <= int(genesis + block_time * block + block_time):
            final_addresses.append(unique_addresses[i])
    file = open(str("UserData/Public_Address_Pool.txt"),"w")
    for i in unique_addresses:
		file.write(str(i))
		file.write(str("\n"))
    file.close()

def add_contact(name, address):
    file = open(str("UserData/Public_Address_Pool.txt"),"rb")
    for i in file:
        if i[:81] == address:
            key = i[81:]
            print 'Contact found'
    file.close()
    file = open(str("UserData/Contacts.txt"),"r+b")
    address_book = file.readlines()
    address_exists = False
    for i in address_book:
        if i == key:
            address_exists == True
            print 'Contact already exists'
    if address_exists != True:
        file.write(str(name))
        file.write(str("\n"))
        file.write(str(key))
        file.write(str("\n"))
    file.close()

def find_contact(name):
    file = open(str("UserData/Contacts.txt"),"rb")
    address_book = file.readlines()
    print address_book
    for i in range (0, len(address_book)):
        print i
        print address_book[i].replace('\n','')
        if address_book[i].replace('\n','') == name:
            key = address_book[i+1]
    file = open("UserData/Public_Address_Pool.txt","r")
    addresses = []
    for i in file:
        if str(i[81:]) == str(key):
            address = i[:81]
            return address

def publish_address(secret_code):
    key = read_public_key().exportKey().replace('\n', '.').replace('\r', ',')
    seed_key = read_seed_key(str(secret_code))
    public_address = generate_address(seed_key, 0) #this will need to be fixed to generate new public addresses when inbox is full
    block = current_block()
    active_ledger = generate_address(public_seed, int(block))
    address_pair = str(public_address) + str(key) + '\n'
    send(active_ledger, address_pair, str(secret_code))

'''initialisation'''
#generate_key_pair('asdasd')
#generate_seed_key()
'''connection'''
#publish_address('asdasd')
#get_public_addresses()

print find_contact('alice')
