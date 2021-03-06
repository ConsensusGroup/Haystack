from IOTA_Module import IOTA
from Configuration_Module import Configuration
from Tools_Module import Tools, Encoding
from Cryptography_Module import Encryption, Decryption
from UserProfile_Module import UserProfile
from NodeFinder_Module import Return_Optimal_Node, Verify_Node, Force_Alternate_Node
import config
import sys

class DynamicPublicLedger:
    def __init__(self):
        Node = Return_Optimal_Node()
        self.Send_Node = Node[0]
        self.Receive_Node = Node[1]

    def Check_Current_Ledger(self):

        def User_Submission():
            IOTA_Send_Private = Verify_Node(Dictionary = self.Send_Node, Seed = Keys.PrivateSeed)[0]
            String_To_Sign = Encoding().To_Base64(IOTA_Send_Private.Generate_Address(Index = Current_Block) + c.Identifier + Encoding().To_Base64(Input = Keys.PublicKey))
            Signature = Encryption().Sign_Message(ToSign = String_To_Sign, PrivateKey = Keys.PrivateKey, Password = config.Password)
            Ready_To_Submit = Encoding().To_Base64(String_To_Sign+c.Identifier+Signature)
            DPL_Address = IOTA_Receive[0].Generate_Address(Index = Current_Block)
            Verify = Force_Alternate_Node(Dictionary = self.Send_Node, Seed = Keys.PrivateSeed, Address = DPL_Address, Message = str(Ready_To_Submit, "utf-8"))
            return Verify

        c = Configuration()
        u = UserProfile()
        Keys = u.Get_Keys(Password = config.Password)

        IOTA_Receive = Verify_Node(Dictionary = self.Receive_Node, Seed = c.PublicSeed)
        Current_Block = IOTA_Receive[1].CurrentBlock
        Current_Time = IOTA_Receive[1].Current_Time
        print(IOTA_Receive[1].Block_Remainder)
        Entries = Force_Alternate_Node(Dictionary = self.Receive_Node, Seed = c.PublicSeed, Start_Block = Current_Block, End_Block = Current_Block+1)
        if Entries == {}:
            return User_Submission()
        elif Entries != False:
            Current_Ledger = {}
            Ledger_Accounts = Tools().JSON_Manipulation(File_Directory = u.LedgerAccounts)
            for Bundle, Dic in Entries.items():
                Temp = {}
                try:
                    User_Entry = Dic["Message"]
                    Submission_Block = Tools().Epoch_To_Block(Epoch_Time = Dic["Timestamp"])[0]
                    Decoded = Encoding().From_Base64(Input = User_Entry).split(c.Identifier)
                    Address_PublicKey = Encoding().From_Base64(Input = Decoded[0]).split(c.Identifier)
                    User_Address = Address_PublicKey[0]
                    User_PublicKey = Encoding().From_Base64(Address_PublicKey[1])
                    if Decryption().Signature_Verification(ToVerify = Decoded[0], PublicKey = User_PublicKey, Signature = Decoded[1]) == True:# and Submission_Block >= Current_Block-c.Offset:
                        Current_Ledger[str(Address_PublicKey[1], "utf-8")] = str(User_Address, "utf-8")
                        Temp[User_Address.decode("utf-8")] = Current_Block
                        try:
                            Ledger_Accounts[Address_PublicKey[1].decode("utf-8")].update(Temp)
                        except KeyError:
                            Ledger_Accounts[Address_PublicKey[1].decode("utf-8")] = {}
                            Ledger_Accounts[Address_PublicKey[1].decode("utf-8")].update(Temp)
                except:
                    print(sys.exc_info()[1])
            Tools().JSON_Manipulation(File_Directory = u.CurrentLedger, Dictionary = Current_Ledger)
            Tools().JSON_Manipulation(File_Directory = u.LedgerAccounts, Dictionary = Ledger_Accounts)
            Client_Address = str(Verify_Node(Dictionary = self.Send_Node, Seed = Keys.PrivateSeed)[0].Generate_Address(Index = Current_Block),"utf-8")
            if Client_Address not in Current_Ledger.values():
                return User_Submission()
            else:
                return False
