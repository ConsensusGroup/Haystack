from Haystack_Module import *
from time import sleep


Start_DLP = Dynamic_Public_Ledger()
Start_MessagingClient = Messaging_Client()

for i in range(20):
	Start_DLP.Start_Ledger()
	#print(Start_DLP.Ledger_Accounts)
	Start_MessagingClient.Check_Inbox()
	sleep(4)
	print(i)


