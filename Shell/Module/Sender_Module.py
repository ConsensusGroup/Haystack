from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.adapter.wrappers import RoutingWrapper
from iota import *
import sys

Seed_key = str(sys.argv[1])
receive = str(sys.argv[2])

#This block of code is simply the seed which can be generated online (google IOTA Wallet generator)
#The "seed" is the private key and is the most important piece in this code. It allows full access to a wallet. This seed is generated for demonstration and has no form of value.
Seed_key = "WCGOWTHOWPC9KYYDLOEDDZMUHPWVASCWPTX9PZEPWWNKNNEETCPZISMZTM99GNRCZQ9GGOBIBKNYNSPAS"
receive='NPBXSOXDPLXSCSZIVQCJBHPLJONYBZEASZHDXWPYDLBXXTH9HORYWTDZEXZODIHGF9QBIB9OZTKFMFUVDGBAHFYXPD'

#This essentially connects python to the locahost which was initiated with the Java package (iri-X.X.X.X.jar)
api = Iota(RoutingWrapper('https://iota.thathost.net:443').add_route('attachToTangle', 'http://localhost:14265'), seed = Seed_key)	


#We are now converting a message into the tribyte representation
text_transfer = TryteString.from_string("This is a test")
print(text_transfer)

#Decode the message as a test
Tryte = TryteString(str(text_transfer))
message = Tryte.as_string()
print(message)

#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived. 
txn_2 = ProposedTransaction(address = Address(receive), message = text_transfer,value = 0)

print(txn_2)

#Now create a new bundle (i.e. propose a bundle)
bundle = ProposedBundle()

#Add the transaction "txn_2" to the bundle. We can also add several addresses for receiving but we get to that later.
bundle.add_transaction(txn_2)

#Send the transaction. the variable "depth" refers to the number of previous transactions being considered. 
bundle.finalize()
coded = bundle.as_tryte_strings()
send = api.send_trytes(trytes = coded, depth = 4)

print(send)
