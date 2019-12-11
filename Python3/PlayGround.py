from IOTA_Module import *
from Tools_Module import *
from iota.multisig.types import MultisigAddress
from iota.multisig import MultisigIota

def Balance_Checker(Address):
    Entries = IOTA.Search_Address(Addresses = [str(Address)])
    if Entries == {}:
        return False
    else:
        IOTA_Tokens = 0
        for i in Entries.keys():
            IOTA_Tokens = IOTA_Tokens + Entries[i].get("Value")
        return IOTA_Tokens





User1 = "QSLZBOTXR99HGCKSUKIEWDOKSAWACQRUSDSVHMMCTKCZVPFFQPBXLQWPBYBCLRTBICBVIL9MZWABUUB9C"
User2 = "IBWBTIYBSZZPIDSQPGYFYCOPENEZOMSDPDUHZVWKVNZSHTAQBJHDXSNJKZHXJDBWAHIOLJFXYYTHZDGWM"
User3 = "QIH9WCYDLMAWIVKEJSANQXUBPT9WXBBPFUYCNFYZUQOBPDZPAMBVZDNGBAYMZSCCYYQPPXLKUWJABZKCK"
User4 = "M9FJIGT9JMNTOMOXJTSTEFTYUPGPRGMKBELZXKGTLPDFSNSFDVLABT9KVYLHNBHKJNMYTYPLJDBLXNFXL"
User5 = "NDBLMRMUDSLZMXEBLVONGR9PNRXNSKPGUBJYXNCLLDAVOICEKSBZLRYXONY9BAKBDGALGMJFOLOGJEPIW"

PayOut = "WZUXIYORFQYUPNHYBM9WTWFHILIQQMUCRZCWVUHOQXPHMIJQJIVIVYNKYZMLNHXQUMSTBDPAUDJZAGMW9"
Relayer = "RKHLHKU9CNSNOT9EVOAUBSHFPFHVQQPALYKCPJIJNGTPKSLPZZWNL9EQVKKEQCRUMDLNMJGFJCSDVFQT9"

Node = "http://localhost:14265"
Index = 3
u1 = Multisignature(Seed = User1, Node = Node, PoW = True)
u2 = Multisignature(Seed = User2, Node = Node, PoW = True)
u3 = Multisignature(Seed = User3, Node = Node, PoW = True)
u4 = Multisignature(Seed = User4, Node = Node, PoW = True)
u5 = Multisignature(Seed = User5, Node = Node, PoW = True)

IOTA = IOTA(Seed = User1, Node = Node, PoW = True)


d1 = u1.Generate_Digest(Index = Index)
d2 = u2.Generate_Digest(Index = Index)
d3 = u3.Generate_Digest(Index = Index)
d4 = u4.Generate_Digest(Index = Index)
d5 = u5.Generate_Digest(Index = Index)

Digests_List = [d1, d2, d3, d4, d5]


#Initial deposit address
print(u1.Generate_Multisignature_Address(Digests_List=[d1, d2], Check_Sum = True))

#Here we generate the multisig address for u1 and u2
Address = u1.Generate_Multisignature_Address(Digests_List=[d1, d2])

#Now check if there is funding in the address
IOTA_Tokens = Balance_Checker(Address = str(Address))
print(IOTA_Tokens)
#
#if IOTA_Tokens >= 0:
Bundle = u1.Generate_Multisignature_Bundle(Receiver = PayOut, Multisignature_Address = Address, Change_Address = Relayer, Value = 1)
print(Bundle)
Bundle = u1.Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Bundle)
Bundle = u2.Sign_Bundle_Input(Index = Index, Bundle_To_Sign = Bundle)
Signed = Validate_Signed_Bundle(Bundle)
print(Signed)
# Signed = Bundle.as_tryte_strings()
# u1.Submit_Bundle(Signed_Trytes = Signed)
#
# #Bundle = IOTA.Import_Bundle(Hash = "9ZIFIBEAIRUJ9UZLIQUVBTKEYRJPALXPGSRT9VVCXDDIUULDBWPEJVHPLXWBIDNSFUGPCEEELPGCYDZUA")
# API1 = MultisigIota(adapter = Node, seed = User1, local_pow = True).get_private_keys(index = Index, count = 1, security_level = 3)["keys"][0]
# API1.sign_input_transactions(Bundle, 1)
#
# API = MultisigIota(adapter = Node, seed = User2, local_pow = True).get_private_keys(index = Index, count = 1, security_level = 3)["keys"][0]
# API.sign_input_transactions(Bundle, 4)
#
# Signed = Bundle.as_tryte_strings()
print(u2.Submit_Bundle(Signed_Trytes = Signed))
