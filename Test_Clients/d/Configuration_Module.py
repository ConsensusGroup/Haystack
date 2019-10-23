##############################################################
##################### Configuration file #####################
##############################################################

class Configuration:
	def __init__(self):
		self.Node = "http://localhost:14265"
		self.PublicSeed = "QTKBTVTEWBSNBYYFSJTHWZIKOVPHDVNPJAO9BPEOIPFAT9FQNHWDHWSZBNLMLCCT9GLWMYCYWKBIKQART"
		self.Charlib = "0123456789qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM^!$%&/()=?+*~'#-_.:;,<>|@{[] }"
		self.Default_Size = 128
		self.Identifier = "////"
		self.MessageIdentifier = ">>>>"
		self.Password = "Hello world"  #This can be removed later. This is used password protect the key.
		self.UserFolder = "UserData"
		self.KeysFolder = "Keys"
		self.SeedFolder = "PrivateSeed"
		self.PrivateSeed = "PrivateSeed.txt"
		self.PrivateKey = "PrivateKey.pem"
		self.PublicKey = "PublicKey.pem"
		self.MessageFolder = "Messages"
		self.ReceivedMessages = "ReceivedMessages"
		self.RelayedMessage = "RelayedMessages"
		self.NotRelayedMessage = "NotRelayedMessage"
		self.GenesisTime = 100000000
		self.BlockTime = 100000000
		self.LowerBound = 0.9999 #Percentage of block cycle completion.
		self.MaxBounce = 2
		self.Replay = 10
		self.DifferentPaths = 3 #This variable allows for the same message to be sent to different paths (increases reliability)
		self.RefreshRate = 4 #Number of seconds the client will check for new messages in the inbox.
