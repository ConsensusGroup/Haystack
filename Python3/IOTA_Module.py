#IOTA library
from iota import TryteString, Address, ProposedBundle, ProposedTransaction, Bundle
from iota.crypto.addresses import AddressGenerator
from iota.adapter import HttpAdapter
from iota import *

#Cryptography library
from random import SystemRandom

def Seed_Generator():
    trytes = [i for i in map(chr, range(65,91))]
    trytes.append("9")
    Seed = [trytes[SystemRandom().randrange(len(trytes))] for x in range(81)]
    return "".join(Seed)
