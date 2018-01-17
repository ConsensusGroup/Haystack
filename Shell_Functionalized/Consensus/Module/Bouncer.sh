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
Server="http://node.hans0r.de:14265"
Public_Seed="RVGII9JLGCAVSJSJIFMOFKXQYVHRTKRDIEVOHDBGSS9WUV9B9ELTRJ9TFDPVSREDRBMZTQQSVJVGRQRTB" 

#Source the shell script with all the functions 
source "$Communication_Module"

Private_Seed="$UserData/Seed.txt"

Node_Run $iri "Run" > /dev/null 2>&1

Message_Being_Bounced=$(Bounce $Communication_Py $UserData $Server $Public_Seed)
echo "$Message_Being_Bounced"