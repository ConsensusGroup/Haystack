import os
import json
from base64 import b64encode, b64decode
from Configuration_Module import Configuration
import math

class Encoding:
    def __init__(self):
        pass

    def To_Base64(self, Input):
        return b64encode(Input)

    def From_Base64(self, Input):
        return b64decode(Input)


class Tools:
    def __init__(self):
        pass

    def File_Manipulation(self, Directory, Setting = ""):
        if os.path.exists(Directory):
            if Setting == "d":
                os.remove(Directory)
            return True
        else:
            if Setting == "b":
                os.makedirs(Directory)
            return False

    def Write_File(self, File_Directory, Data, Setting = "w"):
        #Setting table: w --> Write ### r --> Read ### a --> Append ### x --> Creates new file ### t --> Opens in text mode ### b --> Opens in binary ### + --> Opens file for read write (updating)
        def Write(File_Directory, Data, Setting):
            f = open(File_Directory, Setting)
            f.write(Data)
            f.close()
        try:
            Write(File_Directory, Data, Setting)
            return True
        except FileNotFoundError:
            List = File_Directory.split("/")
            Directory = "/".join(List[:len(List)-1])
            self.File_Manipulation(Directory, Setting = "b")
            Write(File_Directory, Data, Setting)
            return True
        except:
            return False

    def Read_File(self, File_Directory):
        try:
            f = open(File_Directory, "r")
            return f.read()
        except FileNotFoundError:
            return False

    def JSON_Manipulation(self, File_Directory, Setting = "r", **kwargs):
        try:
            if "Dictionary" in kwargs:
                if self.File_Manipulation(Directory = "/".join(File_Directory.split("/")[:len(File_Directory.split("/"))-1])) == False:
                    self.File_Manipulation(Directory = "/".join(File_Directory.split("/")[:len(File_Directory.split("/"))-1]), Setting = "b")
                if Setting == "r":
                    Setting = "w"
                file = open(File_Directory, Setting)
                try:
                    file.write(json.dumps(kwargs["Dictionary"]))
                except TypeError:
                    self.File_Manipulation(Directory = File_Directory, Setting = "d")
                    file = open(File_Directory, Setting)
                    Dictionary = {}
                    for label, value in kwargs["Dictionary"].items():
                        if isinstance(value, bytes) == True:
                            value = str(Encoding().To_Base64(Input = value), "utf-8")
                        Dictionary[label] = value
                    file.write(json.dumps(Dictionary))
                return True
            else:
                return json.load(open(File_Directory, Setting))
        except FileNotFoundError:
            return False

    def Epoch_To_Block(self, Epoch_Time):
        c = Configuration()
        BlockFloat = float(Epoch_Time - c.Genesis_Time)/float(c.Block_Duration)
        Block_Remainder = BlockFloat - math.trunc(BlockFloat)
        CurrentBlock = math.trunc(BlockFloat)
        return [CurrentBlock, Block_Remainder]
