#!/bin/sh

# Required directories for the script. Perhaps we can make a single file with a lot of functions
current_dir=$PWD
Module="$current_dir/Module"
Communication_Module="$Module/Communication_Module.sh"
Communication_Py="$Module/Communication.py"
iri="$current_dir/Node/iri-1.4.0.jar"

#Source the shell script with all the functions 
source "$Communication_Module"

#We initiate the Node using the function Node_run
Node_run "$iri" "Run" > /dev/null 2>&1

Seed="ZGAFNTISXXXDRMJNUIOHGUHLFGPJFCASNSQBKH9TCQQCEBPTWJMFEJIB9UREHIDFXGKELLNAZQGOHIQQB"
Receiver="AJXZLAKDSGOHY9BAAXMOTDLHKANZ9VVAOHSDVJOLQEWSEAADVSKBGUYJLYG9EIJWCHVTETPRDJULGYOACONASMST9B"
Message="A final test of the function with random seed"
Server="http://cryptoiota.win:14265"

#Seed_Generator=$(Seed_Generator)
#echo "This is a random Seed: $Seed_Generator"

#Generate a random Address
Random_Address=$(Address_Generator "$Communication_Py" "$Seed")
echo "Generated: $Random_Address"

#Send the message with the address
Sending_Confirmation=$(Send_Module_Function "$Communication_Py" "$Receiver" "$Seed" "$Message" "$Random_Address" "$Server")
echo "$Sending_Confirmation"

#Download from the tangle the transaction and read the message
Received_Message=$(Receiver_Module_Function "$Communication_Py" "$Seed" "$Server")
echo "$Received_Message"


#Killing the app
PID=$(Node_run "$iri" "PID")
sleep 5
kill $PID

