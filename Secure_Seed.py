# -*- coding: utf-8 -*-
#This generates a cryptographically secure pseudorandom seed corresponding to a wallet on the IOTA network

import subprocess

seed = subprocess.call("cat /dev/urandom |LC_ALL=C tr -dc ‘A-Z9’ | fold -w 81 | head -n 1", shell=True)

print seed
