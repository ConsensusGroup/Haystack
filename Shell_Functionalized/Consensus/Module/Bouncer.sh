#!/bin/sh
#!/bin/python

#######################################################################################################
#######################################################################################################
######################## Message Bouncing script with the encryption ##################################
#######################################################################################################
#######################################################################################################

#These are the required directories which we need to have:
#root="$HOME/IOTA/Consensus/"	#This is the root but it will be input $1

#Change to the root dir
#cd $root

#Make it the current working dir 
current_dir=$PWD

#Define the individual directories 
Module="$current_dir/Module"
UserData="$current_dir/UserData"

mkdir $UserData

#Complete script directories
Communication_Module="$Module/Communication_Module.sh"
Communication_Py="$Module/Communication.py"

#The server which will be used
Server="http://cryptoiota.win:14265"

#The RSA asymmetric encryption key directory:
RSA="$UserData/rsa_key.bin"
Private_Seed="$UserData/Seed.txt"

#Now source the shell script with all the functions
source $Communication_Module

#Generate the private seed
Seed_Address $UserData "Seed.txt" "Seed"

#We need to get the private seed from the user files
Private=$(Scan_Entries $Communication_Py $Private_Seed "Read")

#Generate an RSA key
Key_Generation $Communication_Py $Private $RSA

#Compose a test message which is encrypted
Send_Message="Hello there 3 using five bounces"
Receiver="QYFMQCBWBGLYRIRRWKZPYKSXGHCGMJCTFKPGRKXWHMFUKKDZAPQDKDHHHLEYUMVBEHIOEQIDCWKXTHJOZ"

#================= Initialization ============================#
Public_Seed="TKXBPWRHBHQDKYAHCQQTSQQBVGTDLJPZWORMF9IEYZCFDEFWSG9YIFBXWEYIBSRBKRFMBGTHWZGLLXPV9"

#Generate an address from the public seed
Address_Of_Public_Seed=$(Address_Generator $Communication_Py $Public_Seed $Server $UserData)

#Generate a Personal Address + Public Key to be broadcasted to the public ledger
Client_Address=$(Seed_Address $UserData "Address.txt" "Address" $Communication_Py $Private $Server)

#We now broadcast it to the public ledger 
Send_Module_Function $Communication_Py $Address_Of_Public_Seed $Private "$Client_Address" $Server

#Check the public seed to see if the sending has worked
Received=$(Receiver_Module_Function $Communication_Py $Public_Seed $Server)

Prepare_and_Broadcast $Communication_Py "$Send_Message" $Receiver $UserData $Server "5"

run="true"
while [[ "$run" == "true" ]];
do
	#Now generate a public pool file 
	Public_Addresses $Public_Seed $Server $Communication_Py $UserData

	Message=$(Receiver_Decryption $Communication_Py "$UserData/" $Server $RSA)
	echo "$Message"
done