#!/bin/bash
#!/bin/python

#We need to make sure that python is up to date and installed.
yes | apt-get install python-dev

#Install pip
apt install python-pip

#Install pyOpenSSL
pip install pyOpenSSL

#Installing PyOTA for the HayStack Protocol
pip install pyota[ccurl]

#Installing Cryptography dependencies
pip install pycrypto
pip install pyffx
