#!/bin/sh

# Required directories for the script.
Module=$1
UserData=$2
Communication_Module=$3
Communication_Py=$4
iri=$4 #Relevant only if user does not want full node
Server=$5
Public_Seed=$6 #"WNP9GHNTNJGMEFZHTYTEEILEDHNZFSNJGVVSDDLAVXVHRQDLSKKPRTNEZVFFXQCVKFCFHKYTXZTXVRLNF"
Pool_Threshold=$7 

#Source the shell script with all the functions 
source "$Communication_Module"


#Need to change to while loop and find some condition. Maybe have a temp file saved in the UserData dir and make the script read it until some signal to terminate loop is imposed. 
for ((x=1; x<=20; x++));
do
	
	#We now want to save all the public addresses on the ledger to a local file
	Public_Addresses=$(Public_Addresses $Public_Seed $Server $Communication_Py $UserData)

	#Now we want to determine if we need to perform a ledger migration.
	Gen=$(Dynamic_Ledger $Communication_Py $Public_Seed $Pool_Threshold $UserData $Server)
	
	#Temporarily save the previous seed
	Previous=$Public_Seed
	
	#Perform the migration.
	echo "$Communication_Py $UserData $Server $Public_Seed"
	Public_Seed=$(Ledger_Migration $Communication_Py $UserData $Server $Public_Seed)
	
	if [[ "$Public_Seed" == "" ]];
	then
	
		Public_Seed=$Previous
		
	elif [[ "$Public_Seed" != "" ]];
	then
	
		#Some public address from the public seed so that client can send current address to public ledger.
		Address_Of_Public_Seed=$(Address_Generator $Communication_Py $Public_Seed $Server)

		#We now broadcast it to the public ledger 
		Send=$(Send_Module_Function $Communication_Py $Address_Of_Public_Seed $Private_Seed $Client_Address $Server)
		
	fi
	
	echo "Current Seed: $Public_Seed"
done 

