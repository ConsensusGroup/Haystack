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

  Present_PIP="${command -v pip}"
  Version_PIP="${pip --version}"
  echo "$Present_PIP"
  echo "$Version_PIP"
  #We need to make sure that python is up to date and installed.
  apt update
  yes | apt-get install python2.7

  #Install pip
  yes | apt install python-pip
  pip2 install --upgrade pip

  #Install pyOpenSSL
  pip2 install pyOpenSSL

  #Installing PyOTA for the HayStack Protocol
  pip2 install pyota[ccurl]

  #Installing Cryptography dependencies
  pip2 install pycrypto
  pip2 install pyffx

elif [[ "$Platform" == "Mac" ]];
then
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  brew install python2
  pip install --upgrade pip setuptools

  #Install pyOpenSSL
  pip install pyOpenSSL

  #Installing PyOTA for the HayStack Protocol
  pip install pyota[ccurl]

  #Installing Cryptography dependencies
  pip install pycrypto
  pip install pyffx
fi
