#!/bin/sh


#This will be the main software which the user will interact with 


# Required directories for the script.
current_dir=$PWD
Module="$current_dir/Module"
UserData="$current_dir/UserData"
Communication_Module="$Module/Communication_Module.sh"
Communication_Py="$Module/Communication.py"
iri="$current_dir/Node/iri-1.4.0.jar"
Server="http://node.hans0r.de:14265"
Public_Seed="SKUMGBMQIYQBHBGB9OLW9FXCHFBSWOXJWQIUAIVDZNARRRYEGGJCCNZA9KRZYWUHZOQCWBJKKRERCZEMP"

#Source the shell script with all the functions 
source "$Communication_Module"

PID=$(Node_Run "$iri" "PID")

if [[ "$PID" == "" ]];
then
	#We initiate the Node using the function Node_run
	Node_run "$iri" "Run" > /dev/null 2>&1
fi

#New User Enters the network. We need to create a folder for his data. 
mkdir $UserData

#Now the user generates his Public address from his private seed.
#Client private seed which gets saved under UserData/Seed.txt
Private_Seed=$(Seed_Address $UserData "Seed.txt" "Seed")

#Client Public Address which is to be broadcasted to the network.
Client_Address=$(Seed_Address $UserData "Address.txt" "Address" $Communication_Py $Private_Seed $Server)

#Some public address from the public seed so that client can send current address to public ledger.
Address_Of_Public_Seed=$(Address_Generator $Communication_Py $Public_Seed $Server)

#We now broadcast it to the public ledger 
Send=$(Send_Module_Function $Communication_Py $Address_Of_Public_Seed $Private_Seed $Client_Address $Server)

#We now want to save all the public addresses on the ledger to a local file
Public_Addresses=$(Public_Addresses $Public_Seed $Server $Communication_Py $UserData)




#Killing the app
#PID=$(Node_run "$iri" "PID")
#kill $PID
