from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.adapter.wrappers import RoutingWrapper
from iota import *
import sys

Seed_key = "WCGOWTHOWPC9KYYDLOEDDZMUHPWVASCWPTX9PZEPWWNKNNEETCPZISMZTM99GNRCZQ9GGOBIBKNYNSPAS"
api_rec = Iota(RoutingWrapper('https://iota.thathost.net:443').add_route('attachToTangle', 'http://localhost:14265'), seed = Seed_key)

#We pull the transaction history of the account (using the seed)
mess = api_rec.get_account_data(start = 0) 

#Decompose the Bundle into components
balances = mess.get('balance')
bundle = mess.get('bundles')
Address = mess.get('addresses')

print(bundle[0])
print(Address)
bun = bundle[0]
message_rec = bun.get_messages(errors='drop')
print(message_rec)
