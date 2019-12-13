from IOTA_Module import *

class Node_Incentive:
    def __init__(self, Seed, Node, PoW = True):
        self.Multi = Multisignature(Seed = Seed, Node = Node, PoW = PoW)
        self.IOTA_Api = IOTA(Seed = Seed, Node = Node, PoW = PoW)

    def Sender_Deposit(self, Digests, Reward_Address, Index, Value, Next_Relayer):
        Client_Digest = self.Multi.Generate_Digest(Index)
        Digests.insert(0, Client_Digest)
        Deposit_Address = self.Multi.Generate_Multisignature_Address(Digests_List = Digests, Check_Sum = False)

        z = 0
        while True:
            Contract = self.Multi.Generate_Multisignature_Bundle(Receiver = Reward_Address, Value = Value, Change_Address = Next_Relayer, Multisignature_Address = Deposit_Address)
            if isinstance(Contract, str) == False:
                if z == 0:
                    pass
                else:
                    print("Payment received!")
                break
            elif z == 0:
                print("Waiting for a deposit. Send IOTA to: "+str(Deposit_Address.with_valid_checksum()))
            z = z+1

        Signed_Contract = self.Multi.Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Contract)
        To_Encrypt_Hash = Signed_Contract.as_json_compatible()[0].get("bundle_hash")
        Contract_Trytes = Signed_Contract.as_tryte_strings()
        self.Multi.Submit_Bundle(Signed_Trytes = Contract_Trytes, Depth = 1)
        return To_Encrypt_Hash

    def Relay_Signature(self, Bundle_Hash, Index, PayOut_Address, Value):
        Bundle_Object = self.Multi.Import_Bundle_Object(Hash = Bundle_Hash)
        Json = Bundle_Object.as_json_compatible()[0]

        #First we check that there is an actual deposit on the address and that the PayOut is in the Tx
        if str(Json.get("address")) == PayOut_Address and int(Json.get("value")) == int(Value):
            Bundle = self.Multi.Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Bundle_Object)
            To_Encrypt_Hash = str(Bundle.as_json_compatible()[0].get("bundle_hash"))
            Bundle_Trytes = Bundle.as_tryte_strings()
            #self.Multi.Submit_Bundle(Signed_Trytes = Bundle_Trytes, Depth = 1)
            return Bundle
        else:
            return False

########################## User Accounts #################################################
User1 = "QSLZBOTXR99HGCKSUKIEWDOKSAWACQRUSDSVHMMCTKCZVPFFQPBXLQWPBYBCLRTBICBVIL9MZWABUUB9C"
User2 = "IBWBTIYBSZZPIDSQPGYFYCOPENEZOMSDPDUHZVWKVNZSHTAQBJHDXSNJKZHXJDBWAHIOLJFXYYTHZDGWM"
User3 = "QIH9WCYDLMAWIVKEJSANQXUBPT9WXBBPFUYCNFYZUQOBPDZPAMBVZDNGBAYMZSCCYYQPPXLKUWJABZKCK"
User4 = "M9FJIGT9JMNTOMOXJTSTEFTYUPGPRGMKBELZXKGTLPDFSNSFDVLABT9KVYLHNBHKJNMYTYPLJDBLXNFXL"
User5 = "NDBLMRMUDSLZMXEBLVONGR9PNRXNSKPGUBJYXNCLLDAVOICEKSBZLRYXONY9BAKBDGALGMJFOLOGJEPIW"

########################## Termination ###################################################
PayOut = "ERBDKCFADSKPIHUSTM9RBHCMOFBNRFFFZSC9UDAGOKEKLXUGBGXVYLOUAPHVUVQFTBEANPCDQATZKTLG9LWTDCDBEZ"

########################## Parameters #####################################################
Node = "http://localhost:14265"
Index = 8
d1 = Multisignature(Seed = User1, Node = Node, PoW = True).Generate_Digest(Index = Index)
d2 = Multisignature(Seed = User2, Node = Node, PoW = True).Generate_Digest(Index = Index)
d3 = Multisignature(Seed = User3, Node = Node, PoW = True).Generate_Digest(Index = Index)
d4 = Multisignature(Seed = User4, Node = Node, PoW = True).Generate_Digest(Index = Index)
d5 = Multisignature(Seed = User5, Node = Node, PoW = True).Generate_Digest(Index = Index)


################################ Need to add to DPL #######################################
Digests_List = [d1, d2, d3, d4, d5]
print(Digests_List)

################################ Clients ##################################################
Node_1 = Node_Incentive(Seed = User1, Node = Node)
Node_2 = Node_Incentive(Seed = User2, Node = Node)
Node_3 = Node_Incentive(Seed = User3, Node = Node)
Node_4 = Node_Incentive(Seed = User4, Node = Node)
Node_5 = Node_Incentive(Seed = User5, Node = Node)


############################### Sender of message #########################################
# Sender = Node_1.Sender_Deposit(Digests = [d2, d3], Reward_Address = PayOut, Index = Index, Value = 1, Next_Relayer = PayOut)
# print(Sender)

Hash = "GXZEGKRYQLDHFRVXREJDLLJGSGRVX9JMPVAEJACAIKXKIYN9HDIUKCBSMLHQFCKQHHI9AKLJEIXYRHIFX"
Object = Multisignature(Seed = User1, Node = Node, PoW = True).Import_Bundle_Object(Hash = Hash)
print(Object.as_json_compatible())


Bundle = Multisignature(Seed = User2, Node = Node, PoW = True).Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Object)
Bundle = Multisignature(Seed = User3, Node = Node, PoW = True).Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Object)

print(Bundle)
Signed = Validate_Signed_Bundle(Bundle)
print(Signed)
# Multisignature(Seed = User1, Node = Node, PoW = True).Submit_Bundle(Signed_Trytes = Signed)

#
#
# Hash = "EFQZBRHAEKKFCXHPOP9GQFAUBWINUEFCYTFSKQHNWRXAZFGIVCDWOKMSGDSHCV9W9ECYNWHCXWLDUQAVC"
#
#
# Bundle = Node_2.Relay_Signature(Bundle_Hash = Hash, Index = Index, PayOut_Address = PayOut, Value = 1)
# print(Bundle)
# Bundle = Multisignature(Seed = User3, Node = Node, PoW = True).Generate_Digest(Index = Index).Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Bundle)
#
# x = Multisignature(Seed = User1, Node = Node, PoW = True).Submit_Bundle(Signed_Trytes = Bundle)
# print(x)
# #Node_3.Relay_Signature(Bundle_Hash = To_Encrypt_Hash, Index = Index, PayOut_Address = PayOut)
