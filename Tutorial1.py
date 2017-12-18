from iota import TryteString, Address, ProposedBundle, ProposedTransaction
from iota.crypto.signing import KeyGenerator
from iota.adapter.wrappers import RoutingWrapper
from iota import *


seed = "XHLNPBBWDLJEUDINTHWTFODMB9VAOUVRCVDMFOQEOCPZSVWXGNWU9PKWFUFUMHG9YZBBNIOTIUJWUXRMD"
receive="QNFGLUUSK9KTPYTNOEAWWNWPGUAKZNPYLSRTOKBCJKGXXRBARXEYQ9BXAGFKAYCGMLYPMXNZNADWF9IHAZYZXLSQAW"

api = Iota(RoutingWrapper('https://iota.thathost.net:443').add_route('attachToTangle', 'http://localhost:14265'), seed = b'XHLNPBBWDLJEUDINTHWTFODMB9VAOUVRCVDMFOQEOCPZSVWXGNWU9PKWFUFUMHG9YZBBNIOTIUJWUXRMD')	

print(api)

txn_2 = \
	ProposedTransaction(address = Address(receive), message = TryteString.from_string("This is a really long text which is to test whether this thing actually works properly"),value = 0)

bundle = ProposedBundle()

bundle.add_transaction(txn_2)
bundle.finalize()
bundle.sign_inputs(KeyGenerator(seed))
coded = bundle.as_tryte_strings()
t = api.send_trytes(trytes = coded, depth = 3)



#This is now the receiving end. The purpose is to verify the chain of commands. 
api_rec=Iota(RoutingWrapper('https://iota.thathost.net:443').add_route('attachToTangle', 'http://localhost:14265'), seed = 'XHLNPBBWDLJEUDINTHWTFODMB9VAOUVRCVDMFOQEOCPZSVWXGNWU9PKWFUFUMHG9YZBBNIOTIUJWUXRMD')

mess = api_rec.get_account_data(start=0,stop =1)
print(mess)

