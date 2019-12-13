from Tools_Module import *
from Configuration_Module import *
from NodeFinder_Module import *
from UserProfile_Module import UserProfile
from Cryptography_Module import *
from IOTA_Module import IOTA
import random
import config

class Sending_Message:
    def __init__(self, Password):
        self.User = UserProfile()
        self.Keys = UserProfile().Get_Keys(Password = Password)

    def Trajectory(self, Bounces, Receiver_Address = "", Public_Key = ""):
        if isinstance(Receiver_Address, bytes) == True:
            Receiver_Address = Receiver_Address.decode("utf-8")
        if isinstance(Public_Key, bytes) == True:
            Public_Key = Public_Key.decode("utf-8")

        Output_List = []
        LedgerAccounts = Tools().JSON_Manipulation(File_Directory = self.User.LedgerAccounts)
        Current_Block = Verify_Node(Dictionary = Return_Optimal_Node()[0], Seed = Configuration().PublicSeed)[1].CurrentBlock

        try:
            Current_Ledger_Pool = LedgerAccounts[str(Current_Block)]
        except KeyError:
            pass

        if Receiver_Address != "" or Public_Key != "":
            Member = []
            Output_List = []
            Ledger_List = []
            for Block_Pool in LedgerAccounts.values():
                for PublicKey in Block_Pool:
                    Address = Block_Pool[PublicKey][0]
                    if Receiver_Address == Address:
                        Found = PublicKey
                    elif Public_Key == PublicKey:
                        Member = [Address, PublicKey]
                    if Found == PublicKey:
                        Member = [Block_Pool[Found][0], Found]
            if Member != []:
                Output_List.append(Member)
                Bounces = Bounces -1

        for Public in Current_Ledger_Pool.keys():
            Ledger_List.append([Current_Ledger_Pool[Public][0], Public])

        for i in range(Bounces):
            Choice = random.choice(Ledger_List)
            Output_List.append(Choice)
        random.shuffle(Output_List)

        return Output_List, Member

    def Onionizing(self, Bounces, Message, Receiver_Address = "", Public_Key = ""):
        if Receiver_Address == Public_Key == "":
            print("Ping") #<----- Figure out the ping function
        else:
            Return = self.Trajectory(Bounces = Bounces, Receiver_Address = Receiver_Address, Public_Key = Public_Key)
            Trajectory_List = Return[0]
            Receiver_Address = Return[1][0]
            Public_Key = Return[1][1]

        Destination = list(Trajectory_List)
        for i in Trajectory_List:
            Address = i[0]
            PublicKey = i[1]
            Destination.remove([Address, PublicKey])
            if Address == Receiver_Address:
                print(Address)
                break
            else:
                print(Address)

        print("#####")
        Receiver = Trajectory_List[0][0]
        if len(Destination) > 0:
            Destination.append([b"0"*81, Destination[len(Destination)-1][1]])
            Destination.reverse()
            for i in Destination:
                print(i)
            Layering_Encryption().Cipher_Generator(Bounces = Bounces, Destination = Destination)
        else:
            print(344)
        print(Receiver)

        print("#####################")











        #print(len(x))
        #x = Encryption().Symmetric_Encryption(PlainText = x, SecretKey = 'lol')



if __name__ == "__main__":
    Public_Key = UserProfile().Get_Keys(Password = config.Password).PublicKey
    PublicKey = Encoding().To_Base64(Input = Public_Key)
    Address = "KZUPYRJRT9ZXXRMZLPMVJNVMALZIQLTISEEXKVIBVODAYSZVQGKUHEYPEOBLLZOPN9MSHBQGNQDKBKDHW"
    Public = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUE5bnlqU2tQbGJzK2t6WE5xM2phRwo4Q0U1dVovV2tXajMwNVFTYUNuaHFDTk9uVmVlRGxhMDJRL2ZtMm9CRzVIb3FTN2lXQzFkRStZWEtocEgzTHM3CnVVaFZ6a3BkZ3RhaENiUUx2MWpHQnhHeVhNcE5uUzVSZzhoRDQwSnFBNTBQeEgwTjlodEkrVnVMcTRpaG9wQjgKclZlbHFmTDg1cW1rY2tGdXBlWE9sVkpkQzQrRnArSzBHZEJETFhQNmxPYVd0bG1vWTU3TWlmRUk1TEZNUmFpbwp3MWJrU0hLMFN2Yk9OK0U2NkwyTVd4TnFtYkFsVm1zOW5lSkJEZWpaeHQyTzJYY0t2TjJMT3I5dzNBdzVYWjcvCkpUMExtRzYzVTFRZksvZFZjYXd1WDJOVlNKM1VtNkRURVZCN01XZnBUWDloTEJ3RHlGaW9IVkpnVHZWakZMR3UKWFFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t"
    Ledger_Dic = Sending_Message(Password = config.Password).Onionizing(Message = "l"*214, Receiver_Address = Address, Public_Key = PublicKey, Bounces = 4)
