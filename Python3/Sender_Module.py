from Tools_Module import *
from UserProfile_Module import UserProfile
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
        Ledger_Dic = Tools().JSON_Manipulation(File_Directory = self.User.CurrentLedger)
        All_Ledger_Dic = Tools().JSON_Manipulation(File_Directory = self.User.LedgerAccounts)

        if Receiver_Address != "" and Public_Key != "":
            Output_List.append([Receiver_Address, Public_Key])
        elif Receiver_Address != "":
            if Receiver_Address in Ledger_Dic:
                Output = Dictionary_Manipulation().Search_Dictionary(Dictionary = Ledger_Dic, Search_Term = Receiver_Address, Action = "Return_Key")
                Output_List.append([Output[1], Output[0]])
            else:
                Output = Dictionary_Manipulation().Search_Dictionary(Dictionary = All_Ledger_Dic, Search_Term = Receiver_Address, Action = "Sort")
                if Output != False:
                    Output_List.append([Output[0][0][0], Output[1]])
                else:
                    Output_List = False

        elif Public_Key != "":
            if Public_Key in Ledger_Dic:
               Address = Ledger_Dic[Public_Key]
               Output_List.append([Address, Public_Key])

            elif Public_Key in All_Ledger_Dic:
                Output = sorted(All_Ledger_Dic[Public_Key].items(), key = lambda x: x[1], reverse = True)[0][0]
                Output_List.append([Output, Public_Key])
            else:
                Output_List = False

        else:
            Bounces = Bounces +1

        try:
            for i in range(Bounces):
                Public_Key = random.choice(list(Ledger_Dic))
                Output_List.append([Ledger_Dic[Public_Key], Public_Key])
            random.shuffle(Output_List)
        except AttributeError:
            Output_List = False

        return Output_List

    def Onionizing(self, Bounces, Message, Receiver_Address = "", Public_Key = ""):
        if Receiver_Address == Public_Key == "":
            print("Ping")
        else:
            Trajectory_List = self.Trajectory(Bounces = Bounces, Receiver_Address = Receiver_Address, Public_Key = Public_Key)

        #Continue here with writing the layering encryption part....








if __name__ == "__main__":
    Public_Key = UserProfile().Get_Keys(Password = config.Password).PublicKey
    PublicKey = Encoding().To_Base64(Input = Public_Key)
    Address = "ZAZGHWIVDMXYHQ9QUQCNXLSANS9FKIAFZJUPLWXPHKKQPPJWWKR9OCDAQJALIXYE1LMIDMMEFRWCOBYMC"
    Ledger_Dic = Sending_Message(Password = config.Password).Onionizing(Message = "lol")
