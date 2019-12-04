#This script is going to be used API calls but first it will serve as a testing script.

from IOTA_Module import *
from Configuration_Module import *
from Tools_Module import *
from UserProfile_Module import *
from Cryptography_Module import *
from NodeFinder_Module import *
import config

class HayStack:
    def __init__(self):
        pass

    def Seed_Generator(self):
        Output = Seed_Generator()
        #Output: A 81 character seed for IOTA
        return Output

    def Write_File(self, File_Directory, Data, Setting = "w"):
        Output = Tools().Write_File(File_Directory, Data, Setting)
        #Output: True if file was written, False if failed
        return None

    def Delete_File(self, File_Directory):
        Output = Tools().File_Manipulation(File_Directory, Setting = "d")
        #Output: True if file deleted, False if failed to delete file
        return Output

    def Read_File(self, File_Directory):
        Output = Tools().Read_File(File_Directory)
        #Output: False if file not found/read, Else contents get returned
        return Output

    def Initialization(self):
        Output = Initialization()
        #Output: None
        return None

    def Asymmetric_KeyGen(self, Password):
        Output = Key_Generation().Asymmetric_KeyGen(Password)
        #Output: Private key as bytes
        return Output

    def Import_PrivateKey(self, PrivateKey, Password):
        Output = Key_Generation().Import_PrivateKey(PrivateKey, Password)
        #Output Objects: PrivateKey, PublicKey
        return Output

    def JSON_Manipulation(self, File_Directory, **kwargs):
        Output = Tools().JSON_Manipulation(File_Directory, **kwargs)
        #Optional Input: Dictionary
        #Output: Write to file -> True, Error(FileNotFoundError) -> False, Read from file = Dictionary
        return Output

    def UserProfile_Keys(self, Password):
        Output = UserProfile().Get_Keys(Password)
        #Output: Output.PrivateKey (bytes), Output.PrivateSeed [Decrypted = bytes, Failed Decryption = False], Output.PublicKey
        return Output

    def IOTA_Generate_Address(self, Seed, Node, Index):
        Output = IOTA(Seed = Seed, Node = Node).Generate_Address(Index = Index)
        #Output: 81 tryte address in 'bytes'
        return Output

    def IOTA_Send(self, Seed, Node, PoW, Receiver_Address, Message):
        Output = IOTA(Seed = Seed, Node = Node, PoW = PoW).Send(Receiver_Address = Receiver_Address, Message = Message)
        #Output: TX_Hash (81 tryte Tx hash, otherwise False [Bool])
        return Output

    def IOTA_Receive(self, Seed, Node, Start, Stop):
        Output = IOTA(Seed = Seed, Node = Node).Receive(Start = Start, Stop = Stop)
        #Output: Dictionary {"BundleHash":{"ReceiverAddress", "Tokens", "Timestamp", "Index", "Message", "Message_Tag"}}, else False [Bool]
        return Output

    def Test_IOTA_Nodes(self):
        Output = Test_Nodes()
        # Output: Nothing
        return None

    def Fastest_Node(self):
        Output = Return_Optimal_Node()
        # Output: [Fastest_Sending: {"Node", "PoW"}, Fastest_Receiving: {"Node", "PoW"}]
        return Output

    def Tangle_Block(self, Seed, Node):
        Output = IOTA(Seed = Seed, Node = Node).TangleTime()
        #Output: Output.Current_Time (time in ms)[int], Output.Block_Remainder (fraction of block left)[float], Output.CurrentBlock (Current block)[int]
        return self

if __name__ == "__main__":
    x = HayStack()
    c = Configuration()

    #Change this to test module
    Function = "Test_IOTA_Nodes"

    if Function == "Fastest_Node":
        print(x.Fastest_Node())

    if Function == "Tangle_Block":
        Seed = c.PublicSeed
        Node = c.Preloaded_Nodes[0]
        x.Tangle_Block(Seed = Seed, Node = Node)

    if Function == "Test_IOTA_Nodes":
        x.Test_IOTA_Nodes()

    if Function == "Seed_Generator":
        print(x.Seed_Generator())

    if Function == "Write_File":
        x.Write_File(File_Directory = c.User_Folder+"/"+c.Keys_Folder+"/"+c.PrivateKey_File, Data = "Hello")

    if Function == "Delete_File":
        x.Delete_File(File_Directory = c.User_Folder+"/"+c.Keys_Folder+"/"+c.PrivateKey_File)

    if Function == "Read_File":
        print(x.Read_File(File_Directory = c.User_Folder+"/"+c.Keys_Folder+"/"+c.PrivateKey_File))

    if Function == "Initialization":
        x.Initialization()

    if Function == "Asymmetric_KeyGen":
        print(x.Asymmetric_KeyGen(Password = ""))

    if Function == "JSON_Manipulation":
        x.JSON_Manipulation(File_Directory = c.User_Folder+"/"+c.Keys_Folder+"/"+c.PrivateKey_File, Dictionary = {})

    if Function == "UserProfile_Keys":
        print(x.UserProfile_Keys(Password = config.Password).PrivateSeed)

    if Function == "IOTA_Generate_Address":
        Seed = c.PublicSeed
        Node = c.Preloaded_Nodes[0]
        print(x.IOTA_Generate_Address(Seed = Seed, Node = Node, Index = 0))

    if Function == "IOTA_Send":
        Seed = c.PublicSeed
        Node = c.Preloaded_Nodes[1]
        Test_Message = "Test"
        Address = x.IOTA_Generate_Address(Seed = Seed, Node = Node)
        print(x.IOTA_Send(Seed = Seed, Node = Node, PoW = True, Receiver_Address = Address, Message = Test_Message).TX_Hash)

    if Function == "IOTA_Receive":
        Seed = c.PublicSeed
        Node = c.Preloaded_Nodes[0]
        print(x.IOTA_Receive(Seed = Seed, Node = Node, Start = 1, Stop = 2))
