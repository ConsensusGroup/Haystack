from DynamicPublicLedger_Module import Dynamic_Public_Ledger
from Haystack_Module import Sender_Client
from Inbox_Module import Trusted_Paths
from IOTA_Module import *
from User_Modules import User_Profile

DLP_Accounts = [['MHWYDYXAGFMSWGVTZGWBCOTOGNHHBFYYZAGWGUNQFWEBNCHOJHMT9LDFTPFZ9HLAYNRQWENPJIGKZEPZ9', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqjl0qGSjMAb0XFicS45h\nxVBCxvprisE2pKuOgrg/lKHx7zqf9V6f6W6tkmo0megeTnjuUOBYHssdknmNf4Cx\nVysWp2bWVArfMh9eJWlmJh68ASYQ/6aeGMMLgWWuHeG6RYskaNEybgPZPOKLutCh\nqI0v8AJslBADU8Jd45BPivuT3yDeJYPhKLvrJ5AsmcqvPh0i5A34rYSe2XLvYUT0\nBZq4anYc3z5BWgTyvXc1QIBXoIZlJ16MDCVaqiPu5yc/rkWKQk6pbr2Pv/mju4jH\nDuH5S/pDI8M2rdP2JGF0HPnQB91c0k+ieIaMaVi0xTYa48iGViDEGMHDPFpTNoVy\nwwIDAQAB\n-----END PUBLIC KEY-----'], ['QPXIOBJ9JROE9STXJSQIC9THAQBYYKHDRUVHLEHYWEFXRPGBSQSBY9NHHBSTTPXTWRPHZPGGBFQJIYDBX', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwhEEPJBaCUTJl6ACRZGi\n0czLiaHVfHOQVrcA7WgUPqMtaSVnTTe6KQ0MCSTu525RCfWYPM8CcVWBbzaleXKg\nRis65tfQn1Atn6Womf7JpbGsUhymvsbCB+SVdNyXPBE0nBlyPzdOMzM6oXpA9r5d\n1vP8AuMjFRcwDB3Gc7UXBISKtFyFT3tF4f5ooOdWxzNP1hRiy4iTZvgkeNyOCko1\njbFkgUL0Og6gWbqc3T785OS7j4f4JvOiuDSFYrYjusuGWQcSlIVJRJTXYNsLDCA3\nCF9EJ4razUXuSW1+KOdWU4NOeBWLPtOyyFWsst1J1hkgjwB4ROeR/+AUUYw7Eaai\nywIDAQAB\n-----END PUBLIC KEY-----'], ['HJ9GTA9EOPXJTNWNEQWCPWUITXKTHIICNHX9SBTEWSEDKQOFYCXAYPA9DBSKBXLZIH9TKLEZIYRTGXNGC', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx4bESkbUJm2L5cWLI5rd\nTThTRI5iMHsPkXxOcneUS+btzM0KCelmukkHUi5WPSfpOcIxHL+VUHZi83xgEQnm\nclANy/vn2B7BmnwNJAooE9aKQCM/TSBxt1QJFWRLa9041eEPnNdHz5z9qL5ye54v\nmDsbGEJ/EY42XqeXqDYBfUXJzL5uMLxXFj2sBWBXOhblWC2nHjrII2pYWLpZu9FK\nx9Ne0Q7mI8TviQbZTL9Tru42Sv3u7bMIABet7qUrM91OZouO6hWPcijjo/qDnKez\nTsXxjaMZ8pzXr9I2ibTrPE9IcZKPTcOuvhfaBRgjmmfLLoacV4pDQBDF9fecITY+\nIQIDAQAB\n-----END PUBLIC KEY-----'], ['GNRRIGWDVHKOPHKEKAO9WBDEHDUYQRCSIQQYIEYYFXMESVCEU9ZYHYFOPWUPRVHLGYRWDGOJECPFSTCRD', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt4asJJb794GKa5JRSt2J\nsmwT5N3RimMX4NnGEZyhoyiAoj0zZ62OG1IU80c7tZMM9wW1Rv3gU4GNhXlYLbiK\ndwkl8LlPYJwVoAaDqntywIij32TJfONdyShxjKrhjgZJrRyvCUERBoYAYUA0iKuz\nEDYvdpJa99JScM0lQEhJ5KQu2BTM3HILGyAnfMbTzTfC3VPmOVFps2sDMn+MJj/5\n/Rz9cQJ/27lmn3jM6j5EQZ2zUwpzGzA/HJnESGtnndy/jntFB7cwJTm1tL0izvUp\nx5rXBt0myKpYnjA4kxqTLAzrdhI1uce+c6tk8m4YsDPie3eAwCNFUjqSHIOVQW/T\n5QIDAQAB\n-----END PUBLIC KEY-----'], ['JCEHFWQCYNFQ9VHR9M9VCVXIKFGRETDSVVHQQSVWLGMZZWFJLARLBZBGANX9SNA9I9UT9RVYK9AIUQRH9', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2I+9QxdyPSSqXuGtEClS\n85LtsuUoMFT7WyL5ek3WmyPDSTk1CIUk+AVrI3KOqQ3zdRM0iVzIy1iwBm4uKquL\nHrjPiNXjeQIH5PQF2QNDQVMJIKNm7DKzGOpwtkJSQRucwgoGCqIEHaqDfTgzCeXt\nOLwHryGylNAsOkWPgNQp4ERf0psuzv0Q4CPJ3bibS0YGMT/BrPmzWU5L5ZZgEpt0\n/AgEOZ8GCM3//ws2Ntq7TH0jnvt+XDsnHkdSvTkUZfPMc4Fbsmsg7sNZDS1fgwa4\n1oKCAQJuLbV43oXut8rzG9dCG+IMuWY7kazeK5fIeeggoY1iEZ6qaN5GNvGpI+V4\nCwIDAQAB\n-----END PUBLIC KEY-----']]




def Test_DPL():
	DLP = Dynamic_Public_Ledger()
	DLP.Start_Ledger()
	print(DLP.Check_User_In_Ledger().Ledger_Accounts)
	print("#####")
	print(DLP.Check_User_In_Ledger(Current_Ledger = True).Ledger_Accounts)

def Test_Sender(Message, DLP_Accounts):
    Sender_Client().Send_Message(Message = Message, ReceiverAddress = DLP_Accounts[2][0], PublicKey = DLP_Accounts[2][1], DifferentPaths = 1)

def Test_Paths():
    x = Trusted_Paths()
    x.Catch_Up()

def Test_Trajectory():
    x = Trusted_Paths()
    y = Sender_Client().Ping_Function()
    x.Scan_Paths()

def Play():
	for i in range(15):
		print(IOTA_Module(Seed = User_Profile().Private_Seed).Generate_Address(Index = Dynamic_Public_Ledger().Calculate_Block().Block+i))
		print(IOTA_Module(Seed = User_Profile().Private_Seed).Generate_Address(Index = Dynamic_Public_Ledger().Calculate_Block().Block-i))

if __name__ == "__main__":
    #Test_Paths()
    #Test_DPL()
    Test_Sender(Message = "Did you receive my latest messsage bra???? This is a secret conversion.", DLP_Accounts = DLP_Accounts)
    #Test_Trajectory()
	#Play()
