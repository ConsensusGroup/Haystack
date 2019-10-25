from DynamicPublicLedger_Module import Dynamic_Public_Ledger
from Haystack_Module import Sender_Client
from Inbox_Module import Trusted_Paths

DLP_Accounts = [['MYNF9HISFJBNQQKLHQTNQKPTTUSBORWGEFAAZMHSNNGRJQRJPET9SZBZKRWMQGMEEHNEVILAPEDRYYBZD', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAslXUjCGWvLOfV4+cMwy+\nxhmjyBuLFHieteDNT9NR4iUREpeLxs/XoXeimC+umJ6nmKkjFcLBS/m9fEFic7fY\nVU2Kn8O7oyWa0CiKyXbPKS1logAG3khmZ6w/bep1VNHAMuvhL40+fBADWpfoekwy\nQUtJYvcTaXL2fzjtx4d4nGdbogYz/OATXDlOUwK3OjRH2fptJse0lI6lKLCptN18\nVwIg0PY3rKjmzboxKchvJvb8GiqWheGoJ6a9DHjYx5qhtJHDYbWF7bSP2w1XmXHA\nUHTkJRej9UgkEtAkMN6p4HDqkrVvwSRO7ct3CpGN5mFI56QejKcgHUmb7M0yEpd+\nOwIDAQAB\n-----END PUBLIC KEY-----'], ['OIOGMSDNKXUQNGDJBTLBIBGFZJNVCXYUFOXEBFDZOETRMOQPXMSSOCWFXEJLISWGVUTSIKGEINTYQIMKB', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4nhhrzizgL1ahKoJYknd\nnoB9LfV261dRfonW5W3xYPijjgbbHoI+NE8Sp9UmehNvUFDANoSzj1uhSDbXfabr\nKoliAGkn3yeocxxLIvNFL3Vd4vMsHGxpm+wdEgKNO8MoWvlGwn/vT+ElBp57qhzo\nD6HXlxcRd22cEFOunYzAEs7U99OT0pKbJjHX+g/FCuBrLLNHAiDK0VvydLFKm34G\nDWyEEIFVp5Vc97pmb15GX+lZeFov14ZnxG6hAAyCCoKZgoCSi0P4WQbwfDa9R4Wq\nRFWX30lGRB9QmrfArGnOFVzuBoeCLNAK4v06mkNxq8jEl91pCHQIbK5wqynAk5ke\nqwIDAQAB\n-----END PUBLIC KEY-----'], ['U9NFUAQWCRGZHVNSGZEMBDBXJAJINYIGFCDFMNGWB9IAGBQEKSCAITJVPQGKISPETHXJFOLY9SIBIZFYW', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkHjW+BhLQ8kuu/2o/qxv\nGFv9zsLQ7osWkH7igY9nS56yM8q6RkAcdBx7pybYxPazlSa0Rppa0pftG2ySgHbI\n8z6k9ExVe7dkeHfiftSZk/nTsdhSpcuWp9xzdEQ65jYA+istiqzJk0zTV1zJFqTe\naUvYG1i8pI7/UbvuDcEM+X5n6bD+pdW9pjxEinx0h7l1apX1gqu5S9Kkvud/4EZ/\n4jKaBb+FBQ/1GZtgL7fLJuiTygoWfeenUwXzs+2SfdRac7h6dLv/qfoU0vprZUfa\n2LftSfu9g164Fwts8/MLrAw8guQCpyA3b6Ax+BHPHW58xPlGdSueHZnwG/7Q1VHa\niwIDAQAB\n-----END PUBLIC KEY-----'], ['RWZZV99SF9IQTCIHHEQEUQCVFOQDWBQEOEHIOXHJSWWTRMOQYOAWSWIFCARLISNDRITATHRYYGMIDVCZ9', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4/ADpey96Ge3GlphkpCF\nudKVT5ajzIvqO2ZF74r8bo+O8n/F1IkjltJZVndkMs+PHkjGA4vM12Yd7pwBqGE/\nE1CXEPZoO6fDltYqB2J9jZGKntU8fSQ+r8GaRN18w/RZiN+bc7q+B3wSSgf0jy3u\nKf6G2NO+XEl23ezV690TP1HKQWPUbUJQ4RqytBVflz4/bA7o8EtoWVcgB8g/kEfG\neXm+TNkfU4jlpNHKgqGMBw4HO3be14Ru/jk/3h74fIv8pGEhmcpG16cEGcztWbNx\nqurHyCo1UMl0DrCLLT4eab7TKKibJRdT0aFV2SoO3dcWcfB7mu8rdFudPywjlXWb\n0wIDAQAB\n-----END PUBLIC KEY-----'], ['UQMPZXWD9M9BHZSQETSXSMLAYNNHJOKAFDMXZIEIWRAADXMM9DPHLLCNWQWOTHQCORMIMDQ9A9HYCPBEW', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt8wtd9ht6EQT3icGqgX4\n2P+77Ucu3ijMnB2LEuh2TNfCxo00FJ3Hwq+X0w77JCx8IqkQn7iBfBNke9H7cigq\nfOZ9zjaFHddoYhf0iPasU27hcvjhRWWkfBUN5cwxkPrfyQkXnz1vIr1kBpuBxAH+\nI8jzuCW9JvR0TfR5REHfgMb+/ccN69mYMB3WXHiKuhE7WYUMaCgBf8k+DwN09g2s\nhxAlNSYz86HlXEzgbop7bHsYF2moNNv7lgHZMYoga+1SubCwH79hS2LkdLd8xBDm\nL2LWq+PSPob5z7fyh5pZdtcyDWTSXHmfUqsAy3Ui9TaOu6OMpxC/QD7AXZSMORyd\nNQIDAQAB\n-----END PUBLIC KEY-----']]

def Test_DPL():
    DLP = Dynamic_Public_Ledger().Start_Ledger()
    print(DLP.Ledger_Accounts)

def Test_Sender(Message, DLP_Accounts):
    print(Sender_Client().Send_Message(Message = Message, ReceiverAddress = DLP_Accounts[0][0], PublicKey = DLP_Accounts[0][1], DifferentPaths = 1))

def Test_Paths():
    x = Trusted_Paths()
    x.Catch_Up()

def Test_Trajectory():
    x = Trusted_Paths()
    x.Ping_Function()

if __name__ == "__main__":
    #Test_Paths()
    #Test_DPL()
    Test_Sender(Message = "This12345 is seems to work very well but I want to test this again. The update has local storage of the addresses being uplaoded to the ledger!", DLP_Accounts = DLP_Accounts)
    #Test_Trajectory()
