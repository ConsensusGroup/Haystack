#!/bin/sh
#!/bin/python

#This function installs all the software required
function Software_install() {
	#Get all the required directories
	IOTA_Node=$1
	IOTA=$2
	Consensus_dir=$3
	
	#Install all the required software
	sudo apt-get install python-all python-dev build-essential libssl-dev libffi-dev
	sudo apt-get install wget 
	sudo apt-get install git 
	sudo apt-get install python-setuptools python-pip
	sudo pip install --upgrade pip
	sudo pip install --upgrade virtualenv 
	pip install chardet
	pip install idna
	pip install cryptography
	pip install typing
	
	#Download the iri package for the node and pyOTA
	cd $IOTA_Node
	wget https://github.com/iotaledger/iri/releases/download/v1.4.0/iri-1.4.0.jar 
	cd $Consensus_dir
	cd $IOTA
	git clone https://github.com/iotaledger/iota.lib.py.git 
}

function Java_install() {	
	# We first verify that the correct version of java is installed before we can run the node.
	current_dir=$1 #Change to the current working directory for the app 
	Java_version="$current_dir/Temp" #Create a temporary folder for the version of java on the computer
	mkdir $Java_version > /dev/null 2>&1
	java -version |& tee $Java_version/version_check.txt > /dev/null 2>&1 #Save the current version onto a text file under the Java_version directory 

	#Now we open the saved text file and make sure there is a version of Java.
	text=$(<$Java_version/version_check.txt)
	Java_there=()
	while read -r line
	do
	
		if [[ "$line" == *"java version"* ]] || [[ "$line" == *"Java(TM) SE Runtime Environment"* ]] || [[ "$line" == *"Java HotSpot(TM)"* ]];
		then
			Java_there="yes"
		else
			Java_there="no"
			break
		fi
	done < "$Java_version/version_check.txt"
		
	if [[ "$Java_there" == "no" ]];
	then 
		#installs Java 8
		sudo add-apt-repository ppa:webupd8team/java < "Enter"
		sudo apt-get update 
		sudo apt-get install oracle-java8-installer
		sudo apt-get install -y maven 
			
		#setting environment variables
		sudo apt-get install oracle-java8-set-default
		break
	fi
	
	#Removing the Temp folder
	rm -r "$Java_version" > /dev/null 2>&1
}

function Installation_Check() {
	Consensus_dir=$1
	IOTA_Node=$2
	pyOTA=$3
	cd $Consensus_dir
	
	#Make sure iri is there to run the node 
	iri=($(find $IOTA_Node -name *".jar")) > /dev/null 2>&1
	if [[ "$iri" == "" ]];
	then 
		cd $IOTA_Node
		#retry the download
		echo "Retrying the download of iri"
		wget https://github.com/iotaledger/iri/releases/download/v1.4.0/iri-1.4.0.jar 
		cd $Consensus_dir
	else
		echo "iri: ...Ok"
	fi
	
	#Make sure the pyOTA lib is there. Then execute the setup.py script
	cd $pyOTA
	py=($(find $pyOTA -name *"setup.py")) > /dev/null 2>&1
	if [[ "$py" == "" ]];
	then 
		echo "Retrying the download of pyOTA"
		git clone https://github.com/iotaledger/iota.lib.py.git
	else 
		echo "pyOTA: ...Ok"
	fi
	cd iota.lib.py
	python setup.py test
}
