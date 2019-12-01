import config

class Configuration:
    def __init__(self):
        self.PublicSeed = "LSJEPRQURCKBCF9QAACAEIMED9YWECAFSHSWJOOPGRYPHHFOXCLYMOJJNIMDBXWBGWBQBNPFYZIZBYZQF"
        self.Charlib = "0123456789qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM^!$%&/()=?+*~'#-_.:;,<>|@{[] }"

        # Directories used for the application
        # User Profile:
        self.User_Folder = "UserData/"
        self.Keys_Folder = "Keys/"
        self.PrivateSeed_File = "PrivateSeed.txt"
        self.PrivateKey_File = "PrivateKey.pem"
        self.Password = config.Password

        # Inbox:
        self.Message_Folder = "Messages/"
        self.Received_Folder = "ReceivedMessages/"
        self.Relayed_Folder = "RelayedMessages/"
        self.NotRelayed_Folder = "NotRelayedMessage/"
        self.Inbox_Folder = "Inbox/"

        self.Received_File = "Received.txt"
        self.Relayed_File = "Relayed.txt"
        self.NotRelayed_File = "NotRelayed.txt"
        self.Inbox_File = "Inbox.txt"

        #Trusted Paths:
        self.Path_Folder = "TrustedPaths/"
        self.LedgerAccounts_File = "LedgerAccounts.txt"
        self.CurrentLedgerAccounts_File = "Current_LedgerAccounts.txt"
        self.TrustedPaths_File = "Trajectoies.txt"
        self.LastBlock_File = "LastOnline.txt"
        self.TrajectoryPing_File = "Pings.txt"
        self.TrustedNodes_File = "TrustedNodes.txt"

        #Node Finder:
        self.Node_Folder = "Nodes/"
        self.Node_File = "Nodes.txt"

        #Contact:
        self.Contacts_File = "Contacts.txt"
        self.Contacts_Folder = "Contacts/"
