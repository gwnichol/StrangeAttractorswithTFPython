# Touch List
import numpy as np
import random
import sys

if len(sys.argv) == 2:
    size = int(sys.argv[1])
else:
    size = 250
for i in range(size):
    name = ""
    for i in range(12):
        new = random.choice(["A","B","C","D","E",'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y'])
        name = name + new
    print(name)
