####################################################################################
############## This module is used to handle the inbox of the client ###############
####################################################################################

from User_Modules import Initialization
from Tools_Module import Tools
from Configuration_Module import Configuration

class Inbox_Manager(Initialization, Tools):
    def __init__(self):
        Initialization.__init__(self)
        Tools.__init__(self)
        self.Received_Dir = str(self.InboxGenerator(Output_Directory = True).ReceivedMessages+"/"+Configuration().ReceivedMessages+".txt")
        self.Relayed_Dir = str(self.InboxGenerator(Output_Directory = True).RelayedMessages+"/"+Configuration().RelayedMessage+".txt")
        self.NotRelayed_Dir = str(self.InboxGenerator(Output_Directory = True).OutstandingRelay+"/"+Configuration().NotRelayedMessage+".txt")

    def Create_DB(self):
        def Build_DB(File):
            Empty_Dictionary = {}
            if self.Check_File(File = File) == False:
                self.Write_To_Json(directory = File, Dictionary = Empty_Dictionary, setting = "w+")

        #Here we check if the DB files are already written.
        Build_DB(File = self.Received_Dir)
        Build_DB(File = self.Relayed_Dir)
        Build_DB(File = self.NotRelayed_Dir)
        return self

    def Read_Tangle(self, IOTA_Instance, Block):
        RelayedMessages_Dictionary = self.Read_From_Json(directory = self.Relayed_Dir)
        NotRelayed_Dictionary = self.Read_From_Json(directory = self.NotRelayed_Dir)

        for i in IOTA_Instance.Receive(Start = Block - 3, Stop = Block + 1, JSON = True).Message:
            Bundle_Hash = str(i[0].get('bundle_hash'))
            Message_Received = i[1][1:len(i[1])-1]
            if self.Label_In_Dictionary(Input_Dictionary = RelayedMessages_Dictionary, Label = Bundle_Hash) == False:
                if self.Label_In_Dictionary(Input_Dictionary = NotRelayed_Dictionary, Label = Bundle_Hash) == False:
                    NotRelayed_Dictionary = self.Add_To_Dictionary(Input_Dictionary = NotRelayed_Dictionary, Entry_Label = Bundle_Hash, Entry_Value = Message_Received)

        #Now we write the dictionary to file.
        self.Write_To_Json(directory = self.NotRelayed_Dir, Dictionary = NotRelayed_Dictionary)
        return self

    def Postprocessing_Packet(self, ToSend, Hash_Of_Incoming_Tx, IOTA_Instance):
        Next_Address = ToSend[1]
        Cipher = ToSend[0]
        Relayed_Dictionary = self.Read_From_Json(directory = self.Relayed_Dir)
        NotRelayed_Dictionary = self.Read_From_Json(directory = self.NotRelayed_Dir)
        if Next_Address != '0'*81:
            Relayed_Bundle_Hash = str(IOTA_Instance.Send(ReceiverAddress = Next_Address, Message = Cipher))
            print("Bundle Hash: " + Relayed_Bundle_Hash)
            Relayed_Dictionary = self.Add_To_Dictionary(Input_Dictionary = Relayed_Dictionary, Entry_Label = Hash_Of_Incoming_Tx, Entry_Value = str(Relayed_Bundle_Hash))
            NotRelayed_Dictionary = self.Remove_From_Dictionary(Input_Dictionary = NotRelayed_Dictionary, Label = Hash_Of_Incoming_Tx)
        elif Next_Address == '0'*81:
            print("Zero:" + Cipher)
            Relayed_Dictionary = self.Add_To_Dictionary(Input_Dictionary = Relayed_Dictionary, Entry_Label = Hash_Of_Incoming_Tx, Entry_Value = str('0'*81))
            NotRelayed_Dictionary = self.Remove_From_Dictionary(Input_Dictionary = NotRelayed_Dictionary, Label = Hash_Of_Incoming_Tx)

        self.Write_To_Json(directory = self.Relayed_Dir, Dictionary = Relayed_Dictionary)
        self.Write_To_Json(directory = self.NotRelayed_Dir, Dictionary = NotRelayed_Dictionary)
        return self

    def Addressed_To_Client(self, Message_PlainText, BundleHash):
        Client_Dictionary = self.Read_From_Json(directory = self.Received_Dir)
        self.Add_To_Dictionary(Input_Dictionary = Client_Dictionary, Entry_Label = Message_PlainText, Entry_Value = BundleHash)
        print("Message: "+Message_PlainText)
        return self
