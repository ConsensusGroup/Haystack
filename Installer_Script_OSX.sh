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
mkdir $IRI_DIR #### Need to add in a command that downloads the latest git version of iri.

#Getting PIP Installed.
curl https://bootstrap.pypa.io/get-pip.py -o $PIP_Dir/get-pip.py
python $PIP_Dir/get-pip.py
pip install -U pip

#Installing PyOTA for the HayStack Protocol.
pip install pyota[ccurl]

#Installing Cryptography dependencies
pip install pycrypto
pip install pyffx

#Installing brew for Java
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew cask install java
