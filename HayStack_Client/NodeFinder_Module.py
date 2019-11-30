from Tools_Module import Tools
from Configuration_Module import Configuration
from IOTA_Module import Return_Fastest_Node, IOTA_Module
import time
import config
from iota import *

class Node_Finder(Configuration):
    def __init__(self):
        Configuration.__init__(self)
        self.RootNode = str(self.UserFolder+"/"+self.NodeFolder)
        self.NodeFile_Dir = str(self.RootNode+"/"+self.NodeFile)

    def Build_Directory(self):
        Tools().Build_Directory(directory = str(self.RootNode))
        Tools().Build_DB(File = self.NodeFile_Dir)

        Node_List = ["http://localhost:14265", "https://mama.iota.family:14267", "http://node05.iotatoken.nl:16265", "https://nodes.iota.cafe:443", "https://we-did-it.org:14265", "https://node.iri.host:443", "https://node.iota-tangle.io:14265", "https://node04.iotatoken.nl:443", "https://node02.iotatoken.nl:443", "https://pool.trytes.eu","https://nutzdoch.einfachiota.de","https://pow.iota.community:443","https://papa.iota.family:14267","https://piota-node.com:443","https://v22018036012963637.bestsrv.de:14267","https://trinity.iota-tangle.io:14265","https://dyn.tangle-nodes.com:443","https://perma.iota.partners:443","https://gewirr.com:14267","https://node01.iotatoken.nl:443","https://node01.iotatoken.nl:443","https://www.iotaqubic.us:443","https://community.tanglebay.org","https://node.deviceproof.org:443","https://nodes.thetangle.org:443","https://wallet1.iota.town:443","https://wallet2.iota.town:443","https://iota.chain.garden:443","https://nodes.thetangle.org:443","https://node.trustingiot.com:443","https://power.benderiota.com:14267","https://www.iotaqubic.us:443","https://stirrlink.dyndns.org:14267","https://iota1.chain.garden:443","https://nod3.theshock.de:443","https://wallet1.iota.town:443","https://node00.gubiota.ch:443","https://node01.gubiota.ch:443","https://node02.gubiota.ch:443","https://iotanow.nl:443"]

        Node_Dictionary = {}
        for i in Node_List:
            Node_Dictionary = Tools().Add_To_Dictionary(Input_Dictionary = Node_Dictionary, Entry_Label = i, Entry_Value = "")

        Tools().Write_To_Json(directory = self.NodeFile_Dir, Dictionary = Node_Dictionary)

        return self

    def Test_Nodes(self):
        try:
            Node_Dictionary = Tools().Read_From_Json(directory = self.NodeFile_Dir)
        except:
            self.Build_Directory()
            Node_Dictionary = Tools().Read_From_Json(directory = self.NodeFile_Dir)

        for Node, Value in Node_Dictionary.items():

            if config.RunTime == False:
                break
        
            config.Node = Node
            IOTA = Iota(Node, self.PublicSeed)
            IOTA_Instance = IOTA_Module(Seed = self.PublicSeed, IOTA_Instance = IOTA)
            Burner_Address = IOTA_Instance.Generate_Address()

            Temp_Dictionary = {}
            try:
                start = time.time()
                Hash = IOTA_Instance.Send(ReceiverAddress = Burner_Address, Message = "Test", Test_Node = True)
                end = time.time()
                delta_Send = end - start
            except:
                delta_Send = "Error"

            Temp_Dictionary["Send"] = delta_Send

            if config.RunTime == False:
                break

            try:
                start = time.time()
                Output = IOTA_Instance.Receive(Start = 1, Test_Node = True)
                end = time.time()
                delta_Receive = end-start
            except:
            	delta_Receive = "Error"
            Temp_Dictionary["Receive"] = delta_Receive

            Node_Dictionary[Node] = Temp_Dictionary
            Tools().Write_To_Json(directory = self.NodeFile_Dir, Dictionary = Node_Dictionary)

            if config.RunTime == False:
                break

        return self
