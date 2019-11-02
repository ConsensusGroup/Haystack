import a
import b
import c
import d
import e
from iota import TryteString
from a import DynamicPublicLedger_Module
from b import DynamicPublicLedger_Module
from c import DynamicPublicLedger_Module
from d import DynamicPublicLedger_Module
from e import DynamicPublicLedger_Module

Nodes = ["a","b","c","d","e"]
Message = "Successful execution of the Shrapnells function. It is working completely flawlessly! Let us make a longer string so that this method really is tested for some actual conversations about anon communications.Let us ,make this insanely long just for the fun of this experiment. This time I will change the number of relays to four that way this thing is being really stress tested. If this work I will be very happy about the result. So the last time I tried this I found it was a bit buggy so maybe we can increase it even more just to see how the dynamics change. The settings are still at four bounces."

DLP =  [['SXFHMUODKHRTIKCPJKVWCMQSPLIGDNVXTQDFMWDIKTDWBWFZRMHJRJJKMIOGYUIMUQBEMLJQMAVLXTXIB', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4/ADpey96Ge3GlphkpCF\nudKVT5ajzIvqO2ZF74r8bo+O8n/F1IkjltJZVndkMs+PHkjGA4vM12Yd7pwBqGE/\nE1CXEPZoO6fDltYqB2J9jZGKntU8fSQ+r8GaRN18w/RZiN+bc7q+B3wSSgf0jy3u\nKf6G2NO+XEl23ezV690TP1HKQWPUbUJQ4RqytBVflz4/bA7o8EtoWVcgB8g/kEfG\neXm+TNkfU4jlpNHKgqGMBw4HO3be14Ru/jk/3h74fIv8pGEhmcpG16cEGcztWbNx\nqurHyCo1UMl0DrCLLT4eab7TKKibJRdT0aFV2SoO3dcWcfB7mu8rdFudPywjlXWb\n0wIDAQAB\n-----END PUBLIC KEY-----'], ['IGOGCELLB9NMKDZVY9DGNPKIOISPIRSRIOVSWAKIHNVTAMYOGM9IIO9QTDSQKNJBSCTFQFWDQQPFFJH9W', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt8wtd9ht6EQT3icGqgX4\n2P+77Ucu3ijMnB2LEuh2TNfCxo00FJ3Hwq+X0w77JCx8IqkQn7iBfBNke9H7cigq\nfOZ9zjaFHddoYhf0iPasU27hcvjhRWWkfBUN5cwxkPrfyQkXnz1vIr1kBpuBxAH+\nI8jzuCW9JvR0TfR5REHfgMb+/ccN69mYMB3WXHiKuhE7WYUMaCgBf8k+DwN09g2s\nhxAlNSYz86HlXEzgbop7bHsYF2moNNv7lgHZMYoga+1SubCwH79hS2LkdLd8xBDm\nL2LWq+PSPob5z7fyh5pZdtcyDWTSXHmfUqsAy3Ui9TaOu6OMpxC/QD7AXZSMORyd\nNQIDAQAB\n-----END PUBLIC KEY-----'], ['9HJKEOYTSLMMQIWFJ9CKLWXXHXQAWCU99BS99QRINCVJLXSDXKSHHINFWOIBEBWQCJEAUMAMBYW9VLTOB', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkHjW+BhLQ8kuu/2o/qxv\nGFv9zsLQ7osWkH7igY9nS56yM8q6RkAcdBx7pybYxPazlSa0Rppa0pftG2ySgHbI\n8z6k9ExVe7dkeHfiftSZk/nTsdhSpcuWp9xzdEQ65jYA+istiqzJk0zTV1zJFqTe\naUvYG1i8pI7/UbvuDcEM+X5n6bD+pdW9pjxEinx0h7l1apX1gqu5S9Kkvud/4EZ/\n4jKaBb+FBQ/1GZtgL7fLJuiTygoWfeenUwXzs+2SfdRac7h6dLv/qfoU0vprZUfa\n2LftSfu9g164Fwts8/MLrAw8guQCpyA3b6Ax+BHPHW58xPlGdSueHZnwG/7Q1VHa\niwIDAQAB\n-----END PUBLIC KEY-----'], ['HXFXINRHI9L9XWOECMXENSM9FPWQUAAHODTAEUKCBFRNAFFGENXWXXLNDQUYCLKMRXCYDUTJLGB9WHAIW', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4nhhrzizgL1ahKoJYknd\nnoB9LfV261dRfonW5W3xYPijjgbbHoI+NE8Sp9UmehNvUFDANoSzj1uhSDbXfabr\nKoliAGkn3yeocxxLIvNFL3Vd4vMsHGxpm+wdEgKNO8MoWvlGwn/vT+ElBp57qhzo\nD6HXlxcRd22cEFOunYzAEs7U99OT0pKbJjHX+g/FCuBrLLNHAiDK0VvydLFKm34G\nDWyEEIFVp5Vc97pmb15GX+lZeFov14ZnxG6hAAyCCoKZgoCSi0P4WQbwfDa9R4Wq\nRFWX30lGRB9QmrfArGnOFVzuBoeCLNAK4v06mkNxq8jEl91pCHQIbK5wqynAk5ke\nqwIDAQAB\n-----END PUBLIC KEY-----'], ['XXGTJKGUHWNYWNZHOMPJPWYVPDVHPAMZEZALSAJVYAPDSVIOMRNFDGPKUQOQZWXTC9VDS9VGDUGTKSFMY', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAslXUjCGWvLOfV4+cMwy+\nxhmjyBuLFHieteDNT9NR4iUREpeLxs/XoXeimC+umJ6nmKkjFcLBS/m9fEFic7fY\nVU2Kn8O7oyWa0CiKyXbPKS1logAG3khmZ6w/bep1VNHAMuvhL40+fBADWpfoekwy\nQUtJYvcTaXL2fzjtx4d4nGdbogYz/OATXDlOUwK3OjRH2fptJse0lI6lKLCptN18\nVwIg0PY3rKjmzboxKchvJvb8GiqWheGoJ6a9DHjYx5qhtJHDYbWF7bSP2w1XmXHA\nUHTkJRej9UgkEtAkMN6p4HDqkrVvwSRO7ct3CpGN5mFI56QejKcgHUmb7M0yEpd+\nOwIDAQAB\n-----END PUBLIC KEY-----']]

#Starting the user profiles
UserA = a.User_Modules.User_Profile()
UserB = b.User_Modules.User_Profile()
UserC = c.User_Modules.User_Profile()
UserD = d.User_Modules.User_Profile()
UserE = e.User_Modules.User_Profile()

UserA = a.User_Modules.Initialization().InboxGenerator(Output_Directory = False)
UserB = b.User_Modules.Initialization().InboxGenerator(Output_Directory = False)
UserC = c.User_Modules.Initialization().InboxGenerator(Output_Directory = False)
UserE = e.User_Modules.Initialization().InboxGenerator(Output_Directory = False)
UserD = d.User_Modules.Initialization().InboxGenerator(Output_Directory = False)


def Test_Relaying_Client(Nodes, DLP, Message):
	#here we need to create the initial sender.
	Message_To_Send = a.Haystack_Module.Sender_Client().Send_Message(Message = Message, ReceiverAddress = str(DLP[0][0]), PublicKey = str(DLP[0][1]))
	print("Length of the tryte:" + str(len(TryteString.from_string(Message_To_Send[0]))))
	print("Length of the message without tryte:" + str(len(Message_To_Send[0])))
	print(Message_To_Send[0])
	print("Message should be received by: " + Message_To_Send[1])

	Message_To_Send = Message_To_Send[0]
	for i in range(5):
		for j in Nodes:
			DL = eval(j).DynamicPublicLedger_Module.Dynamic_Public_Ledger()
			print("#########################################################################           Current address:"+DL.PrivateIOTA.Generate_Address(Index = DL.Calculate_Block().Block)+"  Client: "+ j)
			Message_To_Send = eval(j).Haystack_Module.Receiver_Client().Message_Decrypter(Cipher = Message_To_Send[0])
			print(Message_To_Send)

def Test_Shrapnelling():
	Message = a.Inbox_Module.Inbox_Manager().Reconstruction_Of_Message(True)[0]
	if Message[0] != False:
		print("Passed!"+ "\n Message From:	 " + str(Message[0]) + "\n Message:	 "+ str(Message[1]))
	elif Message[0] == False:
		print("No New Message for you.")

def Test_Inbox_Manager(Nodes, Message, DLP, Send_Message = False):
	if Send_Message == True:
		Message_To_Send = a.Haystack_Module.Sender_Client().Send_Message(Message = Message, ReceiverAddress = str(DLP[0][0]), PublicKey = str(DLP[0][1]))
		print("Length of the tryte:" + str(len(TryteString.from_string(Message_To_Send[0]))))
		print("Length of the message without tryte:" + str(len(Message_To_Send[0])))
		print("Message should be received by: " + Message_To_Send[1])

	a.Inbox_Module.Inbox_Manager().Create_DB()
	for i in range(5):
		print(i)
		for j in Nodes:
			print("Client: "+j)
			eval(j).Haystack_Module.Receiver_Client().Check_Inbox()
	Test_Shrapnelling()

if __name__ == "__main__":
	#Test_Inbox_Manager(Nodes, Message = Message, DLP = DLP, Send_Message = True)
	#Test_Shrapnelling()





## TODO:
# - Add the ping function and build "Trusted Paths" (Next major milestone)
# - Work on storing entries in the public ledger locally and pruge after XXX blocks
# - Build a message purger i.e. remove incomplete messages after some time
# - Resolve the glitch where setting MaxBounce = 0 causes an error in the b64 padding.
# - Figure out the UI at some later stage
