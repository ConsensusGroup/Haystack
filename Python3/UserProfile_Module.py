from Configuration_Module import Configuration
from IOTA_Module import Seed_Generator
from Tools_Module import Tools, Encoding
from Cryptography_Module import Key_Generation, Encryption, Decryption
import config

def Initialization():
    u = UserProfile()
    for i in [u.Trusted, u.Traj, u.Keys, u.Received, u.Relayed, u.NotRelayed, u.Inbox, u.LedgerAccounts, u.CurrentLedger, u.Trust, u.LastBlock,  u.Node, u.Contact]:
        if Tools().File_Manipulation(Directory = i) == False:
            Tools().JSON_Manipulation(File_Directory = i, Dictionary = {})

        # This segment clears the node results when starting the application. This forces the application to retest the IOTA nodes. 
        if i == u.Node:
            Tools().JSON_Manipulation(File_Directory = i, Dictionary = {})

    if Tools().JSON_Manipulation(File_Directory = u.Keys) == {}:
        PrivDic = {}
        PrivDic["PrivateKey"] = Key_Generation().Asymmetric_KeyGen(Password = config.Password)
        PrivDic["PublicKey"] = Key_Generation().Import_PrivateKey(PrivateKey = PrivDic["PrivateKey"], Password = config.Password).PublicKey
        PrivDic["PrivateSeed"] = Encryption().Asymmetric_Encryption(PlainText = Seed_Generator(), PublicKey = PrivDic["PublicKey"])
        Tools().JSON_Manipulation(File_Directory = u.Keys, Dictionary = PrivDic)

class UserProfile():
    def __init__(self):
        con = Configuration()

        #ROOT directory
        Root = con.User_Folder

        #Seed and Private key directory
        Keys = Root+con.Keys_Folder

        #Messages and relaying mechamism folder
        Messages = Root + con.Message_Folder
        Received = Messages + con.Received_Folder
        Relayed = Messages + con.Relayed_Folder
        NotRelayed = Messages + con.NotRelayed_Folder
        Inbox = Messages + con.Inbox_Folder

        #Other Directories
        Path = Root + con.Path_Folder
        Node = Root + con.Node_Folder
        Contact = Root + con.Contacts_Folder

        for i in [Root, Keys, Messages, Received, Relayed, NotRelayed, Inbox, Path, Node, Contact]:
            Tools().File_Manipulation(Directory = i, Setting = "b")

        #File directories:
        self.Keys = Keys + con.PrivateKey_File
        self.Received = Received + con.Received_File
        self.Relayed = Relayed + con.Relayed_File
        self.NotRelayed = NotRelayed + con.NotRelayed_File
        self.Inbox = Inbox + con.Inbox_File
        self.LedgerAccounts = Path + con.LedgerAccounts_File
        self.CurrentLedger = Path + con.CurrentLedgerAccounts_File
        self.Trust = Path + con.TrustedPaths_File
        self.LastBlock = Path + con.LastBlock_File
        self.Traj = Path + con.TrajectoryPing_File
        self.Trusted = Path + con.TrustedNodes_File
        self.Node = Node + con.Node_File
        self.Contact = Contact + con.Contacts_File

    def Get_Keys(self, Password):
        Dictionary = Tools().JSON_Manipulation(File_Directory = self.Keys)
        PrivateKey = Encoding().From_Base64(Input = Dictionary["PrivateKey"])
        self.PrivateKey = PrivateKey
        self.PrivateSeed = Decryption().Asymmetric_Decryption(CipherText = Encoding().From_Base64(Input = Dictionary["PrivateSeed"]), PrivateKey = PrivateKey, Password = config.Password)
        self.PublicKey = Encoding().From_Base64(Input = Dictionary["PublicKey"])
        return self
