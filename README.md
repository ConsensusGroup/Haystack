This is the "Consensus" platform. The aim of the project is to implement a communication mechanism through the IOTA Tangle network to broadcast some form of message. 

For the whitepaper of the IOTA project see: https://iota.org/IOTA_Whitepaper.pdf

You can develop in any programming language. 

To install the IOTA python libaries on linux do the following:
1. Open a linux terminal 
2. install git 
3. write the following command "git clone https://github.com/iotaledger/iota.lib.py.git"
4. cd into the "iota.lib.py" folder. This will have a python script called "setup.py"
5. issue the following command into the terminal "python setup.py test". Now this will take a while to finish.
6. run your preferred python interface (e.g. ipython) and issue the following command "import iota"
7. If there are no errors you should now have the libaries completely installed and you are ready to work with the pyOTA libaries.


Some useful documentation:
- https://media.readthedocs.org/pdf/pyota/develop/pyota.pdf

To interact with the Tangle on linux:
1. Make sure your linux OS has java installed.
2. Download the "iri-X.X.X.X.jar" file from "https://github.com/iotaledger/iri/releases"
3. Once downloaded "cd" into the .jar directory (e.g. Downloads folder) 
4. Issue the following command to the command line of your terminal console: "java -jar iri-X.X.X.X.jar -p 14265"
5. You have now connected to the Tangle network and are able to interact with it.
6. Happy coding!!! =)




For those who are new to GitLab here are some useful commands:

######Command line instructions###########
------Git global setup--------

git config --global user.name "Thomas Nommensen"
git config --global user.email "thomas.nommensen@coepp.org.au"

------Create a new repository-------

git clone git@gitlab.com:woywoy123/Consensus.git
cd Consensus
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master

------Existing folder-------

cd existing_folder
git init
git remote add origin git@gitlab.com:woywoy123/Consensus.git
git add .
git commit -m "Initial commit"
git push -u origin master

-------Existing Git repository---------

cd existing_repo
git remote rename origin old-origin
git remote add origin git@gitlab.com:woywoy123/Consensus.git
git push -u origin --all
git push -u origin --tags

##### How to use the functions in the shell script #######
Initialization_Module.sh
-Software_install
    1. Directory where to save the Node contents
    2. Directory where to save the IOTA api or python library
    3. Root Directory i.e. Consensus
    
-Java_install
    1. Current working directory 

-Software_install
    1. Root Directory i.e. Consensus
    2. Directory where to save the Node contents
    3. Directory where to save the IOTA api or python library
    
Communication_Module.sh
-Node_Run
    No input args

-Address_Generator
    1. Directory of "Communication.py"
    2. Seed
    3. Light node server

-Send_Module_Function
    1. Directory of "Communication.py"
    2. Receiver 
    3. Seed
    4. String (message)
    5. Light node server
    
-Receiver_Module_Function
    1. Directory of "Communication.py"
    2. Seed
    3. Light node server
    
-Seed_Module_Generator 
    No input args
    
-Seed_Address
    1. Directory of file to find
    2. Name of file 
    3. the purpose of the file (i.e. Seed or Address)
    
-Public_Addresses
    1. Seed
    2. Light node server
    3. Directory of "Communication.py"
    4. Destination directory of where to save the text file
    
-Bounce
    1. Directory of "Communication.py"
    2. UserData folder directory
    3. Light node server
    4. Public Seed 

-Full_Node
    No input args




