from iota.crypto.addresses import AddressGenerator
import sys
import random

#Generate a random number
begin = random.randint(0,1000)
end = random.randint(0,1000)

Seed_key = str(sys.argv[1])

generator = AddressGenerator(Seed_key)

generated_address = generator.create_iterator(start = int(begin), step = int(end))
for i in generated_address:
	print(i)
	break
