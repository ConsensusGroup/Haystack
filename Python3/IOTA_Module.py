#IOTA library
from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.crypto.addresses import AddressGenerator
from iota.adapter import HttpAdapter
from iota import *

#Cryptography library
from random import SystemRandom

#Import other libs
import sys
from Tools_Module import Tools

def Seed_Generator():
    trytes = [i for i in map(chr, range(65,91))]
    trytes.append("9")
    Seed = [trytes[SystemRandom().randrange(len(trytes))] for x in range(81)]
    return "".join(Seed)

class IOTA:
    def __init__(self, Seed, Node, PoW = False):
        self.IOTA_Api = Iota(Node, seed = Seed, local_pow = PoW)

    def Send(self, Receiver_Address, Message):

        Trytes_Convertion = TryteString.from_string(Message)
        TX = ProposedTransaction(address = Address(Receiver_Address), message = Trytes_Convertion, value = 0)
        bundle = ProposedBundle()
        bundle.add_transaction(TX)
        bundle.finalize()
        TX_Hash = str(bundle.hash)
        bundle_as_trytes = bundle.as_tryte_strings()
        TX_Success = False
        try:
            TX_Confirmation = self.IOTA_Api.send_trytes(trytes = bundle_as_trytes, depth = 4)
            TX_Success = TX_Hash
        except:
            if "iota.adapter.BadApiResponse" in str(sys.exc_info()[1]):
                print("Node not in Sync, finding another node....") #< ----------------------------------------------------

            elif "The subtangle has not been updated yet." in str(sys.exc_info()[1]):
                print("Node not synced yet, finding another node...") #< ----------------------------------------------------

            elif "429 response from node"in str(sys.exc_info()[1]):
                print("Too many requests to node, finding an alternative node...") #< ----------------------------------------------------

            elif "[Errno 111] Connection refused" in str(sys.exc_info()[1]):
                print("Connection error, finding an alternative node...") #< ----------------------------------------------------

            elif "403 Forbidden" in str(sys.exc_info()[1]):
                print("No access granted to node, finding an alternative node...") #< ----------------------------------------------------
                # special case; a node accepts with POW set to "True"

            elif "certificate verify failed" in str(sys.exc_info()[1]):
                print("Node does not have a valid SSL certificate, finding an alternative node...")

            else:
                print("Unexpected exception caught in send") #< ----------------------------------------------------
                print(sys.exc_info()[1]) #< ----------------------------------------------------

        return TX_Success

    def Receive(self, Start, Stop):
        Data_From_Node = False
        try:
            Data_From_Node = self.IOTA_Api.get_account_data(start = Start, stop = Stop)
        except:
            if "[Errno 111] Connection refused" in str(sys.exc_info()[1]):
                print("Connection error, finding an alternative node...") #< ----------------------------------------------------

            elif "certificate verify failed" in str(sys.exc_info()[1]):
                print("Node does not have a valid SSL certificate, finding an alternative node...") #< ----------------------------------------------------

            elif "[Errno 61] Connection refused" in str(sys.exc_info()[1]):
                print("Connection error, finding an alternative node...") #< ----------------------------------------------------

            else:
                print("Unexpected exception caught in receive") #< ----------------------------------------------------
                print(sys.exc_info()[1]) #< ----------------------------------------------------

        if Data_From_Node != False:
            Complete_Collection = {}
            for bundles in Data_From_Node["bundles"]:
                    for JSON in bundles.as_json_compatible():
                        temp = {}
                        temp["ReceiverAddress"] = str(JSON.get("address"))
                        temp["Tokens"] = JSON.get("value")
                        temp["Timestamp"] = JSON.get("attachment_timestamp")
                        temp["Message"] = bundles.get_messages()[0]
                        try:
                            temp["Message_Tag"] = TryteString(str(JSON.get("tag"))).decode()
                        except:
                            temp["Message_Tag"] = JSON.get("tag")
                        Complete_Collection[str(JSON.get("bundle_hash"))] = temp
            Data_From_Node = Complete_Collection
        return Data_From_Node

    def Generate_Address(self, Index):
        generate = self.IOTA_Api.get_new_addresses(index = Index)
        Address = str(generate["addresses"][0]).encode()
        return Address

    def TangleTime(self):
        Node_Data = self.IOTA_Api.get_node_info()
        self.Current_Time = Node_Data["time"]
        Output = Tools().Epoch_To_Block(Epoch_Time = float(self.Current_Time))
        self.Block_Remainder = Output[1]
        self.CurrentBlock = Output[0]
        return self
