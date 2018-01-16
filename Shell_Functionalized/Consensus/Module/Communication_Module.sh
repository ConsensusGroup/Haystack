#!/bin/sh
#!/bin/python

########################################################################################
############################### Constants of the Protocol ##############################
########################################################################################
	
Server_List=("http://eugene.iota.community:14265" "http://eugene.iotasupport.com:14999" "http://eugeneoldisoft.iotasupport.com:14265" "http://node01.iotatoken.nl:14265" "http://node02.iotatoken.nl:14265" "http://node03.iotatoken.nl:15265" "http://node04.iotatoken.nl:14265" "http://node05.iotatoken.nl:16265" "http://node06.iotatoken.nl:14265" "http://node.deviceproof.org:14265" "http://mainnet.necropaz.com:14500" "http://5.9.149.169:14265" "http://wallets.iotamexico.com:80" "http://5.9.137.199:14265" "http://5.9.118.112:14265" "http://88.198.230.98:14265" "http://176.9.3.149:14265" "https://n1.iota.nu:443" "http://node.lukaseder.de:14265" "https://node.tangle.works:443" "https://iota.thathost.net:443" "http://node.hans0r.de:14265" "http://cryptoiota.win:14265")





#This function will run the Node 
function Node_run() {
	iri=$1
	Method=$2
	if [[ "$Method" == "Run" ]];
	then
		java -jar $iri -p 14265 &
	fi
	if [[ "$Method" == "PID" ]];
	then
		process=$(ps ax | grep $iri) #enquires the system for the process id of the iri java 
		for i in ${process[@]};
		do	
			break 
		done
		echo "$i"
	fi
}

#This function generates a random address when called
function Address_Generator() {
	Communication=$1
	Seed=$2
	Server=$3
	Module="Address_Generator"
	output=$(python $Communication $Module "$Seed" "$Server")
	echo "$output"
}

#This function broadcasts the message into the tangle
function Send_Module_Function() {
	Communication=$1
	Receive=$2
	Seed=$3
	Message=$4
	Server=$5
	Module="Sender_Module"
	Sender=$(python $Communication $Module $Seed $Receive $Message $Server)
	echo "$Sender"
}

#This function will run the Receiving module in python
function Receiver_Module_Function() {
	Communication=$1
	Seed=$2
	Server=$3
	Module="Receiver_Module"
	output=$(python $Communication $Module $Seed $Server)
	echo "$output"
}

#This function will generate a new seed if the user does not have one 
function Seed_Module_Generator() {
	Private_Seed=`cat /dev/urandom |tr -dc A-Z9|head -c${1:-81}`
	echo "$Private_Seed"
}

#This function will search for a Seed or Address in a given directory
function Seed_Address() {
	Directory=$1
	Name_Of_File=$2
	Purpose=$3
	File=($(find $Directory -name $Name_Of_File))
	User="$UserData/$Name_Of_File"
	
	#With this option it finds or generates a new seed
	if [[ "$Purpose" == "Seed" ]];
	then
		if [[ "$File" == "" ]];
		then	
			Private_Seed=$(Seed_Module_Generator)
			echo "$Private_Seed" > $User
		fi
	
	#This option will either generate a new address visible to a public ledger or retrieve an existing one.
	elif [[ "$Purpose" == "Address" ]];
	then
		if [[ "$File" == "" ]];
		then	
			Communication=$4
			Seed=$5
			Server=$6
			Address=$(Address_Generator $Communication $Seed $Server)
			echo "$Address" > $User
		fi
	fi
	while read -r line
	do
		echo "$line"
	done < "$User"
}

function Public_Addresses() {
	Public_Seed=$1
	Server=$2
	Communication=$3
	SaveToDirectory=$4
	Module="Public_Addresses"
	Addresses=$(python $Communication $Module $Public_Seed $Server $SaveToDirectory)
	echo "$Addresses"
}

function Random_Bounce() {
	Communication=$1
	Public_Addresses=$2
	Module="Random_Bounce"
	Random_Address_From_Public_Ledger=$(python $Communication $Module "$Public_Addresses")
	echo "$Random_Address_From_Public_Ledger"
}

	
	
	
	
	
	
	
	
	
	
	
	
