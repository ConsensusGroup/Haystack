from Tools_Module import Tools
from Configuration_Module import Configuration
from Cryptography_Module import Encryption
from User_Modules import User_Profile
from IOTA_Module import IOTA_Module

class Backup:
    def __init__(self, SuperSecretKey1,SuperSecretKey2):
        Conf = Configuration()
        self.PEMFile = Conf.UserFolder+"/"+Conf.KeysFolder+"/"+Conf.PrivateKey
        self.SuperSecretKey1 = SuperSecretKey1
        self.SuperSecretKey2 = SuperSecretKey2

    def Decompose(self):
        KeyList = Tools().ReadLine(directory = self.PEMFile)
        KeyString = Tools().List_To_String(List = KeyList)
        KeyEncoded = Tools().String_To_Base64(String = KeyString)
        Private_Seed = User_Profile().Private_Seed
        Combined = str(KeyEncoded + Configuration().Identifier+Private_Seed)
        KeyCipher = Encryption().SymmetricEncryption(PlainText = Combined, SecretKey = self.SuperSecretKey1)
        KeyCipher = Encryption().SymmetricEncryption(PlainText = KeyCipher, SecretKey = self.SuperSecretKey2)
        return KeyCipher

    def PublicBackUp(self):
        Public_Seed = Configuration().PublicSeed
        Private_Seed = User_Profile().Private_Seed
        BackUpAddress = IOTA_Module(Seed = Public_Seed).Generate_Address(Index = 2)
        Submit = IOTA_Module(Seed = PrivateSeed).Send(ReceiverAddress = BackUpAddress, Message = self.Decompose())




if __name__ == "__main__":
    x = Backup(SuperSecretKey1 = "YOLO", SuperSecretKey2 = "BOYZZ")
    x.PublicBackUp()
