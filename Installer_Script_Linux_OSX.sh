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

  if [[ $(command -v pip) == "" ]];
  then
    echo "Installing pip and python2.7"
    # We need to make sure that python is up to date and installed.
    apt update
    yes | apt-get install python2.7

    #Install pip
    for i in 1 2;
    do
      (yes | apt install python-pip) || echo "Hello"
      (pip2 install --upgrade pip) || echo "Hello2"
    done
    pip="False"

  elif [[ $(command -v pip) == "/usr/local/bin/pip" ]];
  then
    if [[ $(pip --version) == *"pip (python 2.7)"* ]];
    then
      pip="True"
    fi
  fi


  if [[ $pip == "True" ]];
  then
    pip install pyOpenSSL
    pip install pyota[ccurl]
    pip install pycrypto
    pip install pyffx
  elif [[ $pip == "False" ]];
  then
    #Install pyOpenSSL
    pip2 install pyOpenSSL

    #Installing PyOTA for the HayStack Protocol
    pip2 install pyota[ccurl]

    #Installing Cryptography dependencies
    pip2 install pycrypto
    pip2 install pyffx
  fi

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
