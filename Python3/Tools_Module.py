import os
import json

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
                file = open(File_Directory, "w")
                file.write(json.dumps(kwargs["Dictionary"]))
                return True
            else:
                return json.load(open(File_Directory, Setting))
        except FileNotFoundError:
            return False
