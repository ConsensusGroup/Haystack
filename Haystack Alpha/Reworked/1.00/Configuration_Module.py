##############################################################
##################### Configuration file #####################
##############################################################

class Configuration:
	def __init__(self):
		self.Node = "https://tuna.iotasalad.org:14265"
		self.PublicSeed = "MKHYA9FZ9STCQGNUIHFVXAAKTP9LSDNEUDSBSBXVQFRTYEMBEMKFIPMHKULCMIIWVGDWWGXTQAKOYGDOW"
		self.Charlib = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/-=% '
		self.Default_Size = 256
		self.Identifier = "////"
		self.Password = "Hello world"  #This can be removed later. This is used password protect the key.
		self.UserFolder = "a/UserData"
		self.KeysFolder = "Keys"
		self.SeedFolder = "PrivateSeed"
		self.PrivateSeed = "PrivateSeed.txt"
		self.PrivateKey = "PrivateKey.pem"
		self.PublicKey = "PublicKey.pem"
		self.GenesisTime = 1520726570370
		self.BlockTime = 1000000000000000000
		self.LowerBound = 0.9 #Percentage of block cycle completion. 
		self.RefreshRate = 2 #This is in seconds.
		self.MaxBounce = 1
		self.MaxLength = 2096

