import a
import b
import c
import d
import e
from a import DynamicPublicLedger_Module
from b import DynamicPublicLedger_Module
from c import DynamicPublicLedger_Module
from d import DynamicPublicLedger_Module
from e import DynamicPublicLedger_Module
from time import sleep

BlockTime = 3000050
#Starting the user profiles
UserA = a.User_Modules.User_Profile()
UserB = b.User_Modules.User_Profile()
UserC = c.User_Modules.User_Profile()
UserD = d.User_Modules.User_Profile()
UserE = e.User_Modules.User_Profile()

#Test the DLP
while True:
	Ledger = a.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
	print("a")
	b.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
	print("b")
	c.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
	print("c")
	d.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
	print("d")
	e.DynamicPublicLedger_Module.Dynamic_Public_Ledger(BlockTime = BlockTime).Start_Ledger()
	print("e")
	print(Ledger.Ledger_Accounts)
	sleep(60)
