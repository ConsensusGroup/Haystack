from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.adapter.wrappers import RoutingWrapper
from iota import *
from random import SystemRandom
import random
from multiprocessing.pool import ThreadPool


#from iota.commands.core import get_node_info


class Background:

	#Example use case:
	#Background(function = Example().ExampleFunction, arguments = str("{'test': 3}")).Run()

	def __init__(self, function, arguments = "()"):
		self.Variable = ""
		self.Function = function
		self.Arg = arguments

	def Run(self):
		Pool = ThreadPool(processes = 1)
		Start = Pool.apply_async(self.Function, eval(self.Arg))


######### Base Classes ###########
class IOTA_Module:
	def __init__(self, Seed, Server = "http://localhost:14265"):
		self.api = Iota(RoutingWrapper(str(Server)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed)

	def Sending(self, ReceiverAddress, Message):
		text_transfer = TryteString.from_string(str(Message))
		#This now proposes a transaction to a person. The "message = ..." command is a message that the receiver should be able to decode once arrived.
		txn_2 = ProposedTransaction(address = Address(ReceiverAddress), message = text_transfer, value = 0)
		#Now create a new bundle (i.e. propose a bundle)
		bundle = ProposedBundle()
		#Add the transaction "txn_2" to the bundle. We can also add several addresses for receiving but we get to that later.
		bundle.add_transaction(txn_2)
		bundle.finalize()
		coded = bundle.as_tryte_strings()
		send = self.api.send_trytes(trytes = coded, depth = 4)

	def Receive(self):
		#We pull the transaction history of the account (using the seed)
		mess = self.api.get_account_data(start = 0)
		
		#Decompose the Bundle into components
		bundle = mess.get('bundles')
		Message = []
		for i in bundle:
			message = str(i.get_messages()).strip("[u'").strip("']")
			Message.append(message)
		self.Messages = Message
		try:
			self.LatestMessage = Message[len(bundle)-1]
		except IndexError:
			self.LatestMessage = "No Message"
		return self		

	def Generate_Address(self, Index = 0):
		generate = self.api.get_new_addresses(index = int(Index))
		self.Address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")		
		return self

	def LatestMileStone(self):
		Node = self.api.get_node_info()
		self.MileStone = Node.get("latestMilestoneIndex")
		return self

	def Seed_Generator(self):
		random_trytes = [i for i in map(chr, range(65,91))]
		random_trytes.append('9')
		seed = [random_trytes[SystemRandom().randrange(len(random_trytes))] for x in range(81)]
		self.Seed = ''.join(seed)
		return self

	def AssociatedMessages(self):
		mess = self.api.get_account_data(start = 0)
		print(mess)
		investigate = mess.get('bundles')
		for i in investigate:
			print(i)
			inv = i.as_json_compatible()
			z = i.get_messages()
			x = eval(str(inv))
			a = str(x[0].get('address'))
			combine = [a,z]
			print(combine)



#This block of code is simply the seed which can be generated online (google IOTA Wallet generator)
#The "seed" is the private key and is the most important piece in this code. It allows full access to a wallet. This seed is generated for demonstration and has no form of value.
public = "TEAWYYNAY9BBFR9RH9JGHSSAHYJGVYACUBBNBDJLWAATRYUZCXHCUNIPXOGXI9BBHKSHDFEAJOVZDLUWV"
private = "XDSVGBKJGXAGSIIDEPZQMQHCOPBNQFXMARYGWBRWOSDRIUYQPWCPDGVBEOXNQSMRZMYWUPHTW9TKWVODY"

person1 = "YHHBXG9XUCBUBKZPGZR9RJPZPKGAQM9DHWQOGF9XJWJRESEXDXJJESNQTF9AYS9QVPGXCEXYFDPHWHWQI"
person2 = "TEAWYYNAY9BBFR9RH9JGHSSAHYJGVYACUBBNBDJLWAATRYUZCXHCUNIPXOGXI9BBHKSHDFEAJOVZDLUWV"
person3 = "XDEUWYBDMHAUSRWAY9IIIXSBYXJOSIHOSLMCJZPJVNTVUGTCBBVZJRHACPXT9ZAVOIJHS9AQKNQWPEPWN"
person4 = "YOJMFZAFRSFZ9CRDSZ9YCQUNIAWFIIXXMHRBL9GDTIYRBRIPZGBWFSBPBNOKBPTICNXGIRCENH9WEKOFD"
person5 = "ZXZHKOXMLCLNKYWWWNVTOFBSLFNSXHMXHGB9DCSSZGBRHIG9ATUOQ9JZYBAHAKSYO9DIPJSHVLVACWEUM"


'''
#We get the address of the ledger
ledger = []
for i in range(5):
	PublicAddress = IOTA_Module(Seed = public).Generate_Address(Index = i).Address
	ledger.append(PublicAddress)


for i in range(100):
	number = random.randrange(0, len(ledger),1)
	ad = ledger[number]
	Message1 = str("Hello1 "+str(ad))
	x = IOTA_Module(Seed = private)
	x.Sending(ReceiverAddress = ad, Message = Message1)
	print(i)
'''


IOTA_Module(Seed = public).AssociatedMessages()



#x = api_rec.get_transfers(start = 0, stop = 10)
#y = x.get('Address')

#print(dir(x))
#print(dir(y[0]))

#print()

#print(y[0].hash)
#print(dir(y[0].transactions))
#print(dir(y[0].transactions.__getitem__.__getattribute__))
