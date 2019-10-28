##############################################################
##################### Configuration file #####################
##############################################################

class Configuration:
	def __init__(self):
		self.Node = "http://localhost:14265"
		self.PublicSeed = "QTKBTVTEWBSNBYYFSJTHWZIKOVPHDVNPJAO9BPEOIPFAT9FQNHWDHWSZBNLMLCCT9GLWMYCYWKBIKQART"
		self.Charlib = "0123456789qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM^!$%&/()=?+*~'#-_.:;,<>|@{[] }"
		self.Identifier = "////"
		self.MessageIdentifier = ">>>>"

		#Basic user folder.
		self.Password = "Hello world"  #This can be removed later. This is used password protect the key.
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

		#Trusted Paths variables
		self.PathFolder = "TrustedPaths"
		self.Ledger_Accounts_File = "LedgerAccounts.txt"
		self.Current_Ledger_Accounts = "Current_LedgerAccounts.txt"
		self.TrustedPaths = "Trajectoies.txt"
		self.Last_Block = "LastOnline.txt"
		self.Trajectory_Ping = "Pings.txt"
		self.Trusted_Nodes = "TrustedNodes.txt"

		self.GenesisTime = 100000000
		self.BlockTime = 100000000
		self.LowerBound = 0.9999 #Percentage of block cycle completion.
		self.MaxBounce = 2	#Number of bounces the message will do
		self.Replay = 10	#Number of path blocks to search
		self.DifferentPaths = 1 #This variable allows for the same message to be sent to different paths (increases reliability)
		self.RefreshRate = 4 #Number of seconds the client will check for new messages in the inbox.
		self.Default_Size = 128 #Length of each fragment
