#!/bin/bash
#!/bin/python

#First we make a directory so that all the needed libraries are installed.
#Assume that nothing is installed.

#Main directories
ROOT_Dir=$PWD
INSTALLER_Dir=$PWD/INSTALLER
PIP_Dir=$PWD/INSTALLER/PIP
IRI_DIR=$PWD/IRI

#Creating directories:
mkdir $INSTALLER_Dir
mkdir $PIP_Dir

#Getting PIP Installed.
curl https://bootstrap.pypa.io/get-pip.py -o $PIP_Dir/get-pip.py
python $PIP_Dir/get-pip.py
pip install -U pip

#We need to make sure that python is up to date and installed.
yes | apt-get install python-dev
#Here we need to install Java
yes | apt install openjdk-8-jre-headless

#Installing PyOTA for the HayStack Protocol
pip install pyota[ccurl]

#Installing Cryptography dependencies
pip install pycrypto
pip install pyffx

#Here we do the clean up.
rm -rf $INSTALLER_Dir
