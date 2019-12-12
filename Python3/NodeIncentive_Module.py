from IOTA_Module import *

class Node_Incentive:
    def __init__(self, Seed, Node, PoW = True):
        self.Multi = Multisignature(Seed = Seed, Node = Node, PoW = PoW)
        self.IOTA_Api = IOTA(Seed = Seed, Node = Node, PoW = PoW)

    def Sender_Deposit(self, Digests, Reward_Address, Index, Value, Next_Relayer):
        Client_Digest = self.Multi.Generate_Digest(Index)
        Digests.append(Client_Digest)
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







########################## User Accounts #################################################
User1 = "QSLZBOTXR99HGCKSUKIEWDOKSAWACQRUSDSVHMMCTKCZVPFFQPBXLQWPBYBCLRTBICBVIL9MZWABUUB9C"
User2 = "IBWBTIYBSZZPIDSQPGYFYCOPENEZOMSDPDUHZVWKVNZSHTAQBJHDXSNJKZHXJDBWAHIOLJFXYYTHZDGWM"
User3 = "QIH9WCYDLMAWIVKEJSANQXUBPT9WXBBPFUYCNFYZUQOBPDZPAMBVZDNGBAYMZSCCYYQPPXLKUWJABZKCK"
User4 = "M9FJIGT9JMNTOMOXJTSTEFTYUPGPRGMKBELZXKGTLPDFSNSFDVLABT9KVYLHNBHKJNMYTYPLJDBLXNFXL"
User5 = "NDBLMRMUDSLZMXEBLVONGR9PNRXNSKPGUBJYXNCLLDAVOICEKSBZLRYXONY9BAKBDGALGMJFOLOGJEPIW"

########################## Termination ###################################################
PayOut = "RJFIJAGVQDLJMHTAIFAJYJAWODHBBJEBHKZJMEFPLFBKBGEQYMWDTNJXWISEKDASRFHVOSDZGCCHLZRBZ"

########################## Parameters #####################################################
Node = "http://localhost:14265"
Index = 5
d1 = Multisignature(Seed = User1, Node = Node, PoW = True).Generate_Digest(Index = Index)
d2 = Multisignature(Seed = User2, Node = Node, PoW = True).Generate_Digest(Index = Index)
d3 = Multisignature(Seed = User3, Node = Node, PoW = True).Generate_Digest(Index = Index)
d4 = Multisignature(Seed = User4, Node = Node, PoW = True).Generate_Digest(Index = Index)
d5 = Multisignature(Seed = User5, Node = Node, PoW = True).Generate_Digest(Index = Index)


################################ Need to add to DPL #######################################
Digests_List = [d1, d2, d3, d4, d5]


################################ Clients ##################################################
Node_1 = Node_Incentive(Seed = User1, Node = Node)
Node_2 = Node_Incentive(Seed = User2, Node = Node)
Node_3 = Node_Incentive(Seed = User3, Node = Node)
Node_4 = Node_Incentive(Seed = User4, Node = Node)
Node_5 = Node_Incentive(Seed = User5, Node = Node)


############################### Sender of message #########################################
#Sender = Node_1.Sender_Deposit(Digests = [d2, d3], Reward_Address = PayOut, Index = Index, Value = 1, Next_Relayer = PayOut)
#print(Sender)


Hash = "KEBBBVACAKPDVUZQDOBIRXGSGFG9BGUAJQK9JOQGFWWDXCCOTUYSICANHPFKQBYYJBZZLAG9QQODHNIVB"
Object = Multisignature(Seed = User1, Node = Node, PoW = True).Import_Bundle_Object(Hash = Hash)
print(Object.as_json_compatible())


Bundle = Multisignature(Seed = User2, Node = Node, PoW = True).Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Object)
Bundle = Multisignature(Seed = User3, Node = Node, PoW = True).Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Object)

print(Bundle)
Signed = Validate_Signed_Bundle(Bundle)
print(Signed)
Multisignature(Seed = User1, Node = Node, PoW = True).Submit_Bundle(Signed_Trytes = Signed)
