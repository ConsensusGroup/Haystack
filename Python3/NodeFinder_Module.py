from IOTA_Module import IOTA
from Tools_Module import Tools
from Configuration_Module import Configuration
from UserProfile_Module import UserProfile
import config
import time

def Test_Node(node):
    def Speed_Tx(Node, Read_Write, PoW = False):
        start = time.time()
        iota = IOTA(Seed = Configuration().PublicSeed, Node = node, PoW = PoW)

        if Read_Write == "w":
            Address = iota.Generate_Address(Index = 0)
            Confirmation = iota.Send(Receiver_Address = Address, Message = "Test")
        else:
            Confirmation = iota.Receive(Start = 1, Stop = 2)
        stop = time.time()
        if Confirmation == False:
            return "Error"
        else:
            return stop - start

    def Kill():
        if config.RunTime == False:
            exit()

    def Collection(temp, Node_Dictionary, node, PoW, Action, Read_Write):
        Kill()
        temp[Action] = Speed_Tx(Node = node, PoW = PoW, Read_Write = Read_Write)
        Node_Dictionary[node] = temp
        Tools().JSON_Manipulation(File_Directory = x.Node, Dictionary = Node_Dictionary)
        return Node_Dictionary, temp

    x = UserProfile()
    Node_Dictionary = Tools().JSON_Manipulation(File_Directory = x.Node)
    temp ={}

    Output = Collection(temp = temp, Node_Dictionary = Node_Dictionary, node = node, PoW = False, Action = "Send_No_PoW", Read_Write = "w")
    Output = Collection(temp = Output[1], Node_Dictionary = Output[0], node = node, PoW = False, Action = "Send_PoW", Read_Write = "w")
    Output = Collection(temp = Output[1], Node_Dictionary = Output[0], node = node, PoW = False, Action = "Read", Read_Write = "r")


# This code block is created to terminate the background thread using config.RunTime later on!
def Test_Nodes():
    con = Configuration()
    for node in con.Preloaded_Nodes:
        Test_Node(node = node)


def Return_Optimal_Node():
    def Return_Rank(Ranked, Plain):
        Ranking = {}
        z = 1
        for i in Ranked:
            for x in Plain:
                if i == x[0]:
                    if len(x) == 3:
                        temp = {}
                        temp["Node"] = x[2]
                        temp["PoW"] = x[1]
                        Ranking[z] = temp
                    else:
                        temp = {}
                        temp["Node"] = x[1]
                        temp["PoW"] = False
                        Ranking[z] = temp
                    z = z+1
        return Ranking

    Node_Dictionary = Tools().JSON_Manipulation(File_Directory = UserProfile().Node)
    Node_Send = []
    Node_Read = []
    Temp_Send = []
    Temp_Read = []
    for node, measurements in Node_Dictionary.items():
        try:
            PoW = measurements["Send_PoW"]
        except KeyError:
            Pow = "Error"
        try:
            No_PoW = measurements["Send_No_PoW"]
        except KeyError:
            No_PoW = "Error"
        try:
            Read = measurements["Read"]
        except KeyError:
            Read = "Error"

        #Checking Dead Nodes
        if PoW == "Error":
            PoW = 9999
        if No_PoW == "Error":
            No_PoW = 9999
        if Read == "Error":
            Read = 9999

        # PoW vs Non PoW
        if PoW < No_PoW:
            Use_PoW = True
            Comparison = PoW
        elif PoW > No_PoW:
            Use_PoW = False
            Comparison = No_PoW
        else:
            Comparison = 9999
            PoW = False

        if Comparison != 9999:
            Node_Send.append([Comparison, Use_PoW, node])
            Temp_Send.append(Comparison)

        if Read != 9999:
            Node_Read.append([Read, node])
            Temp_Read.append(Read)

    Temp_Send.sort()
    Temp_Read.sort()

    Ranked_Sending = Return_Rank(Temp_Send, Node_Send)
    Ranked_Receiving = Return_Rank(Temp_Read, Node_Read)

    return [Ranked_Sending, Ranked_Receiving]
