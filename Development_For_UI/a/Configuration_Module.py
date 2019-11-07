##############################################################
##################### Configuration file #####################
##############################################################
import config

class Configuration:
	def __init__(self):
		self.Node = "http://localhost:14265"
		self.PublicSeed = "QTKBTVTEWBSNBYYFSJTHWZIKOVPHDVNPJAO9BPEOIPFAT9FQNHWDHWSZBNLMLCCT9GLWMYCYWKBIKQART"
		self.Charlib = "0123456789qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM^!$%&/()=?+*~'#-_.:;,<>|@{[] }"
		self.Identifier = "////"
		self.MessageIdentifier = ">>>>"

		#Basic user folder.
		self.Password = config.Password
		self.UserFolder = "UserData"
		self.KeysFolder = "Keys"
		self.SeedFolder = "PrivateSeed"
		self.PrivateSeed = "PrivateSeed.txt"
		self.PrivateKey = "PrivateKey.pem"
		self.PublicKey = "PublicKey.pem"

		#Inbox related variables
		self.MessageFolder = "Messages"
		self.ReceivedMessages = "ReceivedMessages"
		self.RelayedMessage = "RelayedMessages"
		self.NotRelayedMessage = "NotRelayedMessage"
		self.Inbox = "Inbox"

		#Trusted Paths variables
		self.PathFolder = "TrustedPaths"
		self.Ledger_Accounts_File = "LedgerAccounts.txt"
		self.Current_Ledger_Accounts = "Current_LedgerAccounts.txt"
		self.TrustedPaths = "Trajectoies.txt"
		self.Last_Block = "LastOnline.txt"
		self.Trajectory_Ping = "Pings.txt"
		self.Trusted_Nodes = "TrustedNodes.txt"
		self.Ping_Rate = 20 #After how many iterations of going through checking inbox. i.e. after 6 times check inbox send ping #Being removed in the UI release

		#Contact Module parameters
		self.Contacts_File = "Contacts.txt"
		self.Contacts_Folder = "Contacts"

		#Other parameters
		self.GenesisTime = 1572000000000
		self.BlockTime = 1000000
		self.LowerBound = 0.9999 #Percentage of block cycle completion.
		self.MaxBounce = 2	#Number of bounces the message will do
		self.Replay = 10	#Number of path blocks to search
		self.DifferentPaths = 1 #This variable allows for the same message to be sent to different paths (increases reliability)
		self.RefreshRate = 5 #Number of seconds the client will check for new messages in the inbox.
		self.Default_Size = 128 #Length of each fragment
