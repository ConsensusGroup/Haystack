####################################################################################
############# The purpose of the module is to handle IOTA interactions #############
####################################################################################

#IOTA library
from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle 
from iota.crypto.addresses import AddressGenerator
from iota.adapter.wrappers import RoutingWrapper
from iota import *

#Other libraries
from random import SystemRandom
from Configuration_Module import Configuration

######## Base IOTA classes ########
def Seed_Generator():
	random_trytes = [i for i in map(chr, range(65,91))]
	random_trytes.append('9')
	seed = [random_trytes[SystemRandom().randrange(len(random_trytes))] for x in range(81)]
	return ''.join(seed)

class IOTA_Module(Configuration):
	def __init__(self, Seed):
		Configuration.__init__(self)
		self.IOTA_Api = Iota(RoutingWrapper(str(self.Node)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed) 

	def Generate_Address(self, Index = 0):
		generate = self.IOTA_Api.get_new_addresses(index = int(Index))
		Address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")
		return Address

	def Send(self, ReceiverAddress, Message):
		
		def Bundle_Generation(Recepient, ToSend):
			text_transfer = TryteString.from_string(str(ToSend))
			txn_2 = ProposedTransaction(address = Address(Recepient), message = text_transfer, value = 0)
			bundle.add_transaction(txn_2)

		bundle = ProposedBundle()
		if type(ReceiverAddress) == list and type(Message) == list and (len(ReceiverAddress) == len(Message)):	
			for i in range(len(ReceiverAddress)):
				Bundle_Generation(ReceiverAddress[i], Message[i])
		elif type(ReceiverAddress) == str and type(Message) == str:
			Bundle_Generation(ReceiverAddress, Message)

		bundle.finalize()		
		coded = bundle.as_tryte_strings()
		hashed = bundle.hash
		send = self.IOTA_Api.send_trytes(trytes = coded, depth = 4)
		return hashed
			
	
	def Receive(self, Start = 0, Stop = "", JSON = False):
		#This chunck of code is used to choose a segment of Tx history to be retrieved 
		if Stop == "":
			mess = self.IOTA_Api.get_account_data(start = Start)
		else:
			mess = self.IOTA_Api.get_account_data(start = Start, stop = Stop)

		#Decompose the Bundle into components
		bundle = mess.get('bundles')
		Message = []
		self.Message = []
		for i in bundle:
			message = str(i.get_messages()).strip("[u'").strip("']")
			if JSON == True:
				Json = str(i.as_json_compatible()[0])
				message = [Json,message]
			self.Message.append(message)
		return self

	def LatestTangleTime(self):
		Node = self.IOTA_Api.get_node_info()
		self.TangleTime = Node.get("time")
		return self

