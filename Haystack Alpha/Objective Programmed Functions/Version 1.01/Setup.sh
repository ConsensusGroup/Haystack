#!/bin/sh
#Get all the needed PSA keys
sudo apt install curl
sudo add-apt-repository ppa:webupd8team/java
sudo add-apt-repository ppa:kivy-team/kivy
sudo add-apt-repository ppa:qr-tools-developers/daily
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -

#Run update on the repos 
sudo apt-get update 

#Install software 
sudo apt install python 
sudo apt-get install python-kivy
sudo apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo apt-get install -y nodejs
sudo apt-get install python-pip python-dev build-essential -y
sudo pip install --upgrade
sudo pip install --upgrade virtualenv 
sudo pip install pyota
sudo pip install opencv-python
sudo apt-get install python-qrtools -y
sudo pip install Pillow
sudo pip install pycryptodome


# install Java8
sudo apt-get install oracle-java8-installer
sudo apt-get install -y maven 

# set environment variables
sudo apt-get install oracle-java8-set-default

# confirm it was installed correctly
sudo java -version >> /dev/null

#rm docker container
sudo docker stop iri nelson
sudo docker rm iri nelson

#wget http://db.iota.partners/IOTA.partners-mainnetdb.tar.gz
cd ~
mkdir -p iri/mainnetdb
tar -xvf IOTA.partners-mainnetdb.tar.gz -C iri/mainnetdb

# run IRI with the data mounted into it
sudo docker run -d \
	--net host \
	-p 14265:14265 \
	--name iri \
	-v $(pwd)/iri/mainnetdb:/iri/mainnetdb \
	iotaledger/iri

# run nelson to manage neighbors
sudo docker run -d \
	--net host \
	-p 18600:18600 \
	--name nelson \
	romansemko/nelson.cli \
	-r localhost \
	-i 14265 \
	-u 14600 \
	-t 15600 \
	--neighbors "mainnet.deviota.com/16600 mainnet2.deviota.com/16600 mainnet3.deviota.com/16600 iotairi.tt-tec.net/16600"
