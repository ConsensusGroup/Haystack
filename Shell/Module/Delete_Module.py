import sys

Contacts = str(sys.argv[1])
User_Output = Contacts.split("#")
Name = User_Output[0]
Address = User_Output[1]
Return_String = str(Name+" "+Address)
