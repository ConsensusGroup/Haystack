#!/bin/sh
#!/bin/python

########################################################################################
############################### Constants of the Protocol ##############################
########################################################################################
	
Server_List=("http://eugene.iota.community:14265" "http://eugene.iotasupport.com:14999" "http://eugeneoldisoft.iotasupport.com:14265" "http://node01.iotatoken.nl:14265" "http://node02.iotatoken.nl:14265" "http://node03.iotatoken.nl:15265" "http://node04.iotatoken.nl:14265" "http://node05.iotatoken.nl:16265" "http://node06.iotatoken.nl:14265" "http://node.deviceproof.org:14265" "http://mainnet.necropaz.com:14500" "http://5.9.149.169:14265" "http://wallets.iotamexico.com:80" "http://5.9.137.199:14265" "http://5.9.118.112:14265" "http://88.198.230.98:14265" "http://176.9.3.149:14265" "https://n1.iota.nu:443" "http://node.lukaseder.de:14265" "https://node.tangle.works:443" "https://iota.thathost.net:443" "http://node.hans0r.de:14265" "http://cryptoiota.win:14265")

########################################################################################
#################### Things to still do for the functions ##############################
########################################################################################
#-Need to add an encryption method for the messages presumably we use IOTA api 
#-A timeout function for the different servers to find the fastest one available to user
#-Add the dynamic ledger solution (we migrate away from the static one)
#-Need to find a full node script which finds neighbours (see https://github.com/deltaskelta/iota-iri)
#-Imoprove the bouncing function (add full anon (goes through all addresses) or partial anon)


########################################################################################
############################### Start of all functions #################################
########################################################################################

#This function will run the Node 
function Node_Run() {
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

#This needs to be properly checked and tested therefore not quite final. 
function Full_Node(){
	
	#First we need to install docker this worked on my machine 16.04 LTS UBUNTU
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
	sudo apt-get update
	apt-cache policy docker-ce
	sudo apt-get install -y docker-ce
	
	#This part now runs the full node script (This was taken from the reddit page: https://www.reddit.com/r/Iota/comments/7pwfpp/launch_a_full_iota_node_with_one_command/)
	# change to the home directory
	cd ~

	# download the current tangle database
	wget http://db.iota.partners/IOTA.partners-mainnetdb.tar.gz

	# make a data directory for the database and unpack it
	mkdir -p iri/mainnetdb
	tar -xvf IOTA.partners-mainnetdb.tar.gz -C iri/mainnetdb

	# run IRI with the data mounted into it
	docker run -d \
 	   --net host \
 	   -p 14265:14265 \
 	   --name iri \
 	   -v $(pwd)/iri/mainnetdb:/iri/mainnetdb \
  	  iotaledger/iri

	# run nelson to manage neighbors
	docker run -d \
	   --net host \
	   -p 18600:18600 \
 	   --name nelson \
 	   romansemko/nelson.cli \
 	   -r localhost \
 	   -i 14265 \
 	   -u 14777 \
	   -t 15777 \
 	   --neighbors "mainnet.deviota.com/16600 mainnet2.deviota.com/16600 mainnet3.deviota.com/16600 iotairi.tt-tec.net/16600"
}

#This function generates a random address when called
function Address_Generator() {
	Communication=$1
	Seed=$2
	Server=$3
	Module="Address_Generator"
	output=$(python $Communication $Module $Seed $Server)
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

function Scan_Entries() {
	Communication_Py=$1
	Directory_Of_File=$2
	Purpose=$3
	
	Module="Scan_Entries"
	Entry=$(python $Communication_Py $Module $Directory_Of_File $Purpose)
	echo "$Entry"
}

#This bounce method is a primitive solution we still need to add some other stuff to this. 
function Bounce() {
	
	#Input variables 
	Communication_Py=$1
	UserData=$2
	Server=$3
	Public_Seed=$4
	
	#User Data being called see the folder "UserData"
	Private_Seed="$UserData/Seed.txt"
	Address_Pool="$UserData/Current_Public_Address_Pool.txt"
	
	#Read the private seed for detecting messages
	while read line 
	do 
		Private_Seed=$line
	done < "$Private_Seed"
	
	run="true"
	while [ "$run" == "true" ];
	do
		#Retrieve current messages in for the private seed
		Message=$(Receiver_Module_Function $Communication_Py $Private_Seed $Server)
		echo "$Message"	
		
		#If there is no message i.e. empty string then just skip the bounce
		if [[ "$Message" == "" ]];
		then 
			continue
			
		#otherwise bounce a message 
		else
			#We now find the current pool of addresses from the public ledger
			Addresses=$(Public_Addresses $Public_Seed $Server $Communication_Py $UserData)

			#This now choses a random address from the public pool (Or we can include all)
			Address=$(Random_Bounce $Communication_Py $Address_Pool)
		
			#Bounce the message now 
			Sending=$(Send_Module_Function $Communication_Py $Address $Private_Seed $Message $Server)
	
			#Here we need to include a decryption method for the messages (Needs to be still implemented)
			#Decrypted_Message=....
			run="false"
		fi
	done 
}
	
function Dynamic_Ledger() {
	Communication_Py=$1
	Public_Seed=$2
	Max_Address_Pool=$3
	UserData=$4
	Server=$5
	
	#Some hardcoded stuff like the txt file 
	Current_Public_Address_Pool="$UserData/Current_Public_Address_Pool.txt"
	Module="Dynamic_Ledger"
	
	#Counts number of addresses
	Dynamic=$(python $Communication_Py $Module $Public_Seed $Max_Address_Pool $Current_Public_Address_Pool)
	
	#This decides if there will be a new seed generated
	if [[ "$Dynamic" == "True" ]];
	then
		#Generate a new address using the PUBLIC SEED!
		Send_To_Public_Ledger=$(Seed_Address $UserData "TempAddress.txt" "Address" $Communication_Py $Public_Seed $Server)
		
		#Remove the temp text file
		rm "$UserData/TempAddress.txt"

		#Generate a new Public Seed
		New_Seed=$(Seed_Module_Generator)
		Instruction="#New_Seed#$New_Seed"
		
		#Send the new Public Seed to the current Public Seed 
		Broadcast_New_Seed=$(Send_Module_Function $Communication_Py $Send_To_Public_Ledger $Public_Seed $Instruction $Server) 
	fi
}

function Ledger_Migration() {
	
	#Input variables 
	Communication_Py=$1
	UserData=$2
	Server=$3
	Public_Seed=$4
	
	SaveToDirectory="$UserData/Current_Public_Address_Pool.txt"
	Old_List="$UserData/Current_Public_Address_Pool_Old.txt"
	User="$UserData/Address.txt"
	Private_Seed="$UserData/Seed.txt"
	
	#Reading the private seed from the text file
	while read line 
	do 
		Private_Seed=$line
	done < "$Private_Seed"
	
	#Generate an address from the private seed
	Address=$(Address_Generator $Communication_Py $Private_Seed $Server)
	echo "$Address" >> $User
	
	#Read the seed from the saved file "Current_Public_Address_Pool.txt" 
	New_Public_Seed=$(Scan_Entries $Communication_Py $SaveToDirectory "Seed")
	echo "$New_Public_Seed"
	
	#Generate a new public ledger address 
	Receive=$(Address_Generator $Communication_Py $New_Public_Seed $Server)
	echo "$Receive"
	
	#Send new public address to new Public Seed
	send=$(Send_Module_Function $Communication_Py $Receive $Private_Seed $Address $Server)

	#Save new Current_Public_Address_Pool.txt and replace the previous one
	mv $SaveToDirectory $Old_List
	New_List=$(Public_Addresses $New_Public_Seed $Server $Communication_Py $UserData)
}