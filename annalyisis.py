from os import listdir
from os.path import isfile, join
import numpy as np

mypath = "./SortTest"
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
codes =  []
results = np.zeros(shape=(25,12))
for a in filenames:
    code = a[:12]
    codes.append(code)
    first = 0
    for letter in code:
        index = ["A","B","C","D","E",'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'].index(letter)
        results[index,first] += 1
        first += 1
results = results / ((1/25)*(len(filenames)))
#print(codes)
print("After " + str(len(filenames)) + " tests")
print(results)

# Calculate deviation
print("Deviation: " + str(np.std(results)))
