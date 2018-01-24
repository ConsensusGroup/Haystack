from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import warnings

def Key_Generation(secret_code, directory):
	###### Key Generator ######
	key = RSA.generate(2048)
	
	#--Encrypt the private key using a password --#
	encrypted_key = key.exportKey(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")

	#--- Save the encrypted private key ---#
	file_out = open(str(directory), "wb")
	file_out.write(encrypted_key)

def Get_Public_Key(secret_code, directory):
	#--- Open the file with the encrypted private key ---#
	encoded_key = open("rsa_key.bin", "rb").read()

	#-- decrypt private key ---#
	key1 = RSA.import_key(encoded_key, passphrase=secret_code)

	#Public Key which we need to broadcast
	recipient = key1.publickey().exportKey()
	return recipient

def Encrypt_Message(Public_Key, Message):

	#We encrypt the message using the public key
	keys = RSA.importKey(Public_Key)
	cipher = PKCS1_OAEP.new(keys)
	ciphertext = cipher.encrypt(Message)
	return ciphertext #This gets sent to the tangle.



#######FIX UP!!!!!
def Decrypt_Message(directory, ciphertext, secret_code):
	
	#first we open the RSA file which is stored under directory
	#private_key_encoded = open(str(directory),"rb").read()
	#Private_Key = RSA.import_key(private_key_encoded, passphrase = secret_code)
	secret_code = RSA.import_key(secret_code)
	unlock = PKCS1_OAEP.new(secret_code)	#Private_Key)
	Message = unlock.decrypt(ciphertext)
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
	
def Receiver_Decryption(Secret_Password, Encrypted_Message, Public_Key):

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
	Conditions = Operation.count("True")
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



#User/function Input
directory = str("rsa_key.bin")
Secret_Password = str("Hell1o")


Message_To_Decrypt= str("xfdvxxcfv")

#Entry1: A Public
A = str("-----BEGIN PUBLIC KEY-----"+"\n"+"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6iFJS42EbvhI0zR6S5UBR3leYFZoE/+5lXm/tX6luH5C+LENH8DFIWNqGICPbckwBsaG4FGG3dN1MoqGCa7UxhvvssTVWDMWJj7MHVsGYm3yZND7Coiei7ShWMUItdW91fRH9I26UIuq70w1QFuFsmyLHirAII0WydompdGERpw7n5MWMyFcpBAmu1eOqH9b0fMeA+ROsHQB6jYWkxGrYdQxo4pjUJJMK9Wk2eViH6xX5CLcr86/YTkoG5L3mkSbET4+Ba8I+akhsBByUpIYJrHgRslQe/Lh0fS/IlMXa/7ZZYYK20ftKVqVTDwWwUX87mUY4JfiifSJH+9ZJwLytQIDAQAB"+"\n"+"-----END PUBLIC KEY-----")

#Entry2: B Public
B = str("-----BEGIN PUBLIC KEY-----"+"\n"+"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm+wj9fYLwFtgw4vL/IZKy7DmvlED6owX7oFQLMEwt+I2zQbFCLm2uqyAteqit/pvlAGEZmzvXMCPW+x6ffOTlmZ6tWUfZNFGATwKTJ7RZKSCT4R3zyIO62TJ44/BcG0R3D0NKWvH46EDrc4KJUF6g56uUGlzCGL5/e1oh0+ifxEZD1QFuWAl+of/+F5VLaL1V+TzTsNKWLdiIxJg/cupc9BUJQ0zmVlbxWYIj64n5BvYssnlb1m4x/kpRYYj/qe4s8eC/zi4mRoP3RZCCNKYwnD5FJ6b2toWgxl00CJp+aSq8aQOPRkDpRc0NLx66MndgfSnWRABDQNR40YE9LPe/wIDAQAB"+"\n""-----END PUBLIC KEY-----")

#Entry3: C Public
C = str("-----BEGIN PUBLIC KEY-----"+"\n"+"MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBsqg3vyMpv7mFI35DiptKT0Lr2Bwmo70Nl+9H80VBMxyivxCCSPwfKZT7pkhqeR9dfWYVDHyXuMcENnPLCiCpgsYqgPZK4f8Gtkg+dCHhIB6A2gCW6v053cR6Bi6CTqNBg+NAvhKN6r27yY4X/NOvsIWmkPmGonZWdQD189kfQejJq4QKhoWFjKckmExhLRSA4e0IqNOyySZzhWTp+3iylU/rT7V3gFCepDYY6R9XRy0V4EiubBmQYslPCcjOArAED96wLCTExbXOFEct8gxz1eVcjYh+ADrrXnD/ov0h6DNQfqUxBbNYsO9neabrbHVTzWrHP8s9BM0cwmRR5Eu27AgMBAAE="+"\n"+"-----END PUBLIC KEY-----")

#Entry4: D Public
D = str("-----BEGIN PUBLIC KEY-----"+"\n"+"MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBsBnbFDN4xyEw3OpOjOWTp1WtpUHsPWL+xIAuWzSX8jf/5+hCjTNzLDgh9DLSgyqnz70UDItYWh2FtWnsBSWx4YPc5uHagljgsGe5NV6wGgBK9a3Tq+/8PrBLqxh8ToNeV1pwf3Ajy2APa9C9znxA9NGRB6nvIiMtfZcCS0D+9YFKNr337VnY4AJXHwyy550qOpKj29Rqg7ar0FAR+2nuNW2aEXG5Lvobstow7gc3M1UQfSKDFEeSU4lFageScShv/uO5kgXSJJ4AMyGcJQRSUQF1ASonrxm1kD6FjmU6s9d4ZKmt2AE/xvDWXhYEgV+2O+kBenBAnN5tltGnOx9hhAgMBAAE="+"\n"+"-----END PUBLIC KEY-----")




#These are Private keys (not known usually but just for testing)
APriv = str("-----BEGIN RSA PRIVATE KEY-----"+"\n"+"MIIEowIBAAKCAQEA6iFJS42EbvhI0zR6S5UBR3leYFZoE/+5lXm/tX6luH5C+LENH8DFIWNqGICPbckwBsaG4FGG3dN1MoqGCa7UxhvvssTVWDMWJj7MHVsGYm3yZND7Coiei7ShWMUItdW91fRH9I26UIuq70w1QFuFsmyLHirAII0WydompdGERpw7n5MWMyFcpBAmu1eOqH9b0fMeA+ROsHQB6jYWkxGrYdQxo4pjUJJMK9Wk2eViH6xX5CLcr86/YTkoG5L3mkSbET4+Ba8I+akhsBByUpIYJrHgRslQe/Lh0fS/IlMXa/7ZZYYK20ftKVqVTDwWwUX87mUY4JfiifSJH+9ZJwLytQIDAQABAoIBAERCbh8T5E+CHaFOBHWyvIu9C9HkfzWNcertcwIUKXavgREGdYATcKW6WT1JhgeJB3KCQOJ3gm178AhLMKb0DN6xWGHzVwv+4O9HkbThS+w4h9nyv64jhK3QfNXnpBF3foA5Vx0qkO5Yuf5IZqIbzM/nK2whJKCY4dL5whjIC9uVtE2By3SVTOIHUCUOhHhWoYScEFJ5aMmOcrZ0qPwvJlQPKYCAWMg9326WZdTJGtv1O3TcdXfvc3JR8gafMnyU917NRo7HKKlrVlE1xOkAr7LnRjMkJ3Z707LJb0KAEo4MM7kd1v9bB/rIcBYmjMmYqztTuqwW64wJ3pORcnKVwcUCgYEA/Iqw/ELo0bj7ZQ68YKYhOCQarM3zIMYOK9UeBmAmdEe257L9G4Vpl/DygcLqIE4C1joG/BiQPlJ7093ne83IcI/YqRdLTvBasx8NkcczyTQscZ6R2sZuUuImOatcsTsINa+Od6oP+UYnbtTpV7uOfOG8yQQg+9Rr815Gfelm1n8CgYEA7VYNB54v0GyEzbpKUHivp/hRheCBU9HV74bkwWtdHsEvDB/uF557A4O8V/TsjPSXEKLBIG2XEyDO+7l+SjcCH0fldosV7kFB5QooKazNaRfBWQbbZHhrAWcrdtkdDWZKqbIPh4vsmLcMCuXnWMdJz6lq09YQyOYK/sCnh58zJMsCgYEA+xHbgP/4PUCd1kt/JssjLZBfYLtj4opk3lkDf60preL6SYHeNvU9FIy8XBtu7m0ATwDjns/A3+TbLLhpgeEFTDsGWJ1LBpDYa0oNEIgtyPPw14ihUxKB7i7dd+oQvjaFI/KEPh25wcZoP7y2u71AnJFEQci0DgmSxSJODLH1xnsCgYBUDnUA7LKMg9KpNkBZrdSwjc75tmC3egrmEYV1R3wsh0kNZ0WhEd0Jip+rGzCoX3wdRTdXL9kgyi7kkna6/C6BO6p2SJ5UysH2x5kf4XbCsMomqLoNJGTpk0uehRi4BTGOVmUPoawDDllyhqhgFfz7UkpmiltZe7gLL9pluymW7wKBgG7PczPVxFv3G+rUZOsvp+uEkThqnmIS4lf9JWjNGSilCEx+i6DN4+vG9qkJTFqq02sKANxLiFt47sDuNZUksf6mk5nrcoT8i22Uwe/SPRnkJUbmGWyC5HZN+60pxoL+s1VD1NfvDeLORe9IZZFaSdh2NaAsNYkgUOCuMn7K3LDr"+"\n"+"-----END RSA PRIVATE KEY-----")

BPriv = str("-----BEGIN RSA PRIVATE KEY-----"+"\n"+"MIIEpAIBAAKCAQEAm+wj9fYLwFtgw4vL/IZKy7DmvlED6owX7oFQLMEwt+I2zQbFCLm2uqyAteqit/pvlAGEZmzvXMCPW+x6ffOTlmZ6tWUfZNFGATwKTJ7RZKSCT4R3zyIO62TJ44/BcG0R3D0NKWvH46EDrc4KJUF6g56uUGlzCGL5/e1oh0+ifxEZD1QFuWAl+of/+F5VLaL1V+TzTsNKWLdiIxJg/cupc9BUJQ0zmVlbxWYIj64n5BvYssnlb1m4x/kpRYYj/qe4s8eC/zi4mRoP3RZCCNKYwnD5FJ6b2toWgxl00CJp+aSq8aQOPRkDpRc0NLx66MndgfSnWRABDQNR40YE9LPe/wIDAQABAoIBAQCSW7VhskRTmjKZO0cN0cyxqGrfaFKhvkDUiyOD7w/Y+4lvKJSY3SJN1ZC3sfhtc7F6n3X1YvnH+aRXqAFO6u21dppmXPZ7/wiULhSI2Wc57kW3eGOx1YlloeT0K0NrUaY7Mj+Biv9FhyVZ5xaU5AKpO7DqICFvVODOXyQIJ1Mjq56tGolNOCwyzmM5/vi4Et3xSnP9bDgZjEamP2xkAhwO6Axv/9mqwxWmvaiFbQVjpHuAvemZmHLpRIxWqmM3ZMhe9olx+pojULSABhdFugYTFhbHGBNtlwVuZx3Zhl3jmvGv4ca+gvq3A2AMA7rWGr1cGHIsKgHJJpghKoCeDxQJAoGBAO+d5l4srPn5W2qYBLb3Tcc7Q5eaEbcUWlsRCacwnM6mCOqWFVJ1K1EbWBGGhjSTU1bAOXqPL5/MasRph3KHvhT0gCtuN5NCMH68fOCDBaH1BBcqqwbv2RaRmzrggpVYBJIu32tmaqJIlB81Upjce5oEeiulMlGe5RP8Rcu1GNNDAoGBAKaVTrdxdhJcn69YrO+Eu2bl+fANw7Vs2k2Zx8NLz0uGZaqvWwxY3WdLdITJdFfNs8QuJFOXF+OeC+eth3472WPg11bMbxhW55p80ZA/iZdL8wxY8THtQN2QVmmj5tPPyO6MOvkBIQ52DOz5tHxnwnDr4N7VizjfuFKRsVG6WmOVAoGBALH2UfwrriTSICUg1o+VSPzpdSAJW5Lf2OO92a+EmVGZWxHvedKOFyfb6SLLCK3PpZvOlGIEKljCl6Fcxy42xuQFW5Pl/fyushnOn+iXJv3MXcde9zrltBPg/KtTx2hnwK1ZhrHblOMGiIxNLBU/28TeAmacAK1CF90qBiRvUgrFAoGAeqHz/wvh9gaF79oCBZnbNBcddmFLsCXgV7xb2SPYCSt5cLwC9QX+h+p+brq3kWP3cPbe+0KB7akN7pJK6t04XlTJcjaxmmNvwMUeqWh87AqXdIGNnkmgtPtrAf4NEeUncKV/TIxOP40cWuBAxEzGUcb0FldyVH4t/WsP9LCRljkCgYAyEU3IKPpvz/kFqmmFS47jn2V+J9EP3OxQf3NU+HkY5k3OpPn2M/ULEPMoWmM85Xxe8hXlZBYTtORh/6oR42p3wd6qAHMkfL5j+fHCqnhz50L6TeUREF4/tLaIDyn4edg+bxUMEZ9X80tdattXys1i33XM/tJBCKXsOzDC9QGi3g=="+"\n"+"-----END RSA PRIVATE KEY-----")

CPriv = str("-----BEGIN RSA PRIVATE KEY-----"+"\n"+"MIIEoQIBAAKCAQBsqg3vyMpv7mFI35DiptKT0Lr2Bwmo70Nl+9H80VBMxyivxCCSPwfKZT7pkhqeR9dfWYVDHyXuMcENnPLCiCpgsYqgPZK4f8Gtkg+dCHhIB6A2gCW6v053cR6Bi6CTqNBg+NAvhKN6r27yY4X/NOvsIWmkPmGonZWdQD189kfQejJq4QKhoWFjKckmExhLRSA4e0IqNOyySZzhWTp+3iylU/rT7V3gFCepDYY6R9XRy0V4EiubBmQYslPCcjOArAED96wLCTExbXOFEct8gxz1eVcjYh+ADrrXnD/ov0h6DNQfqUxBbNYsO9neabrbHVTzWrHP8s9BM0cwmRR5Eu27AgMBAAECggEAXgKlugzSLxJickSRObWwOxf7mDywe8o8WjAKFRsVyMcJCT+6GiyT1ePQEQ1JICTxTNnLNC3vh+rdpaRiVjCt0Sfo0gdTN3G4Iy1ZerdIMLEASAaIHc/C2A0yokslanpDhZHdsy6irNK4PtYhqJClh43EsscRgGqNdRWN3N3JdbAR84iVIIqUbYU0esakJ9PWZlVK6R6TlTNn00ilRPuD4MHS94mw5VC3Jg47TVADLyd4Jnnot8zX8h4btgYcCKywbNyoGgmqTUmpBkg9FnMztCZjcsPy+tw0iTi2dx/uODBfh9yYWNkvb3VLBypz2Fw18uJ6HSE9mqvtsoAwdAEuuQKBgQCncDptAfx1h7hkPPhohsp6fWvgZDB+vzSz2rV2w6IYa5+oKe1FywnveHD1Wzit4vr9daj+wMZEu5DlikqYtq2b5b0mTlyAULfSZNthgFu4njFvHGw125fYG9/YwTgV3usEuAxJdYH+su06ZO9ulM0f28OLdJpyGLkKp1rw3b0FfQKBgQCmI5hx3kKzWuspP53xzFzIn1Wc3WmF9QlpBmu9NEsyMyG85JyvDXX7rOjmjSZex/xNRjRQ/zsbf8LMyXNTnnOejBtkIyGxZIgbZzqaMZxq2Z8cvEU/hRs8qsfePXld0I5k9fyKM5cKa0Q30MGi0gS0ebScVTd0amd2DTkov6JFlwKBgEv7/Tes2BHKFp6+oIhm6wotUsBRF0TdpqAcF4+e9jeY16pr5HZwzsBy6ugdjpoy0G4ncBq0BwX4DKhuWq308NI3rt/sXcQJXXJIPNqBcp5Ug+CFiIHkdoMnGy11eetK72KD12eawPSB5HBEj/eh5XiYtaPataAjog24pud56SbNAoGAVWh5JxiGm6OCvvrIXJSdojlfDrw4Ujgs9UPqwSKQAaeNkYjJD6jQ3Wf/dv5bGmCe0K7lmDoNjc55O0PYuMT9VSVbs3foC0TOP6Aq3Tfh3IAxrtkOlF/+J4r4IsThjpv3h+l5QSbSX/XS5Qq5cNWcu5bRhYi9cGh+9Y5Isy0I49MCgYAYgx4lwuqZRE81NYG8UvFyQ7a7Z1WSPrrz7OaWZMLKTOn3vn7ku1DhpwrbmEz2l35eGmaHBRd6Rt8Idrt16D/u95pqWwInafEIvbpok8xid218Z0IA/fwL86lIraxyQOyb0EVHUeruornuDq4wD1B42yxifZ40m3g663I2TT+hlQ=="+"\n"+"-----END RSA PRIVATE KEY-----")

DPriv = str("-----BEGIN RSA PRIVATE KEY-----"+"\n"+"MIIEogIBAAKCAQBsBnbFDN4xyEw3OpOjOWTp1WtpUHsPWL+xIAuWzSX8jf/5+hCjTNzLDgh9DLSgyqnz70UDItYWh2FtWnsBSWx4YPc5uHagljgsGe5NV6wGgBK9a3Tq+/8PrBLqxh8ToNeV1pwf3Ajy2APa9C9znxA9NGRB6nvIiMtfZcCS0D+9YFKNr337VnY4AJXHwyy550qOpKj29Rqg7ar0FAR+2nuNW2aEXG5Lvobstow7gc3M1UQfSKDFEeSU4lFageScShv/uO5kgXSJJ4AMyGcJQRSUQF1ASonrxm1kD6FjmU6s9d4ZKmt2AE/xvDWXhYEgV+2O+kBenBAnN5tltGnOx9hhAgMBAAECggEATne/jFFVkUnSewe0uIr3T5e0RzKrwTERRWNmp6rrHfIz72wC6+voMiNGbTdueaHdJBE4yxdh9clvLtTbpsqj3SlqS+Y/XVThBr/rRwkZLzuW4TsOGabk1oiC0UEKz+I012Wl0MqvQV9CJajcUxtG236UGQFv2vHq8Kfj44Eb274HgQfCdzvibp7iL6Q2B0w6IiR7dW1sJaS7jSs8GEBDvsByRfve1xK+q58fk7ffY4PmshIAKtGT5bGL0jICOTXs+jk6qvKRDCfq4OykPehH8zkQEj5RecCqQA/XZ52oP6IXtLtKBXWO7WAcaPY0vhFpZ+z1D0q95tUO7/i/tYdlwQKBgQDHcVsFg3YYfbzDD/B7x90RrLTjSdoD5JXyeDyvvjCG3O5PYr2aRpVbpKMUSc/fN8MLCZHNaN+a9uHj3CRlJk1r8e1vljp4mUt8wVAQ6AfzsTlTaqw+TzjYjw5egNzLODnFWWnPB2aObgZgnyJFFuUJ9Ff7HX7b8S1an5T4F5EB6QKBgQCKqJu3LoTWBYBEqpIMi2blrxaVmH6BrI4BnpTc2I9Y+GYSjX0YdgRfIrl1GaiqcjpuGON5dWhuPhLrIE0olbVpg+mYIhzS6a+nKVXyJZDAamRcBhm+p2Ncp2RJeeUGCdI1HeMWjZEnsyKP/zgfvnO/N6xvKnm6yvj3H1ExqAhfuQKBgQCkBRRPJ3sSzy1S2iPzGD41j+w/U/gI5Y9vlfSKr4XnE4ClJtY5Lz0b3f0D7WQX9hrgU+FlpY7nOYwyQVRpHyPi11ZmQ40YqzFKiwyWqswHXMOBV6QJpktgxd2SWLW8JyRTqaH70eFE1zVFdvnPCfIYyqskaHBw3xpmggEYOwFVKQKBgB9lvpzkM8AizsC9vwSILGymEP8e4MaMRDuppRu9Dfifhr18vG7limfgfQ4/GSo/Y2u6xwehxlvwQmhrkA04mTOjYynHz68Sq2u2uHd0eiqX7NHJr9q0HJPGc7cPmwSbBLZyZhGdTNkofxMMP7EwdxU9jhY+EAJ0I5wRw1jzK7JBAoGAJ8BWIAWrduZ8sikVJ7/VMh51GgNx23G6RK1j5M7R5DATNPKlJ/3smCZNqyPTq2Ah/Di/m0Jme0iKaioTD+genlYbp9szpna81yaj1Y3vaNbkhTF4l+pE5fy5BP2CmruTga3U1OshYCGNl/EXQUkc8dJbyl3wN1ty9IohpZ/L67E="+"\n"+"-----END RSA PRIVATE KEY-----")







#Generate the key first 
Key_Generation(Secret_Password, directory)

#Get the public key from this file
Public_Key = Get_Public_Key(Secret_Password, directory)

Public_Keys = [A,B,C,D]

Addresses = ["B","C","D","E"]

#The Message is encrypted in order with the addresses of the trajectory
#Traj: Me->A -> B -> C-> D(receiver)
Encrypted_Message = Prepare_and_Broadcast(C, Public_Keys, Addresses, Message_To_Decrypt)


#======= A receives a message from me =======#
Secret_Password = APriv 

Tuple = Receiver_Decryption(Secret_Password, Encrypted_Message, A)
bounce = Tuple[0]
Address = Tuple[1]
Message = Tuple[2]

print("Received")
print(str("Message: " + str(Message)))
print(str("Address: " + str(Address)))

#======= B receives a message from A =======#
Secret_Password = BPriv 

Tuple = Receiver_Decryption(Secret_Password, bounce, B)
bounce = Tuple[0]
Address = Tuple[1]
Message = Tuple[2]

print("Received")
print(str("Message: " + str(Message)))
print(str("Address: " + str(Address)))


#======= C receives a message from B =======#
Secret_Password = CPriv 

Tuple = Receiver_Decryption(Secret_Password, bounce, C)
bounce = Tuple[0]
Address = Tuple[1]
Message = Tuple[2]

print("Received")
print(str("Message: " + str(Message)))
print(str("Address: " + str(Address)))

#============D receives from C================#
Secret_Password = DPriv

Tuple = Receiver_Decryption(Secret_Password, bounce, D)
bounce = Tuple[0]
Address = Tuple[1]
Message = Tuple[2]

print("Received")
print(str("Message: " + str(Message)))
print(str("Address: " + str(Address)))
print(str("Bounce: "+ str(bounce)))



















