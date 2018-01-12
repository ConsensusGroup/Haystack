#!/bin/sh


#This will be the main software which the user will interact with 


# Required directories for the script.
current_dir=$PWD
Module="$current_dir/Module"
UserData="$current_dir/UserData"
Communication_Module="$Module/Communication_Module.sh"
Communication_Py="$Module/Communication.py"
iri="$current_dir/Node/iri-1.4.0.jar"
Server="http://cryptoiota.win:14265"

#Source the shell script with all the functions 
source "$Communication_Module"

#We initiate the Node using the function Node_run
#Node_run "$iri" "Run" > /dev/null 2>&1


#This is a seed which will be given to all instances of the app. Eventually we add a dynamic ledger
Public_Seed="EBKHLXYVDORUKDYREOUZJVSPXVFCERIOIDHTUDEYCZLRVPBEYVYDOHGJNAOKEUCWSAIXKJJYAZYEF9NUE" 

#This function looks a seed file. If not present it will generate a new seed
Private_Seed=$(Seed_Address "$UserData" "Seed.txt" "Seed")

#This function now looks for an address saved locally if not present it will generate a new public address from the Private Seed which will be sent to the Public Ledger.
Public_Address_To_Send=$(Seed_Address $UserData "Address.txt" "Address" $Communication_Py $Private_Seed $Server)
echo "$Public_Address_To_Send"

#We now generate a public ledger address to which we send our public address generated from the private seed
Public_Ledger=$(Address_Generator $Communication_Py $Public_Seed $Server)
echo "$Public_Ledger"

#We now generate a second address from our private seed which we use only ONCE! This is due to the Winternitz one-time signature scheme. 
One_Time_Address=$(Address_Generator $Communication_Py $Private_Seed $Server)
echo "$One_Time_Address"

#Now we send our "First generated address" (i.e. Public_Address_To_Send) to the public ledger so that people can find the address within a pool but without any identity.
Sending=$(Send_Module_Function $Communication_Py $Public_Ledger $Private_Seed $Public_Address_To_Send $Server)

#Now we check the bundles within the public ledger and check to see if our Public_Address_To_Send address is in the public ledger so others can find a contact. 
Public_Addresses=$(Public_Addresses "$Public_Seed" "$Server" "$Communication_Py")
echo "Available addresses: $Public_Addresses"




#Killing the app
#PID=$(Node_run "$iri" "PID")
#kill $PID

