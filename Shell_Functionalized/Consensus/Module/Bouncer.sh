#!/bin/sh
#!/bin/python

# Required directories for the script.
current_dir="$HOME/IOTA/Consensus/"
cd $current_dir
current_dir=$PWD
Module="$current_dir/Module"
UserData="$current_dir/UserData"
Communication_Module="$Module/Communication_Module.sh"
Communication_Py="$Module/Communication.py"
iri="$current_dir/Node/iri-1.4.0.jar"
Server="http://node.hans0r.de:14265"
Public_Seed="RVGII9JLGCAVSJSJIFMOFKXQYVHRTKRDIEVOHDBGSS9WUV9B9ELTRJ9TFDPVSREDRBMZTQQSVJVGRQRTB" 

#Source the shell script with all the functions 
source "$Communication_Module"

Private_Seed="$UserData/Seed.txt"

#Read the private seed for detecting messages
while read line 
do 
	Private_Seed=$line
done < "$Private_Seed"

Address_Pool="$UserData/Current_Public_Address_Pool.txt"



run="true"
Message="PC"
while [ "$run" == "true" ];
do
	Message="PC$Message"
	
	#We now find the current pool of addresses from the public ledger
	Addresses=$(Public_Addresses $Public_Seed $Server $Communication_Py $UserData)

	#This now choses a random address from the public pool
	Address=$(Random_Bounce $Communication_Py $Address_Pool)
	
	#Just for demonstration we want to bounce the message now 
	Sending=$(Send_Module_Function $Communication_Py $Address $Private_Seed $Message $Server)
	
	#Here we need to include a decryption method for the messages (Needs to be still implemented)
	#Decrypted_Message=....
	
	#Retrieve current messages in for the private seed
	Message=$(Receiver_Module_Function $Communication_Py $Private_Seed $Server)
	echo "$Message"
	
done 
