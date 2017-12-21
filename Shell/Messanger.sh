#!/bin/sh
#!/bin/ipython

#==========================INITIALIZATION===================================#
# We first verify that the correct version of java is installed before we can run the node.
current_dir=$PWD #Change to the current working directory for the app 
Java_version="$current_dir/Temp" #Create a temporary folder for the version of java on the computer
mkdir $Java_version > /dev/null 2>&1
java -version |& tee $Java_version/version_check.txt > /dev/null 2>&1 #Save the current version onto a text file under the Java_version directory 

#Now we open the saved text file and make sure there is a version of Java.
text=$(<$Java_version/version_check.txt)
Java_there=()
while read -r line
do
	if [[ "$line" == *"java"* ]] || [[ "$line" == *"Java"* ]] ;
	then
		Java_there="yes"
	else
		Java_there="no"
		break
	fi
done < "$Java_version/version_check.txt"


#Now according to the above we install the appropriate java for the full node
#Install Java8
menu=("No" "yes")
if [[ "$Java_there" == "no" ]];
then 
	echo "The version of Java on this computer wont work with the IOTA platform and needs to be installed! Would you like to install Java 8 now and continue with the messanger installation?"
	select choice in "${menu[@]}";
	do 
		if [[ "$choice" == "No" ]];
		then
			echo "Abording the installation..."
			break 
		else
			#installs Java 8
			sudo add-apt-repository ppa:webupd8team/java < "Enter"
			sudo apt-get update 
			sudo apt-get install oracle-java8-installer
			sudo apt-get install -y maven 
			
			#setting environment variables
			sudo apt-get install oracle-java8-set-default
			sudo apt-get install git
			break
		fi
	done
fi

#Removing the Temp folder
rm -r "$Java_version" > /dev/null 2>&1

#Downloading the software for the full node
IOTA_Node="$current_dir/Node"
mkdir $IOTA_Node > /dev/null 2>&1
cd $IOTA_Node

#Check if the iri package is there
iri=($(find $IOTA_Node -name *".jar")) > /dev/null 2>&1
if [[ "$iri" == "" ]];
then 
	wget https://github.com/iotaledger/iri/releases/download/v1.4.0/iri-1.4.0.jar #Downloads the iri package for the node
fi
cd $current_dir

#This segment will now initiate the node but quietly so that it wont display text in the 
#actual app. 
Module="$current_dir/Module"
Node_Module=($(find $Module -name "Node_Module.sh"))
bash $Node_Module "$iri" "$IOTA_Node" > /dev/null 2>&1 & 

#Collect the process name so we can kill it after when the software is closed
process_saved="$IOTA_Node/process.txt"
rm $process_saved #deletes and existing process files
process=$(ps ax | grep $iri) #enquires the system for the process id of the iri java 
echo "$process" >> $process_saved #saves the process in a text file (temp)
while read -r line
do
	sleep 2
	if [[ "$line" == *"java -jar $iri -p 14265" ]];
	then
		process=${line%% *} #Cuts the string to extract PID
	fi 
done < "$process_saved"

#This makes sure the computer has the pyOTA package installed. If not then it will install
pyOTA="$current_dir/IOTA"
py=($(find $pyOTA -name *"setup.py")) > /dev/null 2>&1
if [[ "$py" == "" ]];
then 
	mkdir $pyOTA
	cd $pyOTA
	git clone https://github.com/iotaledger/iota.lib.py.git
	echon "Installing pyOTA python libaries please wait..."
	cd iota.lib.py
	ipython setup.py test
fi
#==========================INITIALIZATION END==============================#





#============================IOTA Messanger================================#
Quit="False"
Seed_Key="WCGOWTHOWPC9KYYDLOEDDZMUHPWVASCWPTX9PZEPWWNKNNEETCPZISMZTM99GNRCZQ9GGOBIBKNYNSPAS"
Local_Address="NPBXSOXDPLXSCSZIVQCJBHPLJONYBZEASZHDXWPYDLBXXTH9HORYWTDZEXZODIHGF9QBIB9OZTKFMFUVDGBAHFYXPD"
while $Quit == "False";
do
	
done 



























sleep 10
kill $process
