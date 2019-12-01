from Tools_Module import Tools
from Configuration_Module import Configuration
from Cryptography_Module import Encryption, Decryption, Key_Generation
from User_Modules import User_Profile, Initialization
from IOTA_Module import IOTA_Module
import config
import getpass

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
        Submit = IOTA_Module(Seed = Private_Seed).Send(ReceiverAddress = BackUpAddress, Message = self.Decompose())
        print("Receipt: "+str(Submit))

class Restore:
    def __init__(self, SuperSecretKey1, SuperSecretKey2):
        self.SuperSecretKey1 = SuperSecretKey1
        self.SuperSecretKey2 = SuperSecretKey2
        self.Conf = Configuration()

    def DownloadDB(self):
        DB = IOTA_Module(Seed = self.Conf.PublicSeed).Receive(Start = 2).Message
        Output = ""
        for i in DB:
            i = i[1:len(i)-1] #Removes the " " from the cipher
            LayerOne = Decryption().SymmetricDecryption(CipherText = i, SecretKey = self.SuperSecretKey2)
            Keys = Decryption().SymmetricDecryption(CipherText = LayerOne, SecretKey = self.SuperSecretKey1)
            if self.Conf.Identifier in Keys:
                Output = Keys.split(self.Conf.Identifier)
        if Output == "":
            return False
        else:
            return Output

    def Restore_FileDirectory(self):
        Outcome = self.DownloadDB()
        HayStackPW = config.Password
        Found = False
        if isinstance(Outcome, list) == True:
            PEM_Directory = self.Conf.UserFolder + "/" + self.Conf.KeysFolder + "/" + self.Conf.PrivateKey
            Seed_Directory = self.Conf.UserFolder + "/" + self.Conf.SeedFolder +"/" + self.Conf.PrivateSeed
            for i in range(10):
                try:
                    if Tools().Check_File(File = PEM_Directory) == False:
                        Decoded_Private = Tools().Base64_To_String(Encoded = Outcome[0])
                        Tools().Write(directory = PEM_Directory, data = Decoded_Private)
                    if Tools().Check_File(File = Seed_Directory) == False:
                        try:
                            Import = Key_Generation().PrivateKey_Import(Password = HayStackPW)
                            Data = Encryption().AsymmetricEncryption(PlainText = Outcome[1], PublicKey = Import.PublicKey)
                            Tools().Write(directory = Seed_Directory, data = Data)
                            Found = True
                            config.Password = HayStackPW
                        except ValueError:
                            print("Please enter the password for your old HayStack account: \n")
                            Password = getpass.getpass()
                            HayStackPW = Password
                except IOError:
                    Initialization().Build_Application()

        if Found != False:
            #Make sure that the block number is being set to 3
            Tools().Build_Directory(directory = str(self.Conf.UserFolder+"/"+self.Conf.PathFolder))
            Tools().Build_DB(File = str(self.Conf.UserFolder+"/"+self.Conf.PathFolder+"/"+self.Conf.Last_Block))
            Block_Number = Tools().Add_To_Dictionary(Input_Dictionary = {}, Entry_Label = "Block", Entry_Value = 3)
            Tools().Write_To_Json(directory = str(self.Conf.UserFolder+"/"+self.Conf.PathFolder+"/"+self.Conf.Last_Block), Dictionary = Block_Number)

        return Found
