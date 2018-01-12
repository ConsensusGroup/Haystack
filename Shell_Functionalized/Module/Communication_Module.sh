#!/bin/sh
#!/bin/python

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
	python $Communication "$Module" "$Seed" "$Receive" "$Message" "$Server" 
}

#This function will run the Receiving module in python
function Receiver_Module_Function() {
	Communication=$1
	Seed=$2
	Server=$3
	Module="Receiver_Module"
	output=$(python $Communication "$Module" "$Seed" "$Server")
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
	Module="Public_Addresses"
	Addresses=$(python $Communication $Module $Public_Seed $Server)
	echo "$Addresses"
}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
