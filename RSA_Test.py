#Requires the pyCrypto package (pip install pycrypto)

import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast


rand_1 = Random.new().read
key_1 = RSA.generate(1024, rand_1) #generate pub and priv key
publickey_1 = key_1.publickey() # pub key export for exchange

rand_2 = Random.new().read
key_2 = RSA.generate(1024, rand_2) #generate pub and priv key
publickey_2 = key_2.publickey() # pub key export for exchange

#test message
test=str('test')

encrypted_2 = publickey_2.encrypt(test, 32)
encrypted_1 = publickey_1.encrypt(str(encrypted_2), 32)
#message to encrypt is in the above line 'encrypt this message'

print 'encrypted message:', encrypted_1 #ciphertext
f = open ('encryption.txt', 'w')
f.write(str(encrypted_1)) #write ciphertext to file
f.close()

#decrypted code below

f = open('encryption.txt', 'r')
message = f.read()


decrypted_1 = key_1.decrypt(ast.literal_eval(str(encrypted_1)))
decrypted = key_2.decrypt(ast.literal_eval(str(decrypted_1)))

print 'decrypted message:', decrypted

f = open ('encryption.txt', 'w')
f.write(str(message))
f.write(str(decrypted))
f.close()
