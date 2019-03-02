import a
import b
import c
import d
import e
from a import DynamicPublicLedger_Module
from b import DynamicPublicLedger_Module
from c import DynamicPublicLedger_Module
from d import DynamicPublicLedger_Module
from e import DynamicPublicLedger_Module

Nodes = ["a","b","c","d","e"]
BlockTime = 15000000
#Starting the user profiles 
UserA = a.User_Modules.User_Profile()
UserB = b.User_Modules.User_Profile()
UserC = c.User_Modules.User_Profile()
UserD = d.User_Modules.User_Profile()
UserE = e.User_Modules.User_Profile()

'''
#Test the DLP 
Started = a.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
print("a")
b.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
print("b")
c.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
print("c")
d.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
print("d")
e.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
print("e")
print(Started.Ledger_Accounts)
'''
DLP = [['LXGAT9RCNCVCICXRGBGVBKXPQJCZD9WPIXBKSRFIEKBH9OS99RZOFAQYIEVVZYGLRNMDELPO9CAQLCJZC', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy03CnC27MH38Mk9sgmkJ\npoQcPgYmKF/dpHRuOB85sC+vW0/Sqy98jpkU/JpUdehau62U+QaOh191cgrpu6uu\nhAvT0EZje+8t5T/vZF914QjMs7gGZiIn7rc0Zo28MF4ajn890ye0JITD8VfObj5N\nUI9HDpFHbCDwuwoBvsK3uFfMjfAKCzSp1rfU+VQs0RA6YOJKFp1YSpB+rPd0FM+l\nmmk5sDyx0u+QS0M8+AbCmCvt0vDKgbojCuDWPYsvprp35T1t/M1sSSjgyf3DetAa\ndYznQ1tbziV2BzFu3timU2fucT7bW1DQwjRTfeBJPjp2bQqololW94N+xB8tCSlj\ncwIDAQAB\n-----END PUBLIC KEY-----'], ['JGAQUQSXBBVTBAGTHZFDZMEAEOPPOMOPFKFOQREMKDEAOTCPMOMIVVHJOATRNUDO9RWLNQTXVUWZMRJQB', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwbvrCp4R5FVfekIRVwvp\n6zxZ98gOqj1OwbgIGypEsTlsCrPcPNH8ljpaa5G8mXCthi1jIaSdxmdCOOQv5/R2\nL673EyQUMC/ffRG3lOMHNauqdSMh2UWiIWUx8BuaC7DVpNRKvrSoQHaGvu1mMdoh\n0AGglc10NsNP6EmwpV3Z+3ZiNBNsyJB+uxH7AQrLcpvlEUmac+kXPCaOZDucFgVp\nXQnT2h1azBAoi9xRtvtZWS+A2ej7hA6c61iDX/VB7z6BAwThhi8RlvDn8V6J0bPA\nGmrCFKRJhrmG0Oj97lO5r/sOwo5unGHdrlXmipXn5b2inXrPrjhkU3eC2vD3OAbx\niQIDAQAB\n-----END PUBLIC KEY-----'], ['KREZVVFIQIFQJVICZHGXVKYABPLOM9JAVKUQPOEQVKDJNJY9AIEL9GXTLXILHN9BXBQJGZSRSHPXQTQ99', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqYNqu6x6ZKBCymvwTTRH\nnLndUefufB1WGnGZ8ohdqNiX1Z58kcRE+nEhSO8R//Uc4KH2jPutuMnVnKHEm2iX\nnyVspm0H9h7jgpldjhzWcRMlOMYHSu5yjxzaQkXUy2XZkmRk7SeDYwfWgw4DL6G5\n1rU6awFjOLB49R+5Bmq3YUC3RMHK71kuMUCeelsr/le+ijl0sXYZTPUT5iFhvgJd\nunQYAe3mnEckYY9d7vI6FILLaLkMkNal20gpkXWkYgYPfYutc6YSQHuJwUlLZasJ\n3dZwC386f9f/5+AgiVz9rUw1THp6fBp+mfhrLNRf/bJ2RfhGg4a1f/FFsJpGAsW+\nOQIDAQAB\n-----END PUBLIC KEY-----'], ['QNDDFQCAW9WJIQSFFIYZFGWKZXVWROQBCYIKKYZALTFCFHEI9NAEJCPEKV9JZCEXXGSQNIDZIZU9PAJTY', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzJLkDj0oe63Anp9U5cmV\nmkqMr0EYkGMvF0dNuAQjbnR/ypv+xs/S4vl5AT2OM9FxfEiGuP3EEutISymAoXFQ\n+QFajASud8VPBnF69GkPEPRjpDDyiEOodnPVINXXYc4upm03/vviZd4t56iRraWM\nl5fRD82iyGkx1WmQ5dicBf9cXaQD8nhWW/nliXF6uM2p24Zcj2zVEhY8wA5Fu4du\nLYMq4pa2SXOM3HvWV1N0ZUU5G7fJo/MW0/GzvtUJ/HIFZ8QpKL2FHthUh2Vv/l9s\nVc9fFjShseD3A4nNxwbJuiwFpFwZmFfmXTMAW+F+cfnH3/ld6OE9B7Xm9b3AdiH5\nrwIDAQAB\n-----END PUBLIC KEY-----'], ['L9SBDPTGSMEBZOJBJUWERD9TLNTKOHOLOAKXSZJHRMJEYLKGAGSVXKRNAWQOLZTDKYZYGMMKGAXCCQRYZ', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6kBA55OGHXwscg3u6HTK\nZoEKqM6G5ZAmknX8zsnN86LoV7PjV25QpHHF2qOx6HUXxvG+sg54yOcjawhlAukC\nyLKZeXEmSpl4HhxQAZ3p/0IxUJe9Fcv/zwFGlY4/rMZ2nxA4rc0LwYbVb9GCa0jA\n1qJp0qrmRxAy6ZLF95249coteOct6V3zjbszAII8gV5+a/bHp968pRbhW5tlQzMj\nwn8UeojZlt7F+sEODScLcFhcGp5WbiPakM8mphvxaZ/znC7+pA9jd5KTvtsSPn3w\nnPeE0RI1rox48yzJwrWqEyJ18mMiIRGCEloY+LvO47ql5tBtcweKJeFZosnZvBP9\nWQIDAQAB\n-----END PUBLIC KEY-----']]
#Test the Sender Function
Message = "Hello"
Output = a.Haystack_Module.Sender_Client(BlockTime = BlockTime).Send_Message(Message = Message, ReceiverAddress = DLP[0][0], PublicKey = DLP[0][1])[0]
print(Output)
#for i in range(4):
#	for x in Nodes:
#		Output = eval(x).Haystack_Module.Receiver_Client(BlockTime = BlockTime).Message_Decrypter(Output)
#		print(x)
#		print("#####################################################################################")
