import a
import b
import c
import d
import e
from time import sleep
import pyffx

Nodes = [a, b, c, d, e]
#First we initialize all the users 
a.User_Modules.User_Profile()
b.User_Modules.User_Profile()
c.User_Modules.User_Profile()
d.User_Modules.User_Profile()
e.User_Modules.User_Profile()

Constants = a.Configuration_Module.Configuration()
ExampleUser = ['E9KNHFCLUIODZAJQSQIDECLQLMJP9PETCDZMRRWWBIURA9ZANLVYCHIELVDKIJKLIYRSGQEHEFULEYAIB', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyCcWZGMN/o3qGNfV3elU\nAgFx73sXqof3OvBhfxDuZK117QPrsVuYyTu2bDcmSu61FHH9DJi/MsloV6UrfN6h\ntH+OFEdvHrmV6IKXQeX/27xsREg/iI1yelEZyUaDcA6pl5xtOtCrJ6AUXcM/xFR6\n4pbD+DxwFBv4uIpmiIqGcm8ORnnLCjrev8mfPcXMIdDOVMr70+Wc4VrSwSGHx11Y\nb0gPPuSFAEAd89b69HbcYXeiObCtRn6hvLmauKtJkZmchXFK9qjyPUrPPg+lMbD6\ndGU56E6dfqmCdGFrvwEiu+78xaNM7x5fXHke6FavsZ1+TX87jg76vRZSyMwVoGzS\newIDAQAB\n-----END PUBLIC KEY-----']
Charlib = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-= '

#Nowwe want to simulate the DPL with user data 
DLP_Simulation = []
for i in Nodes:
	UserEntry = i.Haystack_Module.Dynamic_Public_Ledger().Submit_User().decode("hex").split(Constants.Identifier)[:2]
	DLP_Simulation.append(UserEntry)
	print(str(i))

for i in range(15):
	output = a.Haystack_Module.Relay_Client(Delete_Input = DLP_Simulation).Sender_Function(ReceiverAddress = ExampleUser[0], PublicKey = ExampleUser[1], Message = "Hsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fgHsd d fgsd g dg dfs dfgsd fg")
	print(output)
	print(len(output))

	"{:<1024}".format()