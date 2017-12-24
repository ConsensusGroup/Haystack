from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.adapter.wrappers import RoutingWrapper
from iota import *
import sys


#This block of code is simply the seed which can be generated online (google IOTA Wallet generator)
#The "seed" is the private key and is the most important piece in this code. It allows full access to a wallet. This seed is generated for demonstration and has no form of value.
Seed_key = str(sys.argv[1]) #User seed key
receive = str(sys.argv[2]) #Receiver address
Sending_from = str(sys.argv[4]) #Address used by sender 
message = str(sys.argv[3]) #The message which is to be sent


#This essentially connects python to the locahost which was initiated with the Java package (iri-X.X.X.X.jar) (see Node_Module.sh)
api = Iota(RoutingWrapper('https://iota.thathost.net:443').add_route('attachToTangle', 'http://localhost:14265'), seed = Seed_key)	

Send_to_IOTA=str("#'#'v'#Message: "+message+" #'#'v'#Address: "+Sending_from)
#We are now converting a message into the tribyte representation
text_transfer = TryteString.from_string(Send_to_IOTA)

#Decode the message as a test
Tryte = TryteString(str(text_transfer))
message = Tryte.as_string()

#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived. 
txn_2 = ProposedTransaction(address = Address(receive), message = text_transfer,value = 0)

#Now create a new bundle (i.e. propose a bundle)
bundle = ProposedBundle()

#Add the transaction "txn_2" to the bundle. We can also add several addresses for receiving but we get to that later.
bundle.add_transaction(txn_2)

#Send the transaction. the variable "depth" refers to the number of previous transactions being considered. 
bundle.finalize()
coded = bundle.as_tryte_strings()
send = api.send_trytes(trytes = coded, depth = 4)



#print(text_transfer)
#print(message)
#print(txn_2)
#print(send)
