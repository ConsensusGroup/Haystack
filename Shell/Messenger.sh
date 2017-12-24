#!/bin/sh

# Required directories for the script. Perhaps we can make a single file with a lot of functions
current_dir=$PWD
Ini_Module="$current_dir/Module/Initialization_Module.sh" #Shell script
Send_Module="$current_dir/Module/Send_Module.sh" #Shell script
Sender_Module="$current_dir/Module/Sender_Module.py" #Python script
Receive_Module="$current_dir/Module/Receive_Module.sh" #Shell Script
Receiver_Module="$current_dir/Module/Receiver_Module.py" #Python Script
Addresses_Generator="$current_dir/Module/Addresses_Generator.sh" #Shell Script
Address_Generator="$current_dir/Module/Address_Generator.py" #Python Script


#Sourced scripts due to function (Might want to implement these into a single file later)
source ./Consensus/Shell/Module/Receive_Module.sh
source ./Consensus/Shell/Module/Addresses_Generator.sh


Seed="ZGAFNTISXXXDRMJNUIOHGUHLFGPJFCASNSQBKH9TCQQCEBPTWJMFEJIB9UREHIDFXGKELLNAZQGOHIQQB"
Receiver="AJXZLAKDSGOHY9BAAXMOTDLHKANZ9VVAOHSDVJOLQEWSEAADVSKBGUYJLYG9EIJWCHVTETPRDJULGYOACONASMST9B"
Message="We can generate a random address and receive a message lol we will win cunts!"

#Start the Node
bash $Ini_Module

#Generate a random address
Random_Address=$(Address_Generator "$Address_Generator" "$Seed")

#Send the message with the address
bash $Send_Module "$Sender_Module" "$Receiver" "$Seed" "$Message" "$Random_Address"

#Download from the tangle the transaction and read the message
Received_Message=$(Receiver_Module_Function "$Receiver_Module" "$Seed")

echo "$Received_Message"
wait







#End of app
process_txt="$current_dir/Consensus/Shell/Node/PID.txt"
while read -r line
do
	process=${line%% *} #Cuts the string to extract PID
done < "$process_txt"

sleep 2
#Clean up session
kill $process
cd ~/
rm -rf ~/ixi
rm -rf ~/mainnet.log
rm -rf ~/mainnetdb
