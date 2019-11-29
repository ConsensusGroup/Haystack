#!/bin/bash
#!/bin/python

#Find the current operating System being used.
Platform="None"
if [[ "$OSTYPE" == "linux-gnu" ]]; then
        Platform="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
        Platform="Mac"
fi


if [[ "$Platform" == "Linux" ]];
then
  #We need to make sure that python is up to date and installed.
  yes | apt-get install python-dev

  #Install pip
  yes | apt install python-pip
  pip install --upgrade pip
elif [[ "$Platform" == "Mac" ]];
then
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  brew install python2
  pip install --upgrade pip setuptools
fi

#Install pyOpenSSL
pip install pyOpenSSL

#Installing PyOTA for the HayStack Protocol
pip install pyota[ccurl]

#Installing Cryptography dependencies
pip install pycrypto
pip install pyffx