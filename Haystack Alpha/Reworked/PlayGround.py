import a
import b
import c
import d
import e
from time import sleep
import pyffx
from base64 import b64encode, b64decode


Nodes = [a, b, c, d, e]
#First we initialize all the users 
a.User_Modules.User_Profile()
b.User_Modules.User_Profile()
c.User_Modules.User_Profile()
d.User_Modules.User_Profile()
e.User_Modules.User_Profile()

Constants = a.Configuration_Module.Configuration()
ExampleReceiver = ['E9KNHFCLUIODZAJQSQIDECLQLMJP9PETCDZMRRWWBIURA9ZANLVYCHIELVDKIJKLIYRSGQEHEFULEYAIB', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyCcWZGMN/o3qGNfV3elU\nAgFx73sXqof3OvBhfxDuZK117QPrsVuYyTu2bDcmSu61FHH9DJi/MsloV6UrfN6h\ntH+OFEdvHrmV6IKXQeX/27xsREg/iI1yelEZyUaDcA6pl5xtOtCrJ6AUXcM/xFR6\n4pbD+DxwFBv4uIpmiIqGcm8ORnnLCjrev8mfPcXMIdDOVMr70+Wc4VrSwSGHx11Y\nb0gPPuSFAEAd89b69HbcYXeiObCtRn6hvLmauKtJkZmchXFK9qjyPUrPPg+lMbD6\ndGU56E6dfqmCdGFrvwEiu+78xaNM7x5fXHke6FavsZ1+TX87jg76vRZSyMwVoGzS\newIDAQAB\n-----END PUBLIC KEY-----']

DLP = [['VMEBKOULTVBMDQN9WFYCDCTWMRGJBGBVHCTMMBFBUREMAQMPICQCE9TVHYNVEVCSRQBDXAOWLKMEIUXJD', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm9s8YLJpBvxlrgDWens6\n05V5bOPe4LXm/dLWRBD8p/axYGH6fBUexGKhGsY662FDJYqtWw+uQFFqmbo/3HLF\nceoEJEvUAu2g3FHcDv8Dir63BzsZATgwSlC+iwTZHj/PnrJhhPmzFj8+e/OgQ+Eq\npLY5CtafhZBg2Mg/TKdGRw9eJilmPrEF3i/9XZqnBwlszs8EUOmM2NTrZ/+gargf\nwjbIyzbFcdyPfEugNf1O/rXxaLiNCvC8cxD+NC41OEKEYA3mBT5bYx6J0Clz/any\nrZ/RAGJe4AqHd4A9AF0q54YDw4sg8w0+4FlJzYl7siyOudx2faJ6ie+EqpV9305t\nOQIDAQAB\n-----END PUBLIC KEY-----'], ['HULLPVHPEDEPEHYOKBYNHBZTRDMCRHIHIKBU9DH9MAIMCVVG9HZWZJPHZETLMQSOVURFIFZTRSBCKEIYX', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApxEpt0Sclfw+Z4R+IqMW\nndwu7OyWimrEJLJEphR8SDQBItNx2uSWhXgI6ySwGyh7EztntYCip/SWs0LE5Hth\nIBZPzjQTaY5Bi8AS+YdiJB7oUlzqiIscrJ8eP+bHLkHfy5Jvi/VMboJSxLL6ryLF\nIKhdQBdFG60JZQmCMjtj4AbyrHcocJx/XDxMtC6AItMwf4b3sApR/ViZqd1YLC44\nSdRLF2tgHRBa7Ev2SCAKmU4Fk6RgpGIGfQ8hsdyMYSEOYh3ZCUGGWcfX5przm7Ge\nOjVkH10Aeb6siYBQFE9btoC2hKANXEfT2YQJa5+7Rfd2/8ocrHnlYaeBEtDBes+L\nkQIDAQAB\n-----END PUBLIC KEY-----'], ['JBFPDHNJVSAGUYZNCISGFMXPKMCWAQTOZCXZGGMGYCBUJDQCENNPMAOWICZRELGDRQMJLERAVTUDSLLJC', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsMLSbZi7vyJIT+CjdIRp\n1J2lnVenKAk/Yusk3rh/iHAC65yd90qAUa0szRhOyJ1wjNJdRNj19DuOphcSZXuU\nvF8CoUdRyV0ks4OhELXaC6uUgNcP0l9WydnxYPubIs0swKRDEmxYAanJG5rYrkhW\nVh6W7i1jr9ZRg4AnqA8FPVSw3OzqYR+Hf/CmxVOAmDeOm9dYjZMuz9BkpbdIAfu1\nKOZFjOyKbzygGGMEIHH2UOMSpL8nlzaKFtpX3etqw+mUoE5ml6NrFgaMVEhHaQOA\nKoZ4UcbUqgOP+rOZE4+IujRGcW5OEx/lz+hRJXuzcRHsOJnLZihupN7UkqXfqUQ8\neQIDAQAB\n-----END PUBLIC KEY-----'], ['UVKGXGBN9IHVCLVJCPP9FLDQVRD9MWYYSODHYIBXDSHIQET9T9UDTLTMWVA9HLGFIQJDXDHOYXICNRIK9', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyLHUcr30T4djkyw7AqUw\n12PVR1RWI8caco5g/pgTPdoaXTuviB7oW8fV8s+DFTiGaBnj5u7rwm6t+mgGQHyN\nGbivaGHlHRRjwQEoTMOPidDnNGhsQdGDacbNJd5jEYbwQF7uuEF6Dg2+EO1qwaW+\nAkOu6yzIzNsMiiVayfQSYwXtJuyMCpd63GTDqr4N5faJXemdyP5Sffa/qFE6cWX9\nKU9EtH9RfkHBv5dMCXuS4/L0aDegbxs8jcO1bxwnAf/wok+X+XGU2EDSCzygpfEq\nU3bj9yJP9k1Q34NpByU+GL91rHTZeam4lUyNtJNQtHvx1iPRhMX/Nprnrph2Pay8\n0wIDAQAB\n-----END PUBLIC KEY-----'], ['E9KNHFCLUIODZAJQSQIDECLQLMJP9PETCDZMRRWWBIURA9ZANLVYCHIELVDKIJKLIYRSGQEHEFULEYAIB', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyCcWZGMN/o3qGNfV3elU\nAgFx73sXqof3OvBhfxDuZK117QPrsVuYyTu2bDcmSu61FHH9DJi/MsloV6UrfN6h\ntH+OFEdvHrmV6IKXQeX/27xsREg/iI1yelEZyUaDcA6pl5xtOtCrJ6AUXcM/xFR6\n4pbD+DxwFBv4uIpmiIqGcm8ORnnLCjrev8mfPcXMIdDOVMr70+Wc4VrSwSGHx11Y\nb0gPPuSFAEAd89b69HbcYXeiObCtRn6hvLmauKtJkZmchXFK9qjyPUrPPg+lMbD6\ndGU56E6dfqmCdGFrvwEiu+78xaNM7x5fXHke6FavsZ1+TX87jg76vRZSyMwVoGzS\newIDAQAB\n-----END PUBLIC KEY-----']]
#DLP = [['VMEBKOULTVBMDQN9WFYCDCTWMRGJBGBVHCTMMBFBUREMAQMPICQCE9TVHYNVEVCSRQBDXAOWLKMEIUXJD', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm9s8YLJpBvxlrgDWens6\n05V5bOPe4LXm/dLWRBD8p/axYGH6fBUexGKhGsY662FDJYqtWw+uQFFqmbo/3HLF\nceoEJEvUAu2g3FHcDv8Dir63BzsZATgwSlC+iwTZHj/PnrJhhPmzFj8+e/OgQ+Eq\npLY5CtafhZBg2Mg/TKdGRw9eJilmPrEF3i/9XZqnBwlszs8EUOmM2NTrZ/+gargf\nwjbIyzbFcdyPfEugNf1O/rXxaLiNCvC8cxD+NC41OEKEYA3mBT5bYx6J0Clz/any\nrZ/RAGJe4AqHd4A9AF0q54YDw4sg8w0+4FlJzYl7siyOudx2faJ6ie+EqpV9305t\nOQIDAQAB\n-----END PUBLIC KEY-----'], ['HULLPVHPEDEPEHYOKBYNHBZTRDMCRHIHIKBU9DH9MAIMCVVG9HZWZJPHZETLMQSOVURFIFZTRSBCKEIYX', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApxEpt0Sclfw+Z4R+IqMW\nndwu7OyWimrEJLJEphR8SDQBItNx2uSWhXgI6ySwGyh7EztntYCip/SWs0LE5Hth\nIBZPzjQTaY5Bi8AS+YdiJB7oUlzqiIscrJ8eP+bHLkHfy5Jvi/VMboJSxLL6ryLF\nIKhdQBdFG60JZQmCMjtj4AbyrHcocJx/XDxMtC6AItMwf4b3sApR/ViZqd1YLC44\nSdRLF2tgHRBa7Ev2SCAKmU4Fk6RgpGIGfQ8hsdyMYSEOYh3ZCUGGWcfX5przm7Ge\nOjVkH10Aeb6siYBQFE9btoC2hKANXEfT2YQJa5+7Rfd2/8ocrHnlYaeBEtDBes+L\nkQIDAQAB\n-----END PUBLIC KEY-----']]
#Nowwe want to simulate the DPL with user data 
#DLP_Simulation = [] #[["A1","P1"],["A2","P2"],["A3","P3"],["A4","P4"],["A5","P5"],["A6","P6"],["A7","P7"],["A8","P8"],["A9","P9"]]
#for i in Nodes:
#	UserEntry = i.Haystack_Module.Dynamic_Public_Ledger().Submit_User().decode("hex").split(Constants.Identifier)[:2]
#	DLP_Simulation.append(UserEntry)
	

PrivA = a.User_Modules.User_Profile()
PrivB = b.User_Modules.User_Profile()
PrivC = c.User_Modules.User_Profile()
PrivD = d.User_Modules.User_Profile()
PrivE = e.User_Modules.User_Profile()


PersonA = a.Haystack_Module.Messaging_Client(Delete_Input = DLP)
Output = PersonA.Sending_Message(Message_PlainText = str("l"*220), ReceiverAddress = DLP[2][0], PublicKey = DLP[2][1])
print(Output)

'''
print("################################################################################################")
PersonA = a.Haystack_Module.Messaging_Client(Delete_Input = DLP)
Output = PersonA.Receiving_Message(CipherText = Output)
print(Output.MessageShrapnells)

print("################################################################################################")
PersonB = b.Haystack_Module.Messaging_Client(Delete_Input = DLP)
Output = PersonB.Receiving_Message(CipherText = Output.ToRelay[0][1])
print(Output.MessageShrapnells)

print("################################################################################################")
PersonC = c.Haystack_Module.Messaging_Client(Delete_Input = DLP)
Output = PersonC.Receiving_Message(CipherText = Output.ToRelay[0][1])
print(Output.MessageShrapnells)

print("################################################################################################")
PersonD = d.Haystack_Module.Messaging_Client(Delete_Input = DLP)
Output = PersonD.Receiving_Message(CipherText = Output.ToRelay[0][1])
print(Output.MessageShrapnells)

print("################################################################################################")
PersonE = e.Haystack_Module.Messaging_Client(Delete_Input = DLP)
Output = PersonE.Receiving_Message(CipherText = Output.ToRelay[0][1])
print(Output.MessageShrapnells)
'''






#PersonBE = b.Cryptography_Module.Encryption().AsymmetricEncryption(PlainText = "HelloWorld", PublicKey = DLP[1][1])
#PersonCE = c.Cryptography_Module.Encryption().AsymmetricEncryption(PlainText = "HelloWorld", PublicKey = DLP[2][1])
#PersonDE = d.Cryptography_Module.Encryption().AsymmetricEncryption(PlainText = "HelloWorld", PublicKey = DLP[3][1])
#PersonEE = e.Cryptography_Module.Encryption().AsymmetricEncryption(PlainText = "HelloWorld", PublicKey = DLP[4][1])






#PersonAD = a.Cryptography_Module.Decryption().AsymmetricDecryption(CipherText = output, PrivateKey = a.User_Modules.User_Profile().PrivateKey)
#PersonBD = b.Cryptography_Module.Decryption().AsymmetricDecryption(CipherText = output, PrivateKey = b.User_Modules.User_Profile().PrivateKey)
#PersonCD = c.Cryptography_Module.Decryption().AsymmetricDecryption(CipherText = output, PrivateKey = c.User_Modules.User_Profile().PrivateKey)
#PersonDD = d.Cryptography_Module.Decryption().AsymmetricDecryption(CipherText = output, PrivateKey = d.User_Modules.User_Profile().PrivateKey)
#PersonED = e.Cryptography_Module.Decryption().AsymmetricDecryption(CipherText = output, PrivateKey = e.User_Modules.User_Profile().PrivateKey)
