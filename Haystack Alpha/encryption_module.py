#!/usr/bin/env python
#-*- coding: utf-8 -*-
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
from random import SystemRandom
import random
import pyffx
import os
import sys
from base64 import b64encode, b64decode

'''System Parameters'''

global chars
chars = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= '
global identifier
identifier = '////'
global default_size
default_size = 256
global alpha # number of trajectories
alpha = 1
global beta # number of bounces
beta = 1

'''Define administrative tasks'''

def create_user_data():
    if not os.path.exists('UserData'):
        os.makedirs('UserData')

def normalise(plaintext):
    normaltext = str(plaintext) + (default_size - len(plaintext) - len(identifier)) * str(' ') + str(identifier)
    return normaltext

def split(input):
	return [input[start:start+default_size-len(identifier)] for start in range(0, len(input), default_size - len(identifier))]

def random_address():
    rand = SystemRandom()
    random_trytes = [i for i in map(chr, range(65,91))]
    random_trytes.append('9')
    seed = [random_trytes[rand.randrange(len(random_trytes))] for x in range(81)]
    return ''.join(seed)

'''Construct symmetric format-preserving encryption functions and generators'''

def generate_secret_key():
    sec_key = os.urandom(64)
    return sec_key

def encrypt(plaintext, secret_key):
    cipher = pyffx.String(str(secret_key), alphabet=str(chars), length=len(str(plaintext)))
    ciphertext = cipher.encrypt(str(plaintext))
    return ciphertext

def decrypt(ciphertext, secret_key):
    cipher = pyffx.String(str(secret_key), alphabet=str(chars), length=len(str(ciphertext)))
    plaintext = cipher.decrypt(str(ciphertext))
    return plaintext

'''Define RSA key generation and reading functions'''

def generate_key_pair(secret_code):

    create_user_data()
    if not os.path.exists('UserData/Keys'):
        os.makedirs('UserData/Keys')

    pair = RSA.generate(2048)

    f = open("UserData/Keys/priv_key.pem", "wb")  # private key
    f.write(pair.exportKey(format = 'PEM', passphrase=str(secret_code)))
    f.close()

    pub_key = pair.publickey().exportKey(format = 'PEM')

    with open("UserData/Keys/pub_key.pem", 'wb') as f:  # the plain text public key for providing to ledger
        f.write(pub_key)

def read_private_key(secret_code):
    assert  os.path.exists('UserData/Keys'), 'No RSA keys! Please generate them with generate_key_pair()'
    with open("UserData/Keys/priv_key.pem", 'rb') as f:
        content = f.readlines()
    data = ''.join(content[:30])
    key = RSA.importKey(data, passphrase=str(secret_code))
    return key

def read_public_key():
    assert os.path.exists('UserData/Keys'), 'No RSA keys! Please generate them with generate_key_pair()'
    with open("UserData/Keys/pub_key.pem", 'rb') as f:
        data = f.read().replace("\\n","\n")
    key = RSA.importKey(data)
    return key

'''Construct asymmetric encryption functions'''

def decode(ciphertext, secret_code):
    priv_key = read_private_key(str(secret_code))
    cipher = PKCS1_OAEP.new(priv_key)
    msg = cipher.decrypt(str(ciphertext))
    return msg

def encode(plaintext, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(str(plaintext))
    return encrypted

'''Create signature and authentication functions'''

def message_signature(plaintext, secret_code):
    digest = SHA256.new()
    digest.update(plaintext)
    private_key = read_private_key(str(secret_code))
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)
    return sig

def verify_signature(plaintext, signature, public_key):
    digest = SHA256.new()
    digest.update(plaintext)
    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, signature)
    assert verified, 'Signature verification failed'
    print('Successfully verified message')
    return verified

'''Construct preparation and verification functions for the Haystack'''

def prepare_needle(plaintext, secret_code):
    normaltext = normalise(str(plaintext))
    needle = str(normaltext) + str(b64encode(message_signature(str(normaltext), str(secret_code))))
    return needle

def verify_needle(needle, public_key):
    plaintext = needle[:int(default_size)]
    try:
        sig = b64decode(needle[int(default_size):])
        verification = verify_signature(plaintext, sig, public_key)
        return verification
    except:
        print 'Authentication failed.'
        return False

'''Higher level functions [for testing purposes]'''

def rand_pub_key():
    pair = RSA.generate(2048)
    pub_key = pair.publickey()
    return pub_key

def generate_address_pool(number_of_entries):
    create_user_data()
    with open("UserData/Address_Pool.txt", 'wb') as f:
        for i in range (0, int(number_of_entries)):
            address_pair = str(random_address()) + str(rand_pub_key().exportKey()).replace('\n', '.').replace('\r', ',') +'\n'
            f.write(address_pair)
    return

'''Bouncing protocol implementation'''

def random_bounce():
    assert os.path.exists('UserData/Address_Pool.txt'), 'No current address pool exists! Run the dynamic ledger module.'
    file = open("UserData/Address_Pool.txt","r")
    addresses = []
    for i in file:
        if "#New_Seed#" in i:
            continue
        else:
            addresses.append(i)
	index = random.randrange(0,len(addresses),1)
    address = addresses[int(index)]
    return address

def generate_trajectory():
    bounces = []
    for i in range (0, int(beta)):
        bounces.append(random_bounce())
    return bounces

def get_addresses(bounces):
    addresses = []
    for i in range (0, len(bounces)):
        addresses.append(str(bounces[i])[:81])
    return addresses

def get_text_keys(bounces):
    keys = []
    for i in range (0, len(bounces)):
        key = str(bounces[i])[81:]
        keys.append(key)
    return keys

def load_keys(text_keys):
    keys = []
    for i in range (0, len(text_keys)):
        pub_key = text_keys[i].replace('.', '\n').replace(',', '\r')
        data = pub_key.replace("\\n","\n")
        public_key = RSA.importKey(data)
        keys.append(public_key)
    return keys

def get_keys(bounces):
    return load_keys(get_text_keys(bounces))

#get_text_keys and load_keys should be one function (maybe)

'''Message preparation and higher level functions'''

###Normalises and signs message then prepares trajectory and loads public keys.###
###The message is encrypted and the secret keys are locked.###
def lock_n_load(plaintext, secret_code, receiver_address, receiver_key):
    needle = prepare_needle(plaintext, str(secret_code))
    bounces = generate_trajectory()
    addresses = get_addresses(bounces)
    keys = get_keys(bounces)
    index = random.randrange(0,int(beta),1)
    addresses[int(index)] = receiver_address
    keys[int(index)] = receiver_key
    metadata = []
    for i in range (int(beta)-1, index, -1):
        if i == int(beta)-1:
            bounce_address = '0' * 81
        else:
            bounce_address = addresses[i+1]
        bounce_key = keys[i]
        bouncedata = str(bounce_address) + str(bounce_key)
        encoded_bouncedata = encode(str(bouncedata), bounce_key)
        metadata.append(encoded_bouncedata)
    for i in range (index, -1, -1):
        secret_key = generate_secret_key()
        needle = encrypt(needle, str(secret_key))
        if i == int(beta)-1:
            bounce_address = '0' * 81
        else:
            bounce_address = addresses[i+1]
        bounce_key = keys[i]
        bouncedata = str(bounce_address) + str(secret_key)
        encoded_bouncedata = encode(str(bouncedata), bounce_key)
        metadata.append(encoded_bouncedata)

    random.shuffle(metadata)
    message_data = ''
    for i in range (0, len(metadata)):
        message_data = str(message_data) + str(metadata[i]) + '##:##'
    locked_message = str(needle) + '##Begin#Metadata##' + str(message_data)
    first_bounce_address = addresses[0]
    return locked_message, first_bounce_address

def prepare_for_broadcast(plaintext, secret_code, receiver_address, receiver_key):
    messages = []
    addresses = []
    for i in range (0, int(alpha)):
        message_data = lock_n_load(plaintext, secret_code, receiver_address, receiver_key)
        messages.append(message_data[0])
        addresses.append(message_data[1])
    return messages, addresses

def unlock(locked_message, secret_code):
    ciphertext = locked_message[:600]
    metadata = locked_message[618:].split("##:##")
    metadata.remove('')
    for i in range (0, len(metadata)):
        try:
            decoded_data = decode(metadata[i], secret_code)
        except:
            pass
        try:
            bounce_address = decoded_data[:81]
        except:
            print 'Format error: No metadata could be decoded or the message exceeds 252 characters.'
            sys.exit(1)
    secret_key = decoded_data[81:]
    needle = decrypt(ciphertext, secret_key)
    if needle[int(default_size - len(identifier)):int(default_size)] == str(identifier):
        print 'Message successfully received.'
        print 'Message:', needle[:int(int(default_size) - len(identifier))]
    else:
        print 'Message is still locked!'
    if bounce_address == '0'*81:
        print 'Message terminated.'
    else:
        print 'Bouncing...'
    return needle

###This demonstration will generate a new set of RSA keys and a random ###
###example public address pool. the message is then encrypted and then ###
###bounced around the network. The encrypted packed is then decomposed and###
###the metadata is encrypted to reveal a secret key and bounce address. The ###
###content is then decrypted with the secret key and in the event that the ###
###randomly generated receiver index is == 0, the message is successfully ###
###received and authenticated. this occurs with probability 1/5 ###

#print read_private_key('abcdefg')
#address = '999ZZZ999'*9
#locked = lock_n_load('will the real slim shady please stand up please stand up please stand up take me to the moon let me play above the stars four score and seven years ago the great states of yo momma', 'swagyolo', address, read_public_key())
#needle = unlock(locked[0], 'swagyolo')
#verify_needle(needle, read_public_key())


########################################################################################
################ Routing of functions from a shell script ##############################
########################################################################################
