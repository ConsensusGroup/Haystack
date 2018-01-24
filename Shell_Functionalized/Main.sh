#!/bin/sh

#This is how the software is supposed to flow:

#First we run the environment check. This means we see if the user already has a "UserData" folder. Plus we check if there is a private seed from which he will be sending messages. 
# ----> If not there we creat the directory and generate a seed with a public address.

#Now the user has the option if he is willing to run a full node or a light node. 
#x----> If he wants a full node we run the Full_Node script in the background but keep the user updated about the download. He will for the time being, use the light node to connect to a server which is the quickest for him. 
#------------> Still need to write a script which finds the fastest node available and connects to it

#x----> If user doesnt want full node then simply do Node_Run and this will run iri. 
#------------> Still need to write a script which finds the fastest node available and connects to it

#If user is a new user: He/She will need to connect to the public seed and backtrace all the public ledgers used. So now we run Migrator.sh (input: Module, UserData, Communication_Module, Communication_Py, iri, Server, Public_Seed) in the background but inform user about the current ledger seed.
#------------> Still to do: Save last known public seed so that the app doesnt always have to catch up.
#------------> Still to do: Add a Public_Seed validator under Scan_Entries 

#Once synced up with the ledger, messages are going to be bounced around so we invoke the "Bouncer.sh" script (input: Module, UserData, Communication_Module, Communication_Py, iri, Server, Public_Seed) and run it in the background. 

########## Outstanding tasks for the app #############
#-> Write a working bouncing method with the layered RSA encryption
#-> Add perhaps a post quantum encryption scheme 
#-> Add a restarting/Shutting down command of the iri and nelson containers of docker 
#-----------> sudo docker start nelson
#-----------> sudo docker start iri 
#-> Add a script which reads the log file of iri and tells the user when the Full Node is in sync with the other nodes. We use the command "sudo docker logs iri -f".
#-----------> Another method for users with full nodes: We can use the command "curl http://localhost:18600" to see the latest milestone. When the node is not in sync "latestMilestone": "999999999999999999999999999999999999999999999999999999999999999999999999999999999". 
#-> Make an actual GUI for the user. 
#-> Add a contact list 
#-> Add a conversation backup

###### Code Sniplets which need to be moved #######
------ Move to initialization of the app -----
#Now the user generates his Public address from his private seed.
#Client private seed which gets saved under UserData/Seed.txt
Private_Seed=$(Seed_Address $UserData "Seed.txt" "Seed")

#Client Public Address which is to be broadcasted to the network.
Client_Address=$(Seed_Address $UserData "Address.txt" "Address" $Communication_Py $Private_Seed $Server)


------ Servers for light nodes -------	
#Server_List=("http://eugene.iota.community:14265" "http://eugene.iotasupport.com:14999" "http://eugeneoldisoft.iotasupport.com:14265" "http://node01.iotatoken.nl:14265" "http://node02.iotatoken.nl:14265" "http://node03.iotatoken.nl:15265" "http://node04.iotatoken.nl:14265" "http://node05.iotatoken.nl:16265" "http://node06.iotatoken.nl:14265" "http://node.deviceproof.org:14265" "http://mainnet.necropaz.com:14500" "http://5.9.149.169:14265" "http://wallets.iotamexico.com:80" "http://5.9.137.199:14265" "http://5.9.118.112:14265" "http://88.198.230.98:14265" "http://176.9.3.149:14265" "https://n1.iota.nu:443" "http://node.lukaseder.de:14265" "https://node.tangle.works:443" "https://iota.thathost.net:443" "http://node.hans0r.de:14265" "http://cryptoiota.win:14265")







