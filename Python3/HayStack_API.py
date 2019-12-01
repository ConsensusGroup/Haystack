#This script is going to be used API calls but first it will serve as a testing script.

from IOTA_Module import *
from Configuration_Module import *
from Tools_Module import *
from UserProfile_Module import *
from Cryptography_Module import *
import config

class HayStack:
    def __init__(self):
        pass

    def Seed_Generator(self):
        Output = Seed_Generator()
        #Output: A 81 character seed for IOTA
        return Output

    def Write_File(self, File_Directory, Data, Setting = "w"):
        Output = Tools().Write_File(File_Directory, Data, Setting)
        #Output: True if file was written, False if failed
        return None

    def Delete_File(self, File_Directory):
        Output = Tools().File_Manipulation(File_Directory, Setting = "d")
        #Output: True if file deleted, False if failed to delete file
        return Output

    def Read_File(self, File_Directory):
        Output = Tools().Read_File(File_Directory)
        #Output: False if file not found/read, Else contents get returned
        return Output

    def Initialization(self):
        Output = Initialization()
        #Output: None

    def Asymmetric_KeyGen(self, Password):
        Output = Key_Generation().Asymmetric_KeyGen(Password)
        #Output: Private key as bytes
        return Output

    def Import_PrivateKey(self, PrivateKey, Password):
        Output = Key_Generation().Import_PrivateKey(PrivateKey, Password)
        #Output Objects: PrivateKey, PublicKey
        return Output

    def JSON_Manipulation(self, File_Directory, **kwargs):
        Output = Tools().JSON_Manipulation(File_Directory, **kwargs)
        print(Output)
        return Output

if __name__ == "__main__":
    x = HayStack()
    c = Configuration()

    #Change this to test module
    Function = "JSON_Manipulation"

    if Function == "Seed_Generator":
        print(x.Seed_Generator())
    if Function == "Write_File":
        x.Write_File(File_Directory = c.User_Folder+"/"+c.Keys_Folder+"/"+c.PrivateKey_File, Data = "Hello")
    if Function == "Delete_File":
        x.Delete_File(File_Directory = c.User_Folder+"/"+c.Keys_Folder+"/"+c.PrivateKey_File)
    if Function == "Read_File":
        print(x.Read_File(File_Directory = c.User_Folder+"/"+c.Keys_Folder+"/"+c.PrivateKey_File))
    if Function == "Initialization":
        x.Initialization()
    if Function == "Asymmetric_KeyGen":
        print(x.Asymmetric_KeyGen(Password = ""))
#    if Function == "Import_PrivateKey": # Need to test wrong password case to catch exception
#        x.Import_PrivateKey(PrivateKey = Key, Password = "")
    if Function == "JSON_Manipulation":
        x.JSON_Manipulation(File_Directory = c.User_Folder+"/"+c.Keys_Folder+"/"+c.PrivateKey_File)
