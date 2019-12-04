import config

class Configuration:
    def __init__(self):
        self.PublicSeed = "LSJEPRQURCKBCF9QAACAEIMED9YWECAFSHSWJOOPGRYPHHFOXCLYMOJJNIMDBXWBGWBQBNPFYZIZBYZQF"
        self.Charlib = "0123456789qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM^!$%&/()=?+*~'#-_.:;,<>|@{[] }"
        self.Genesis_Time = 1575457718533 #Epoch time in seconds
        self.Block_Duration = 30 #600 #block is valid for 10 minutes
        self.Identifier = b'///'

        # Directories used for the application
        # User Profile:
        self.User_Folder = "UserData/"
        self.Keys_Folder = "Keys/"
        self.PrivateKey_File = "Keys_Seed.txt"
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
        self.Preloaded_Nodes = ["http://localhost:14265", "https://mama.iota.family:14267", "http://node05.iotatoken.nl:16265", "https://nodes.iota.cafe:443", "https://we-did-it.org:14265", "https://node.iri.host:443", "https://node.iota-tangle.io:14265", "https://node04.iotatoken.nl:443", "https://node02.iotatoken.nl:443", "https://pool.trytes.eu","https://nutzdoch.einfachiota.de","https://pow.iota.community:443","https://papa.iota.family:14267","https://piota-node.com:443","https://v22018036012963637.bestsrv.de:14267","https://trinity.iota-tangle.io:14265","https://dyn.tangle-nodes.com:443","https://perma.iota.partners:443","https://gewirr.com:14267","https://node01.iotatoken.nl:443","https://node01.iotatoken.nl:443","https://www.iotaqubic.us:443","https://community.tanglebay.org","https://node.deviceproof.org:443","https://nodes.thetangle.org:443","https://wallet1.iota.town:443","https://wallet2.iota.town:443","https://iota.chain.garden:443","https://nodes.thetangle.org:443","https://node.trustingiot.com:443","https://power.benderiota.com:14267","https://www.iotaqubic.us:443","https://stirrlink.dyndns.org:14267","https://iota1.chain.garden:443","https://nod3.theshock.de:443","https://wallet1.iota.town:443","https://node00.gubiota.ch:443","https://node01.gubiota.ch:443","https://node02.gubiota.ch:443","https://iotanow.nl:443"]

        #Contact:
        self.Contacts_File = "Contacts.txt"
        self.Contacts_Folder = "Contacts/"
