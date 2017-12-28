#!/bin/sh

#First we build all the directories needed for the application
current_dir=$PWD #Find the current working directory. From here we build the app

#Set the directories which we will use
Consensus="$current_dir/Consensus" #Root directory of application 
Node="$Consensus/Node"
IOTA="$Consensus/IOTA"
Module="$Consensus/Module"

#Build the Consensus directory
mkdir $Consensus
mkdir $Node
mkdir $IOTA
mkdir $Module

#Find the tar file so the files can be placed in the correct directory
package=($(find $current_dir -name *".tar.gz")) > /dev/null 2>&1
tar -xzvf "$package" -C "$Module/"

#Now start the initialization script to setup the correct environment
Initialization="$Module/Initialization_Module.sh"


#Source the script for the required functions 
source $Initialization

#Run the functions individually
echo "For the software to run properly please enter your password"
Software_install "$Node" "$IOTA" "$Consensus"
Java_install "$Consensus"
Installation_Check "$Consensus" "$Node" "$IOTA"

#Move the Messanger app to the correct directory
mv "$Module/Messanger.sh" $current_dir




