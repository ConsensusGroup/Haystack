##############################################################
##################### Configuration file #####################
##############################################################

class Configuration:
	def __init__(self):
		self.Node = "https://tuna.iotasalad.org:14265"
		self.PublicSeed = "PJKEJOSPR99CK9TVRJUUDYRWZX9IPIQBRUCWOQMQSKOGEWXYOIFGKXSCSAUTKLDQYNZWMSTVRIUXCGZZQ"
		self.Default_Size = 256
		self.Identifier = "////"
		self.Password = "Hello world"  #This can be removed later. This is used password protect the key.
		self.UserFolder = "UserData"
		self.KeysFolder = "Keys"
		self.SeedFolder = "PrivateSeed"
		self.PrivateSeed = "PrivateSeed.txt"
		self.PrivateKey = "PrivateKey.pem"
		self.PublicKey = "PublicKey.pem"
		self.GenesisTime = 1520726570370
		self.BlockTime = 1000000


