##############################################################
##################### Configuration file #####################
##############################################################

class Configuration:
	def __init__(self):
		self.Node = "https://nodes.thetangle.org:443"
		self.PublicSeed = "MKHYA9FZ9STCQGNUIHFVXAAKTP9LSDNEUDSBSBXVQFRTYEMBEMKFIPMHKULCMIIWVGDWWGXTQAKOYGDOW"
		self.Charlib = "0123456789qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM^!$%&/\()=?+*~'#-_.:;,<>|@{[]} "
		self.Default_Size = 128
		self.Identifier = "////"
		self.MessageIdentifier = ">>>>"
		self.Password = "Hello world"  #This can be removed later. This is used password protect the key.
		self.UserFolder = "a/UserData"
		self.KeysFolder = "Keys"
		self.SeedFolder = "PrivateSeed"
		self.PrivateSeed = "PrivateSeed.txt"
		self.PrivateKey = "PrivateKey.pem"
		self.PublicKey = "PublicKey.pem"
		self.GenesisTime = 1520726570370
		self.BlockTime = 100000000
		self.LowerBound = 0.9 #Percentage of block cycle completion. 
		self.RefreshRate = 4 #This is in seconds.
		self.MaxBounce = 1



