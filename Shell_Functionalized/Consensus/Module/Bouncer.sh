#!/bin/sh
#!/bin/python

# Required directories for the script.
current_dir="$HOME/IOTA/Consensus/"
cd $current_dir
current_dir=$PWD
Module="$current_dir/Module"
UserData="$current_dir/UserData"
Communication_Module="$Module/Communication_Module.sh"
Communication_Py="$Module/Communication.py"
iri="$current_dir/Node/iri-1.4.0.jar"
Server="http://cryptoiota.win:14265"
Public_Seed="APSRUFSQXGO9HLSRLJEOZBOZKFTIVIBAUQXTCGBQFDOMYYM9CAGOHYZSUX9TQVFYWSXESWLGDCRMQWYXB" 

#Source the shell script with all the functions 
source "$Communication_Module"

Private_Seed="$UserData/Seed.txt"
Current_Public_Address_Pool="$UserData/Current_Public_Address_Pool.txt"


#Bouncing 
runtime="yes"
while [[ "$runtime" == "yes" ]];
do
	Message_Being_Bounced=$(Bounce $Communication_Py $UserData $Server $Public_Seed)
	echo "$Message_Being_Bounced"
done

