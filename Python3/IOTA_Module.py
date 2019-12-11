#IOTA library
from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle, BundleValidator, Tag, TransactionTrytes, Transaction
from iota.crypto.addresses import AddressGenerator
from iota.crypto.types import Digest, PrivateKey
from iota.multisig import MultisigIota
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
        if isinstance(Message, bytes):
            Message = Message.decode()
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

    def Search_Address(self, Addresses):
        Output = self.IOTA_Api.find_transaction_objects(addresses = Addresses).get('transactions')
        Results = {}
        for Tx in Output:
            Temp = {}
            Tx_as_Json = Tx.as_json_compatible()
            Temp["Signature"] = str(Tx_as_Json.get("signature_message_fragment"))
            Temp["Address"] = str(Tx_as_Json.get("address"))
            Temp["Value"] = int(Tx_as_Json.get("value"))
            Results[str(Tx_as_Json.get("hash_"))] = Temp
        return Results

    def Import_Bundle(self, Hash):
        Output = self.IOTA_Api.get_bundles(Hash).get("bundles")[0]
        return Output

    def TangleTime(self):
        Node_Data = self.IOTA_Api.get_node_info()
        self.Current_Time = Node_Data["time"]
        Output = Tools().Epoch_To_Block(Epoch_Time = float(self.Current_Time))
        self.Block_Remainder = Output[1]
        self.CurrentBlock = Output[0]
        return self

class Multisignature:
    def __init__(self, Seed, Node, PoW = False):
        self.IOTA_Api = MultisigIota(adapter = Node, seed = Seed, local_pow = PoW)

    def Generate_Digest(self, Index, Security = 3):
        get_digest = self.IOTA_Api.get_digests(index = Index, count = 1, security_level = Security)['digests'][0]
        return str(get_digest)

    def Generate_Multisignature_Address(self, Digests_List, Check_Sum = False):
        if isinstance(Digests_List, list) == True:
            Multisignature_Address = self.IOTA_Api.create_multisig_address(digests=Digests_List)["address"]
            if Check_Sum == True:
                Multisignature_Address = Multisignature_Address.with_valid_checksum()
        else:
            Multisig_Address = False
        return Multisignature_Address

    def Generate_Multisignature_Bundle(self, Receiver, Multisignature_Address, Value, As_Bundle_Object = True, Change_Address = None, Message = False, Tag_Entry = False):
        if len(Multisignature_Address) != 81:
            return "Remove IOTA address checksum!"
        elif str(type(Multisignature_Address)) != "<class 'iota.multisig.types.MultisigAddress'>":
            return "Incorrect data type! MultisigAddress is needed."
        else:
            if len(Receiver) == 90:
                Receiver = Receiver[:81]
            if Message == Tag_Entry == False:
                Populated = ProposedTransaction(address = Address(Receiver),value=Value)
            elif Message != False:
                Populated = ProposedTransaction(address = Address(Receiver),value=Value, message = TryteString.from_string(Message))
            elif Tag_Entry != False:
                Populated = ProposedTransaction(address = Address(Receiver),value=Value, tag = Tag_Entry.upper())
            elif Tag_Entry != Message != False:
                Populated = ProposedTransaction(address = Address(Receiver),value=Value, message = TryteString.from_string(Message), tag = Tag_Entry.upper())
            try:
                prepared_trytes = self.IOTA_Api.prepare_multisig_transfer(transfers=[Populated], multisig_input = Multisignature_Address, change_address = Change_Address)['trytes']
                if As_Bundle_Object == True:
                    prepared_trytes = Bundle.from_tryte_strings(prepared_trytes)
            except ValueError:
                if "Insufficient balance" in str(sys.exc_info()[1]):
                    return "Insufficient funds in address"
                else:
                    return "You have to provide a change address! Not all IOTA tokens are sent to recipient."
        return prepared_trytes

    def Sign_Bundle_Input(self, Index , Bundle_To_Sign, Count = 1, Security = 3):
        Private = self.IOTA_Api.get_private_keys(index = Index, count = Count, security_level = Security)["keys"][0]
        if isinstance(Bundle_To_Sign, list) == True:
            Bundle_To_Sign = Bundle.from_tryte_strings(Bundle_To_Sign)
        if "iota.transaction.base.Bundle" in str(type(Bundle_To_Sign)):
            Initial_Position = 1
            for i in range(len(Bundle_To_Sign)):
                try:
                    Private.sign_input_transactions(Bundle_To_Sign, Initial_Position)
                    break
                except ValueError:
                    Initial_Position = Initial_Position +1
        return Bundle_To_Sign

    def Submit_Bundle(self, Signed_Trytes, Depth = 3):
        return self.IOTA_Api.send_trytes(trytes = Signed_Trytes, depth = Depth)

def Validate_Signed_Bundle(Signed_Bundle):
    Valid = BundleValidator(Signed_Bundle)
    if not Valid.is_valid():
        return False
    else:
        return Signed_Bundle.as_tryte_strings()
