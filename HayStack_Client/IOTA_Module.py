####################################################################################
############# The purpose of the module is to handle IOTA interactions #############
####################################################################################

#IOTA library
from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.crypto.addresses import AddressGenerator
from iota.adapter.wrappers import RoutingWrapper
from iota.adapter import HttpAdapter
from iota import *

#Other libraries
from random import SystemRandom
from Configuration_Module import Configuration
from Tools_Module import Tools
import config

######## Base IOTA classes ########
def Seed_Generator():
	random_trytes = [i for i in map(chr, range(65,91))]
	random_trytes.append('9')
	seed = [random_trytes[SystemRandom().randrange(len(random_trytes))] for x in range(81)]
	return ''.join(seed)


def Return_Fastest_Node():
    x = Configuration()
    Node_Dictionary = Tools().Read_From_Json(directory = x.UserFolder+"/"+x.NodeFolder+"/"+x.NodeFile)
    Send_initial = 999.0
    Receive_initial = 999.0
    Fastest_Combination = {}
    for Node, Stats in Node_Dictionary.items():
        try:
            Send = Stats["Send"]
            Receive = Stats["Receive"]
            float
        except TypeError:
            Send = 999.0
            Receive = 999.0

        if Send_initial > Send:
            Send_initial = Send
            Fastest_Combination["Send"] = Node

        if Receive_initial > Receive:
            Receive_initial = Receive
            Fastest_Combination["Receive"] = Node

    return Fastest_Combination

class IOTA_Module(Configuration):
	def __init__(self, Seed, IOTA_Instance = ""):
		Configuration.__init__(self)

		try:
			Optimal_Node = Return_Fastest_Node()["Send"]
			if Optimal_Node == 999.0:
				Optimal_Node = Return_Fastest_Node()["Receive"]
			config.Node = Optimal_Node
		except:
			config.Node = "http://localhost:14265"

		if config.Node == "http://localhost:14265":
			self.IOTA_Api = Iota(RoutingWrapper(str(config.Node)).add_route('attachToTangle', 'http://localhost:14265'), seed = Seed)
		else:
			self.IOTA_Api = Iota(config.Node, seed = Seed)

		if IOTA_Instance != "":
			self.IOTA_Api = IOTA_Instance
		self.Seed_Copy = Seed

	def Generate_Address(self, Index = 0):
		generate = self.IOTA_Api.get_new_addresses(index = int(Index))
		Address = str(generate.get('addresses')).strip("[Address(").strip(")]").strip("'")
		return Address

	def Send(self, ReceiverAddress, Message, Test_Node = False):

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

		#Return the fastest sender node from the DB if localhost is not present.
		if str(self.Node) != "http://localhost:14265":
			if Test_Node == False:
				self.Node = Return_Fastest_Node()["Send"]
		self.IOTA_Api = Iota(self.Node, seed = self.Seed_Copy)

		send = self.IOTA_Api.send_trytes(trytes = coded, depth = 4)
		return hashed


	def Receive(self, Start = 0, Stop = "", JSON = False, Test_Node = False):

		#Return the fastest sender node from the DB if localhost is not present.
		if self.Node != "http://localhost:14265":
			if Test_Node == False:
				self.Node = Return_Fastest_Node()["Receive"]

			self.IOTA_Api = Iota(self.Node, seed = self.Seed_Copy)

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
				Json = i.as_json_compatible()[0]
				message = [Json,message]
			self.Message.append(message)
		return self

	def LatestTangleTime(self):
		Node = self.IOTA_Api.get_node_info()
		self.TangleTime = Node.get("time")
		return self
