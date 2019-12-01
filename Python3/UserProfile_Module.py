from Configuration_Module import Configuration
from Tools_Module import Tools
from Cryptography_Module import Key_Generation

def Initialization():
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
    PrivateKey = Keys + con.PrivateKey_File
    PrivateSeed = Keys + con.PrivateSeed_File
    Received = Received + con.Received_File
    Relayed = Relayed + con.Relayed_File
    NotRelayed = NotRelayed + con.NotRelayed_File
    Inbox = Inbox + con.Inbox_File

    LedgerAccounts = Path + con.LedgerAccounts_File
    CurrentLedger = Path + con.CurrentLedgerAccounts_File
    Trust = Path + con.TrustedPaths_File
    LastBlock = Path + con.LastBlock_File
    Traj = Path + con.TrajectoryPing_File
    Trusted = Path + con.TrustedNodes_File
    Node = Node + con.Node_File
    Contact = Contact + con.Contacts_File

    for i in [Trusted, Traj, PrivateKey, PrivateSeed, Received, Relayed, NotRelayed, Inbox, LedgerAccounts, CurrentLedger, Trust, LastBlock,  Node, Contact]:
        if Tools().File_Manipulation(Directory = i, Setting = "") == False:
            pass # Finish writing the setup sequence of the application.
