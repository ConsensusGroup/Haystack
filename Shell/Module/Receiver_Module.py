from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.adapter.wrappers import RoutingWrapper
from iota import *
import sys




Seed_key = str(sys.argv[1]) #User seed key

api_rec = Iota(RoutingWrapper('https://iota.thathost.net:443').add_route('attachToTangle', 'http://localhost:14265'), seed = Seed_key)

#We pull the transaction history of the account (using the seed)
mess = api_rec.get_account_data(start = 0) 

#Decompose the Bundle into components
balances = mess.get('balance')
bundle = mess.get('bundles')
Address = mess.get('addresses')


message_rec=""
for i in bundle:
	message_rec = i.get_messages(errors='drop')

message=str(message_rec)

#Not a big fan of this implementation but this will have to do for now 
#This is cleans the string of the receiving side. 
clean = message.lstrip("[u'") 
splitting = str(clean).split("#'#'v'#Message: ")
splitting_Address = str(clean).split(" #'#'v'#Address: ")
splitting_Message = splitting[1].split(" #'#'v'#Address: ")
print(splitting_Message[0])
print(splitting_Address[1].rstrip('"]'))


